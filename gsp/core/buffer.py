# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union
from typeguard import typechecked

from gsp.core.object import Object
from gsp.core.command import command
from gsp.core.datatype import Datatype

class Buffer(Object):

    # Convenience method, not part of the protocol
    @classmethod
    def from_numpy(cls, Z):
        import numpy as np
        
        if (isinstance(Z, np.ndarray)):
            return Buffer(Z.size, Datatype.from_numpy(Z.dtype), Z.tobytes())
        raise ValueError(f"Unknown type for {Z}, cannot convert to Buffer")

    
    @command("core.Buffer")
#             converters = {"datatype" : [Datatype.from_numpy],
#                           "data"     : [Buffer.from_numpy]})
    def __init__(self, count : int,
                       datatype : Datatype,
                       data  : bytes):

        """Uni-dimensional buffer with `count` elements of type
        `dtype` with content equal to `data`.
        
        Parameters:

         count:
        
            Number of elements

         datatype:
        
            Element datatype

         data:
        
            Content of the buffer
        """
        
        Object.__init__(self)
        self.count = count
        self.datatype = datatype
        self.data = data
