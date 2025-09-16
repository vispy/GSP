# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
This example shows how an object can derive from an instrumented
class with different parameter types with registered converters. This
example is mostly targeted at people who want to develop their own
backend.

Note the difference between the print call that displays a float value
(no conversion) versus the yamld dump where parameter has been
converted just in time.

Keywords: io, command, inheritance
"""
from gsp.object import Object
from gsp.io import json
from gsp.io.command import command, register

class Foo(Object):
    """Foo documentation"""

    @command()
    def __init__(self, value : int):
        """Foo creation """
        Object.__init__(self)
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, value={self.value})"

@register("float", "int")
def float_to_int(value):
    return int(value)

class Bar(Foo):
    """Bar documentation"""

    def __init__(self, value : float):
        Foo.__init__(self, value)


bar = Bar(123.0)
print(bar)
print(json.dump())
