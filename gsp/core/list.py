# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from __future__ import annotations # Solve circular references with typing

import numpy as np
from gsp.object import Object
from . data import Data
from . buffer import Buffer
from gsp.io.command import command, register

class List(Object):

    """A List represents a partitioned Buffer with elements of
    (possibly) different sizes. It is created using a regular data
    Buffer (any type) and a second item Buffer (integer type) whose
    size correspond to the number of elements and whose content
    describes the size of each. Elements are made of consecutive
    data in the data Buffer.
    """

    @command("core.List")
    def __init__(self, data : Buffer,
                       itemsizes : Buffer | int):
        """
        Create a new List

        Parameters
        ----------
        buffer:
            Buffer to be consider
        partition:
            Partition of the buffer
        """
        Object.__init__(self)
        self._data = data
        self._itemsizes = itemsizes

        
    def __len__(self):
        """ Return the number of items in the list """
        
        if isinstance(self._itemsizes, (int)):
            return len(data) / self._itemsizes
        else:
            return len(self._itemsizes)
        

