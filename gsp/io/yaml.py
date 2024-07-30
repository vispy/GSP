# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import io
import sys
import yaml
from .. object import Object, OID
from . command import CommandQueue, Command, Converter, CID

def dump_command(command, stream=sys.stdout):
    """ Dump a command to a given stream in yaml format """

    # Convert parameters if necessary
    parameters = {}
    for key,value in command.parameters.items():
        if isinstance(value, Converter):
            parameters[key] = value()
            if isinstance(parameters[key], Object):
                parameters[key] = parameters[key].id
        else:
            parameters[key] = value

    # Check which method has been called
    if (command.methodname is None or not len(command.methodname)):
        method = command.classname
    elif "." in command.methodname:
        method = command.methodname
    else:
        method = "%s/%s" % (command.classname, command.methodname)

    data = [ { "method" : method,
               "cid" : command.id,
               "timestamp" : command.timestamp,
               "parameters" : parameters } ]

    yaml.dump(data, stream, default_flow_style=None, sort_keys=False)

def dump(queue=None, filename=None):
    """Dump command queue to a file if filename has been provided, else
    return it as a string"""

    queue = queue or CommandQueue.get_default()

    if filename is None:
        stream = io.StringIO()
        for command in queue._commands:
            dump_command(command, stream)
        return stream.getvalue()
    else:
        with open(filename, "w") as stream:
            for command in queue._commands:
                dump_command(command, stream)


def save(queue, filename):
    """ Save command queue to a file """

    dump(queue, filename)


def load(filename):
    """ Load commands from file into the default command queue """

    with open(filename) as stream:
        try:
            commands = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

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


def CID_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:int', str(data))
yaml.add_representer(CID, CID_representer)

def OID_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:int', str(data))
yaml.add_representer(OID, OID_representer)
