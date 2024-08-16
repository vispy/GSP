# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

from . log import log
from . object import Object

from . import core
from . import visual
from . import transform

def use(backend):
    """
    Specify a backend to use by importing core, transform and
    visual modules into global namespace.
    """

    import inspect

    if backend == "matplotlib":
        from . import transform
        from . matplotlib import core
        from . matplotlib import visual
        import matplotlib.pyplot as plt
        inspect.stack()[1][0].f_globals["plt"] = plt

    else:
        from . import core
        from . import transform

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
    from gsp.io import json
    from gsp.io.command import CommandQueue

    Object.objects = {}
    queue = CommandQueue.get_default()
    queue.empty()

    format = format or pathlib.Path(filename).suffix[1:]
    if format in ["json"]:
        json.load(filename)
    else:
        raise ValueError(f"Unknown format ({format})")

    return queue
