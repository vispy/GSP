# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
The role of the Command class is to facilitate the writing of the reference
implementation. It is *not* part of the protocol.
"""
import yaml
import json
import inspect
import itertools
import numpy as np
from datetime import datetime
from functools import wraps
from gsp.core.object import Object, OID

def json_default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def get_default_args(func):
    """Retrieve default arguments and their values from a function. """
    
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty }

def command(method=None, record=None, output=None):
    """Function decorator that create a command when the function is called and
    optionally record it and/or write it to stdout. The name of the method it
    decorates can be overriden with the method argument. """

    def wrapper(func):

        @wraps(func)
        def inner(self, *args, **kwargs):
            keys = func.__code__.co_varnames[1:]
            values = args
            defaults = get_default_args(func)
            
            func(self, *args, **kwargs)

            # Add self (identifying by id) to parameters
            parameters = {"id": self.id}

            # Parameters
            for key,value in zip(keys,values):
                parameters[key] = value

            # Named parameters
            for key,value in zip(kwargs.keys(), kwargs.values()):
                if key not in parameters.keys():
                    parameters[key] = value

            # Default parameters
            for key,value in defaults.items():
                if key not in parameters.keys():
                    parameters[key] = value

            classname = self.__class__.__name__
            methodname = func.__code__.co_name if method is None else method
            command = Command()
            command.register(classname, methodname, parameters)

            if record != False and (record or Command.record):
                Command.commands.append(command)

            if output != False and (output or Command.output):
                print(command.yaml_dump())
                
        return inner
    return wrapper


class CID(yaml.YAMLObject):
    """
    Command unique identification
    """

    # YAML tag (class attribute)
    yaml_tag = "!CID"

    # YAML loader (class method)
    yaml_loader = yaml.SafeLoader

    # Identifier counter
    counter = itertools.count()

    def __init__(self, id : int = None):
        """ Creates a new identifier unless id is provided. """

        if id is None:
            self.id = 1 + next(CID.counter)
        else:
            self.id = int(id)

    def __eq__(self, other):
        if isinstance(other, (int,)):
            return self.id == other
        else:
            return self.id == other.id

    def __int__(self):
        return self.id
    
    def __hash__(self):
        return self.id

    def __repr__(self):
        return "%d" % self.id

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.id}'.format(node))

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(node.value)


class Command:
    """ Generic command with a unique id. """

    # Flag indicating whether to record commands
    record = True

    # Flag indicating whether to print when registering a new command
    output = True

    # List of issued commands
    commands = []
    

    def __init__(self):
        self.id = CID()
        self.timestamp = datetime.timestamp(datetime.now())
            
    def register(self, classname : str,  methodname : str, parameters : dict):
        """ Register a new method call """

        if "id" not in parameters.keys():
            raise ValueError("Parameters needs to have an id")
        
        self.classname = classname
        self.methodname = methodname
        self.parameters = parameters
        for key, value in parameters.items():
            if isinstance(value, Object):
                self.parameters[key] = value.id

    def record(self, classname : str,  methodname : str, parameters : dict):
        """ Register and record a new method call """

        self.register(classname, methodname, parameters)
        self.commands.append(self)

    def execute(self, globals=None, locals=None):
        """ Execute the command. """

        parameters = self.parameters.copy()
        oid = parameters["id"]
        del parameters["id"]
        
        # Resolve objects references
        for key, value in parameters.items():
            if isinstance(value, OID):
                parameters[key] = Object.objects[value]

        if self.methodname is None:
            # Warning: this call advances the object counter, is it a problem?
            object = globals[self.classname](**parameters)
            object.id = oid
            Object.objects[oid] = object
        else:
            getattr(globals[self.classname], method)(Object.objects[oid], **parameters)


    def yaml_load(self, command):
        command = yaml.safe_load(data)[0]
        self.id = command["id"]
        try:
            self.classname, self.methodname = command["method"].split("/")
        except ValueError:
            self.classname, self.methodname = command["method"], None
        self.parameters = command["parameters"]
        self.timestamp = command["timestamp"]


    def yaml_dump(self) -> str:
        if self.methodname:
            method = "%s/%s" % (self.classname, self.methodname)
        else:
            method = self.classname
        data = [ { "method" : method,
                   "id" : self.id,
                   "timestamp" : self.timestamp,
                   "parameters" : self.parameters } ]
        return yaml.dump(data, default_flow_style=None, sort_keys=False)

    def json_dump(self) -> str:
        if self.methodname:
            method = "%s/%s" % (self.classname, self.methodname)
        else:
            method = self.classname
        payload = { "jsonrpc": "2.0",
                    "id" : int(self.id),
                    "timestamp" : self.timestamp,
                    "method" : method,
                    "parameters" : self.parameters }
        return json.dumps(payload, default=json_default)

    def json_load(self, payload) -> str:
        self.id = payload["id"]
        try:
            self.classname, self.methodname = payload["method"].split("/")
        except ValueError:
            self.classname, self.methodname = payload["method"], None
        self.parameters = payload["parameters"]
        self.timestamp = payload["timestamp"]

if __name__ == "__main__":
    import gsp
    
    gsp.mode("client", output=False, reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b): pass

    Test().call(1,2)
    command = gsp.Command.commands[-1]
    print(command.json_dump())
