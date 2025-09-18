# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from __future__ import annotations # Solve circular references with typing
import numpy as np
from gsp.io.command import command, register

from gsp import core

class List(core.List):

    __doc__ = core.List.__doc__

    @command("core.List")
    def __init__(self, data : Buffer,
                       itemsizes : Buffer | int):
        super().__init__(data, itemsizes, __no_command__ = True)

    def __array__(self):
        return self._data.__array__()

    def __repr__(self):
        return f"List({len(self)}, {self._data._dtype})"
