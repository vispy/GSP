# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import io
import sys
import json
import base64
import numpy as np
from .. object import Object
from . command import CommandQueue, Command

def default(obj):
    from .. core.types import Color

    if isinstance(obj, memoryview):
        return base64.b64encode(bytes(obj)).decode()
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode()
    elif isinstance(obj, np.dtype):
        return str(obj)
    elif isinstance(obj, np.ndarray):
        return base64.b64encode(obj).decode()
    elif isinstance(obj, Color):
        return tuple(obj._color.tolist())
    elif isinstance(obj, Object):
        return obj.id
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def dump_command(command, stream=sys.stdout):
    """ Dump a command to given stream in json format """

    # Convert parameters if necessary
    parameters = {}
    for key,value in command.parameters.items():
        if callable(value):
            value = value()
        if isinstance(value, Object):
            parameters[key+"(id)"] = value.id
        else:
            parameters[key] = value

    # Check which method has been called
    if (command.methodname is None or not len(command.methodname)):
        method = command.classname
    elif "." in command.methodname:
        method = command.methodname
    else:
        method = "%s/%s" % (command.classname, command.methodname)

    payload = { "method" : method,
                "id" : int(command.id),
                "timestamp" : command.timestamp,
                "parameters" : parameters }
    if stream == sys.stdout:
        print(payload)
    else:
        return payload

def dump(queue=None, filename=None):
    """ Save command queue to a file """

    queue = queue or CommandQueue("active")
    commands = []
    for command in queue.commands:
        commands.append(dump_command(command, stream=None))
    payload = { "jsonrpc": "2.0", "commands" : commands }

    if filename is None:
        return json.dumps(payload, indent=2, default=default)
    else:
        with open(filename, "w") as stream:
            json.dump(payload, stream, default=default)


def save(filename, queue = None ):
    """ Save command queue to a file """

    queue = queue or CommandQueue("active")
    dump(queue, filename)


def load(filename, queue = None):
    """ Load commands from JSON file into the default command queue """

    with open(filename) as stream:
        commands = json.load(stream)["commands"]

    # Get default command queue
    queue = queue or CommandQueue("active")
    queue.empty()

    for command in commands:
        method = command["method"]
        try:
            classname, methodname = method.split("/")
        except ValueError:
            classname, methodname = method, "__init__"
        parameters = command["parameters"]
        command = Command(classname,  methodname, parameters)
        queue.push(command)

    return queue
