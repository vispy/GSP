# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
This example illustrates how to use the gsp.io machinery to write
a new GSP backend. To do so, each new class needs to inherit from the
Object class and then, each method that has a command decorator, will
lead to the creation of a Command when called. This command will be
recorded to the default command queue.

If the method is called with a parameter whose type does not
correspond to the documented one, it is possible to register a
converter that will be used when needed. In this example, the creation
method requires an integer as parameter but when called with float, it
is actually registered to be later converted using the provided
converter (float_to_int). This conversion occurs just-in-time (when
needed).

Once several of commands have been recorded, it is possible to
re-execute them or to save them on a file. Finally, it is also
possible to load them and run them.

Keywords: command, queue, yaml, json
"""

import os

from gsp import Object
from gsp.log import log
from gsp.io import json
from gsp.io.convert import register
from gsp.io.command import Command, CommandQueue, command

@register("float", "int")
def float_to_int(value):
    return int(value)

class Foo(Object):

    @command()
    def __init__(self, value : int):
        Object.__init__(self)
        self.value = value

    @command()
    def update(self):
        self.value = self.value + 1

    def __repr__(self):
        return f"Foo(id={self.id}, value={self.value})"


print(f"—————{__doc__}—————\n")

# Client
print("1. Commands creation")
queue = CommandQueue()
foo = Foo(123.0)
foo.update()
print(foo)

# Server
print()
print("2. Commands execution")
Object.objects = {}
for command in queue:
    command.dump()
queue.run(globals(), locals())
print(Object.objects[1])

print()
print("3. Commands load & execution")

__dirname__ = os.path.dirname(os.path.abspath(__file__))
json_path = f"{__dirname__}/output/foo.json"
json.save(json_path, queue)

Object.objects = {}
queue = json.load(json_path)
for command in queue:
    log.info("%s" % command)

queue.run(globals(), locals())
print(Object.objects[1])
print()
