# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
The role of the Command class is to facilitate the writing of the reference
implementation. It is *not* part of the protocol.
"""

import sys
import types
import typing
import inspect
import itertools
from datetime import datetime
from functools import wraps
from types import UnionType
from typing import Union, get_origin, get_args

from .. log import log
from .. object import Object, OID
from . convert import Converter, get_converter, register


__record__ = True
""" Global variable controlling whether commands are build and recorded. """

def record(state : bool = False):
    """
    Activate (state=True) or deactivate (state=False) global
    command recording (for all command queues).
    """
    global __record__

    if state:
        __record__ = True
        log.info("Command recording is now ON")
    else:
        __record__ = False
        log.info("Command recording is now OFF")

        return __record__

def queue(name = "default"):
    """
    Return a new or existing command queue.
    """

    return CommandQueue(name)


class NamedSingleton(type):
    """
    NamedSingleton class is a metaclass that can be inherited in
    order to produce uniue objects of a given class, where name is
    used to identify them
    """

    _instances = {}

    def __call__(cls, name="default", *args, **kwargs):
        if name == "active" or name is None:
            if CommandQueue.active is None:
                CommandQueue.active = super(NamedSingleton, cls).__call__("default", *args, **kwargs)
            return CommandQueue.active
        if name not in cls._instances.keys():
            cls._instances[name] = super(NamedSingleton, cls).__call__(name, *args, **kwargs)
        return cls._instances[name]


class CommandQueue(metaclass = NamedSingleton):
    """
    A command queue allows to store a list of Command that can be
    ran later.
    """

    name = "default"
    readonly = False
    commands = None
    active = None

    def __init__(self, name : str = "default"):
        """
        Parameters
        ----------
        name:
            Name of the queue
        """

        self.commands = []
        self.name = name
        self.readonly = False
        CommandQueue.active = self


    def __str__(self):

        s = f"CommandQueue({self.name}, "
        if CommandQueue.active == self:
            s += f"active, "
        else:
            s += f"not active, "
        if self.readonly:
            s += f' read-only) : {len(self)} command(s)\n'
        else:
            s += f' read-write) : {len(self)} command(s)\n'
        for command in self.commands:
            s +=   "  - " + str(command)
        return s

    def empty (self):
        """ Empty the queue """

        self.commands = []
        return self


    def __len__(self):
        """ Length of command queue. """

        return len(self.commands)


    def __getitem__(self, index):
        """ Get command at provided index. """

        return self.commands[index]


    def run(self,  globals=None, locals=None):
        """
        Execute all commands in the queue, with the provided
        globals and locals dictionary that must contain claases and
        methids from all the commands.

        Parameters
        ----------

        globals : dict

            Dictionary containing the current scope's global variables

        locals : dict

            Dictionary containing the current scope's local variables
        """

        readonly = self.readonly
        self.readonly = True
        for command in self.commands:
            command.execute(globals, locals)
        self.readonly = readonly


    def push(self, command):
        """
        Push a new command onto the queue unless it is in
        read-only mode.

        Parameters
        ----------

        command : Command

            Command to be appended to the queue

        Returns
        -------

        True if the command has been pushed to the queue, False else.
        """

        if not self.readonly:
            self.commands.append(command)
            return True
        return False


def get_default_args(func):
    """Retrieve default arguments and their values from a function. """

    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty }



def command(name=None):
    """
    Function decorator that creates a command when the function is
    called and optionally record it. The name of the method can
    can be overriden with the provided name.
    """

    def wrapper(func):

        @wraps(func)
        def inner(self, *args, **kwargs):
            global __record__

            no_command = False
            if "__no_command__" in kwargs:
                no_command = True
                del kwargs["__no_command__"]

            result = func(self, *args, **kwargs)

            if not __record__:
                return result

            queue = CommandQueue("active")
            keys = func.__code__.co_varnames[1:]
            annotations = func.__annotations__
            annotations = typing.get_type_hints(func)

            values = args
            defaults = get_default_args(func)

            # Add self (identifying by id) to parameters
            parameters = {"id": self.id}

            # Parameters
            for key,value in zip(keys,values):
                # We change the name of the parameter to indicate it is an ID
                # This will be used later whne executing a command queue
                if isinstance(value, Object):
                    key = key + "(id)"
                parameters[key] = value

            # Named parameters
            for key,value in zip(kwargs.keys(), kwargs.values()):
                if key not in parameters.keys():
                    if isinstance(value, Object):
                        key = key + "(id)"
                    parameters[key] = value

            # Default parameters
            for key,value in defaults.items():
                if key not in parameters.keys():
                    if isinstance(value, Object):
                        key = key + "(id)"
                    parameters[key] = value

            # Check if parameter is of the right type, else, search
            # for a conversion method inside the parameter class.
            for key,value in parameters.items():
                if key in annotations.keys():

                    check = False
                    parameter_type = parameters[key].__class__
                    if "[" in parameter_type.__name__:
                        parameter_type = parameters[key].__class__.__base__

                    if get_origin(annotations[key]) is UnionType:
                        annotated_types = list(get_args(annotations[key]))
                    else:
                        annotated_types = annotations[key],

                    base_types = inspect.getmro(value.__class__)

                    for annotated_type in annotated_types:
                        # Parameter is an instance of one the annotated type
                        if (annotated_type == parameter_type or
                            isinstance(parameter_type,annotated_type) or
                            issubclass(parameter_type,annotated_type)):
                            check = True
                            break
                        elif parameter_type == types.NoneType:
                            check = True
                            break

                        # Search for possible converters in any base type
                        for base_type in base_types:
                            # Found converter, register it
                            converter = get_converter(base_type, annotated_type)
                            if converter:
                                check = True
                                # if queue._immediate:
                                # Immediate conversion
                                # parameters[key] = converter(value)
                                # else:
                                # Delayed conversion
                                parameters[key] = Converter(converter, value)

                    if check:
                        continue
                    else:
                        raise ValueError(
                            "No converter found for converting %s to %s."
                            % (parameter_type, annotated_types))

            if not no_command and not queue.readonly:
                classname = self.__class__.__name__
                methodname = func.__code__.co_name if name is None else name
                command = Command(classname, methodname, parameters, annotations)
                queue.push(command)
                log.info("%s" % command)

            return result
        return inner
    return wrapper


class CID(int):
    """
    Command unique Identification
    """

    # Identifier counter
    counter = itertools.count()

    def __new__(cls, cid=None):
        """
        Creates a new identifier unless one is provided
        """

        if cid is None:
            cid = 1 + next(CID.counter)
        else:
            cid = int(cid)
        return super(CID, cls).__new__(cls, cid)


class Command:
    """ Generic command with a unique id. """

    def __init__(self,  classname,  methodname, parameters, annotations = None):
        """ Build a new command with a unique command id (cid)

        Parameters
        ----------
        classname : string
            Name of the class
        methodname : string
            Name of the method
        parameters : dict
            Dictionnary of parameters
        annotations : dict
            Annoated type of the called method

        Examples
        --------

        ```python
        class Foo(Object):
            def __init__(self, value : int):
                self.value = value

        command = Command("Foo", "__init__", {"value" : 1})
        foo = command.execute()
        ```
        """

        self.id = CID()
        self.timestamp = datetime.timestamp(datetime.now())
        if "id" not in parameters.keys():
            raise ValueError("Parameters needs to have an id")
        self.classname = classname
        self.methodname = methodname
        self.parameters = parameters

        for key, value in parameters.items():
            if isinstance(value, Object):
                self.parameters[key] = value.id

        self.annotations = annotations


    def __str__(self):
        """
        String short representation of the command
        """

        id = self.parameters["id"]
        if (self.methodname is None or
            not len(self.methodname) or
            "." in self.methodname):
            s = "Command #%d: %s(id=%d)" % (self.id, self.classname, id)
        else:
            s = "Command #%d: %s(id=%d)/%s(…)" % (
                self.id, self.classname, id, self.methodname)
        return s


    def dump(self):
        """ Dump command onto console """

        id = self.parameters["id"]
        if (self.methodname is None or
            not len(self.methodname) or
            "." in self.methodname):
            print("#%03d: Creation of %s(id=%d)" % (self.id, self.classname, id))
        else:
            print("#%03d: %s(id=%d) → %s(…)" % (
                self.id, self.classname, id, self.methodname))
        for key,value in self.parameters.items():
            if isinstance(value, Converter):
                print("      | %s: %s (→ %s)"
                      % (key, type(value.value).__name__, value.converter.__name__))
            else:
                print("      | %s: %s"
                      % (key, type(value).__name__))


    def execute(self, globals=None, locals=None):
        """ Execute the command. """

        parameters = self.parameters.copy()
        oid = parameters["id"]
        del parameters["id"]

        # Resolve objects references
        _parameters = {}
        for key, value in parameters.items():
            if key.endswith("(id)"):
                _parameters[key[:-4]] = Object.objects[value]
            elif isinstance(value, OID):
                parameters[key] = Object.objects[value]
            elif isinstance(value, Converter):
                _parameters[key] = value()
            else:
                _parameters[key] = value
        parameters = _parameters

        # for key, value in parameters.items():
        #     if isinstance(value, OID):
        #         parameters[key] = Object.objects[value]
        #     elif isinstance(value, Converter):
        #         parameters[key] = value()

        if "." in self.methodname:
            module, name = self.methodname.split(".")
            if len(module) > 0:
                func = getattr(globals[module], name)
            else:
                func = eval(name, globals, locals)
            object = func(**parameters)
            object.id = oid
            Object.objects[oid] = object
            return object
        elif self.methodname == "__init__":
            func = eval(self.classname, globals, locals)
            object = func(**parameters)
            object.id = oid
            Object.objects[oid] = object
            return object
        else:
            name = self.methodname
            func = getattr(Object.objects[oid].__class__, name)
            return func(Object.objects[oid], **parameters)
