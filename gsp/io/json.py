# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import io
import sys
import json
import base64
from .. object import Object, OID
from . command import CommandQueue, Command, Converter, CID


def default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode()

    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def dump_command(command, stream=sys.stdout):
    """ Dump a command to given stream in json format """

    # Convert parameters if necessary
    parameters = {}
    for key,value in command.parameters.items():
        if callable(value):
            parameters[key] = value()
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

    queue = queue or CommandQueue.get_default()
    commands = []
    for command in queue._commands:
        commands.append(dump_command(command, stream=None))
    payload = { "jsonrpc": "2.0", "commands" : commands }

    if filename is None:
        return json.dumps(payload, indent=2, default=default)
    else:
        with open(filename, "w") as stream:
            json.dump(payload, stream, default=default)


def save(queue, filename):
    """ Save command queue to a file """

    dump(queue, filename)


def load(filename):
    """ Load commands from JSON file into the default command queue """

    with open(filename) as stream:
        commands = json.load(stream)["commands"]

    # Get default command queue
    queue = CommandQueue.get_default()
    queue.empty()

    for command in commands:
        method = command["method"]
        classname, methodname = method.split("/")
        parameters = command["parameters"]
        command = Command(classname,  methodname, parameters)
        queue.push(command)

    return queue
