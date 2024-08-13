# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

from . log import log
from . object import Object

from . import core
from . import transform


def use(backend):
    if backend == "matplotlib":
        from . matplotlib import core
        from . import transform
    else:
        from . import core
        from . import transform

    import inspect
    inspect.stack()[1][0].f_globals["core"] = core
    inspect.stack()[1][0].f_globals["transform"] = transform
