# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

from . log import log
from . object import Object

from . import io
from . import core
from . import visual
from . import transform

# minimal version of python is 3.11 - check it is respected. if not, then exit with an error message
import sys
if sys.version_info < (3, 11):
    print("Python 3.11 or higher is required.")
    sys.exit(1)

@io.register("str", "memoryview")
def str_to_memoryview(obj):
    return memoryview(bytes(obj))

@io.register("list", "Color")
def list_to_Color(obj):
    return core.Color(*obj)

@io.register("tuple", "Color")
def tuple_to_Color(obj):
    return core.Color(*obj)

@io.register("Color", "list")
def Color_to_list(obj):
    return obj._color.tolist()

@io.register("Color", "tuple")
def Color_to_tuple(obj):
    return tuple(obj._color.tolist())

@io.register("list", "tuple")
def list_to_tuple(obj):
    return tuple(obj)

@io.register("tuple", "list")
def tuple_to_list(obj):
    return list(obj)

@io.register("int", "Canvas")
def int_to_Object(obj):
    return Object.objects[obj]


# Some default coloes
black = [0.0, 0.0, 0.0, 1.0]
grey  = [0.5, 0.5, 0.5, 1.0]
white = [1.0, 1.0, 1.0, 1.0]

def use(backend):
    """
    Specify a backend to use by importing core, transform and
    visual modules into global namespace.
    """

    import inspect
    import numpy as np
    from . import transform

    if backend == "matplotlib":
        from . import transform
        from gsp_matplotlib import glm
        from gsp_matplotlib import core
        from gsp_matplotlib import visual
        import matplotlib.pyplot as plt
        inspect.stack()[1][0].f_globals["glm"] = glm
        inspect.stack()[1][0].f_globals["plt"] = plt
    else:
        from . import core

    inspect.stack()[1][0].f_globals["np"] = np
    inspect.stack()[1][0].f_globals["core"] = core
    inspect.stack()[1][0].f_globals["transform"] = transform
    inspect.stack()[1][0].f_globals["visual"] = visual


def save(filename, format=None):
    """
    Save default command stack into a file. If format is not
    specified, it is deduced from filename exension.
    """

    import pathlib
    from gsp.io import json
    from gsp.io.command import CommandQueue

    format = format or pathlib.Path(filename).suffix[1:]
    if format in ["json"]:
        json.save(filename)
    else:
        raise ValueError(f"Unknown format ({format})")

def load(filename, format=None):
    """
    Reset the current default stack and populate it with commands from
    the given filename. If format is not specified, it is deduced from
    filename exension.
    """

    import pathlib
    from gsp.io import queue, json

    Object.objects = {}
    queue = queue("active").empty()

    format = format or pathlib.Path(filename).suffix[1:]
    if format in ["json"]:
        json.load(filename)
    else:
        raise ValueError(f"Unknown format ({format})")

    return queue
