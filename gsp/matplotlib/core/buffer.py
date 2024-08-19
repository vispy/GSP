# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from __future__ import annotations # Solve circular references with typing
import numpy as np
from gsp.io.command import command, register

from gsp import core

class Buffer(core.Buffer):

    __doc__ = core.Viewport.__doc__

    @command("core.Buffer")
    def __init__(self, count : int,
                       dtype : np.dtype,
                       data : memoryview | bytes = None):
        super().__init__(count, dtype, data, __no_command__ = True)
        self._count = count
        self._dtype = dtype
        self._data = data
        self._array = None

    @command()
    def set_data(self, offset : int,
                       data : memoryview | bytes):
        # Be careful with set_data when the underlying data is already tracked
        # buffer = np.asanyarray(self).view(np.ubyte)
        # buffer[offset:offset+len(data)] = np.frombuffer(data, np.ubyte)
        pass

    def __array__(self):
        if self._array is None:
            if self._data is not None:
                self._array = np.frombuffer(self._data, self._dtype)
            else:
                self._array = np.empty(self._count, self._dtype)
        return self._array

    def __repr__(self):
        return f"Buffer({self._count}, {self._dtype})"
