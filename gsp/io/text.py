# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
import io
import sys
from datetime import datetime
from .. object import Object, OID
from . command import CommandQueue, Command, Converter, CID

def bold(s): return s
def dim(s): return s

def dump_command(command, stream=sys.stdout):
    """
    Dump a command to given stream in text (ansi) format

    This is mostly useful for the documentatipn where the TEXT tab of
    any commands can be dumped via markdow-exec.
    """

    s = ""

    # Get timestamp in date format
    date = datetime.fromtimestamp(command.timestamp)

    # Check which method has been called
    if (command.methodname is None or not len(command.methodname)):
        method = command.classname
    elif "." in command.methodname:
        method = command.methodname
    else:
        method = "%s/%s" % (command.classname, command.methodname)
    s += dim("%d. " % command.id) + bold("COMMAND\n")
    # s += "%d. " % command.id + bold("COMMAND:") + ' "%s" (str)\n' % (method)
    s += '     - METHOD: "%s"' % (method) + dim(" (str)\n")
    s += "     - COMMAND_ID: %s" % command.id + dim(" (int)\n")
    s += "     - TIMESTAMP: %s" % date.strftime("%Y-%m-%dT%H:%M:%S.%f") + dim(" (datetime)\n")
    s += dim("   PARAMETERS\n")
    for key,value in command.parameters.items():

        # Immediate conversion for lisibility in the documentation
        if isinstance(value, Converter):
            value = str(value()) + " (converted)"

        if key == "id":
            s += "     - OBJECT_ID: %s" % value + dim(" (int)\n")
        else:
            vtype = command.annotations[key]
            if hasattr(vtype, "__name__"):
                vtype = vtype.__name__
            else:
                vtype = str(vtype)
            s +="     - %s: %s" % (key.upper(), value)
            s += dim(" (%s)\n" % (vtype))

    if stream == sys.stdout:
        print(s)
    else:
        return s

def dump(queue=None, filename=None):
    """ Save command queue to a file """

    queue = queue or CommandQueue.get_default()
    commands = ""
    for command in queue._commands:
        commands += dump_command(command, stream=None)
        commands += "\n"

    if filename is None:
        return commands
    else:
        with open(filename, "w") as stream:
            stream.write(commands)

def save(queue, filename):
    """ Save command queue to a file """

    dump(queue, filename)


def load(filename):
    """ Load commands from JSON file into the default command queue """

    raise NotImplemented
