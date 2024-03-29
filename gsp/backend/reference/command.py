# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
The role of the Command class is to facilitate the writing of the reference
implementation. It is *not* part of the protocol.
"""

import yaml
import typing
import inspect
import itertools
from datetime import datetime
from functools import wraps
from gsp import log
from gsp.converters import *
from gsp.backend.reference.object import Object, OID
from typing import Union, get_origin, get_args


def get_default_args(func):
    """Retrieve default arguments and their values from a function. """
    
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty }


class Converter:
    """This class is used to postpone the conversion of a parameter of
    a command.

    This allows to writes function with types compatible with the
    required type while the actual conversion to the required type
    will be done just in time (depending on the convert flag). This is
    necessary to avoid passing large data from one function to the
    other. For example, numpy arrays ca be kept as such and converted
    to bytes only when it is needed by the protocol (dump functions).

    """
    
    def __init__(self, converter, value):
        self.converter = converter
        self.value = value

    def __call__(self):
        return self.converter(self.value)
    

def command(method=None, record=None, output=None, convert=None):
    """Function decorator that create a command when the function is called and
    optionally record it and/or write it to stdout. The name of the method it
    decorates can be overriden with the method argument. """

    def wrapper(func):

        @wraps(func)
        def inner(self, *args, **kwargs):
            
            no_command = False
            if "__no_command__" in kwargs:
                no_command = True
                del kwargs["__no_command__"]
                
            keys = func.__code__.co_varnames[1:]
            annotations = func.__annotations__
            annotations = typing.get_type_hints(func)

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
                    
            # Check if parameter is of the right type, else, search
            # for a conversion method inside the parameter class.
            for key,value in parameters.items():
                if key in annotations.keys():

                    check = False
                    parameter_type = parameters[key].__class__
                    if "[" in parameter_type.__name__:
                        parameter_type = parameters[key].__class__.__base__
                    
                    if typing.get_origin(annotations[key]) is typing.Union:
                        annotated_types = list(typing.get_args(annotations[key]))
                    else:
                        annotated_types = annotations[key],

                    for annotated_type in annotated_types:
                        # Parameter is an instance of one the annotated type
                        if (annotated_type == parameter_type or
                            isinstance(parameter_type,annotated_type) or
                            issubclass(parameter_type,annotated_type)):
                            check = True
                            break

                        # Name of the potential converter
                        converter ="%s_to_%s" % (parameter_type.__name__, annotated_type.__name__)

                        # converted does not exist, look for parameter bas class
                        if converter not in globals():
                            converter = None
                            for base in value.__class__.__bases__:
                                converter ="%s_to_%s" % (base.__name__, annotated_type)
                                if converter in globals():
                                    break
                                converter = None
                        
                        # Found converter, register it
                        if converter:
                            check = True
                            converter = globals()[converter]
                            # Delayed conversion
                            # parameters[key] = Converter(converter ,value)

                            # Immediate conversion
                            parameters[key] = converter(value)
                    if check:
                        continue
                    else:
                        raise ValueError(
                            "Converter missing for %s to %s" % (parameter_type, annotated_types))


            if not no_command:
                classname = self.__class__.__name__
                methodname = func.__code__.co_name if method is None else method
                command = Command()
                command.register(classname, methodname, parameters)
                if record != False and (record or Command.record):
                    Command.commands.append(command)
                if output != False and (output or Command.output):
                    command.dump()

        return inner
    return wrapper


class CID(yaml.YAMLObject):
    """
    Command unique identification
    """

    # Identifier counter
    counter = itertools.count()

    # YAML tag (class attribute)
    yaml_tag = "!CID"

    # YAML loader (class method)
    yaml_loader = yaml.SafeLoader

    def __init__(self, id = None):
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

    def to_json(self):
        return self.id

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

    # Flag indicating whether to convert parameter immediately (True)
    # or just in time (False)
    convert = False

    # List of issued commands
    commands = []
    

    def __init__(self):
        self.id = CID()
        self.timestamp = datetime.timestamp(datetime.now())
            
    def register(self, classname,  methodname, parameters):
        """ Register a new method call """

        if "id" not in parameters.keys():
            raise ValueError("Parameters needs to have an id")
        
        self.classname = classname
        self.methodname = methodname
        self.parameters = parameters
        for key, value in parameters.items():
            if isinstance(value, Object):
                self.parameters[key] = value.id

    def record(self, classname,  methodname, parameters):
        """ Register and record a new method call """

        self.register(classname, methodname, parameters)
        self.commands.append(self)

    def dump(self):
        """ Dump command is backend specific."""
        raise NotImplementedError

        
    def execute(self, globals=None, locals=None):
        """ Execute the command. """

        parameters = self.parameters.copy()
        oid = parameters["id"]
        del parameters["id"]

        # log.debug(f"Class name: {self.classname}")
        # log.debug(f"Method name: {self.methodname}")
        
        # Resolve objects references
        for key, value in parameters.items():
            if isinstance(value, OID):
                parameters[key] = Object.objects[value]

        if "." in self.methodname:
            module,name = self.methodname.split(".")
            func = getattr(globals[module], name)
            object = func(**parameters)
            object.id = oid
            Object.objects[oid] = object
            return object
        else:
            func = getattr(Object.objects[oid].__class__, self.methodname)
            return func(Object.objects[oid], **parameters)
