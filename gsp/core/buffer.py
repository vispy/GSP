# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from __future__ import annotations # Solve circular references with typing

import numpy as np
from gsp import Object
from . data import Data
from gsp.io.command import command, register


class Buffer(Object):

    """
    Buffer represents a structured view on some Data or
    Buffer. Buffer can be a partial or whole view on the underlying
    source.
    """

    @command("core.Buffer")
    def __init__(self, count : int,
                       dtype : np.dtype,
                       data : memoryview | bytes = None):
        """
        Create a new Buffer.

        Parameters
        ----------
        count:
            Number of item
        dtype:
            Type of the item
        data:
            Content of of the buffer
        """
        Object.__init__(self)
        self._count = count
        self._dtype = dtype
        self._data = data

    @command()
    def set_data(self, offset : int,
                       data : memoryview):

        """Update buffer content at given offset with new data.

        Parameters
        ----------
        offset :
            Offset in bytes where to start update
        data :
            Content to update with.
        """
        pass

    def __len__(self):
        return self._count
