# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
import pytest
from gsp import Object
from gsp.io.convert import register, unregister
from gsp.io.command import command, Command, CommandQueue

class Foo(Object):
    @command()
    def __init__(self, value : int):
        Object.__init__(self)
        self.value = value

class Bar(Foo):
    def __init__(self, value : float):
        Foo.__init__(self, value)

def test_io_recording():
    """ Test if commands are recorded """

    Object.objects = {}
    queue = CommandQueue("active")
    queue.readonly = False

    Foo(1), Foo(2), Foo(3)
    assert(len(Object.objects) == 3)
    assert(len(queue) == 3)

def test_io_no_recording():
    """ Test if commands are not recorded """

    Object.objects = {}
    queue = CommandQueue("active").empty()
    queue.readonly = True

    Foo(1), Foo(2), Foo(3)
    assert(len(Object.objects) == 3)
    assert(len(queue) == 0)


def test_io_queue_execution():
    """ Test if commands can be executed """

    Object.objects = {}
    queue = CommandQueue()
    queue.readonly = False

    foo = Foo(123)
    queue.run(globals(), locals())
    foo = Object.objects[foo.id]
    assert (foo.value == 123)

def test_io_type_checking():
    """ Test if type checking raises an exception """

    with pytest.raises(ValueError):
        foo = Foo(123.0)

def test_conversion():
    """ Test if type is converted """

    @register("float", "int")
    def float_to_int(value):
        return int(value) + 1

    queue = CommandQueue("active").empty()
    queue.readonly = False

    foo = Foo(123.0)
    Object.objects = {}
    queue.run(globals(), locals())
    foo = Object.objects[foo.id]
    assert foo.value == 124

def test_conversion_registered():
    """ Test if conversion has been already registered """

    with pytest.raises(TypeError):
        @register("float", "int")
        def float_to_int(value):
            return int(value)

def test_conversion_unregister():
    """ Test if a conversion can be unregistered """

    unregister("float", "int")
    @register("float", "int")
    def float_to_int(value):
        return int(value)

def test_io_to_json():
    """ Test export to JSON """

    import io
    import json
    import gsp.io.json

    unregister("float", "int")

    @register("float", "int")
    def float_to_int(value):
        return 4*int(value)

    queue = CommandQueue("test").empty()
    queue.readonly = False

    foo = Foo(123.0)
    result = gsp.io.json.dump(queue)
    commands = json.loads(result)["commands"][0]

    assert commands["method"] == "Foo/__init__"
    assert commands["parameters"]["value"] == 123*4


def test_io_inheritance():
    """ Test if commands are recorded """

    unregister("float", "int")

    @register("float", "int")
    def float_to_int(value):
        return int(value)

    queue = CommandQueue("active").empty()
    queue.readonly = False

    bar = Bar(123.0)
    Object.objects = {}
    queue.run(globals(), locals())
    barload = Object.objects[bar.id]

    assert isinstance(bar.value, float)
    assert isinstance(barload.value, int)
