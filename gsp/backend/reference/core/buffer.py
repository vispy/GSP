# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core.datatype import Datatype

class Buffer(Object):
    
    @command("core.Buffer")
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

    @command()
    def set_data(self, offset: int,
                       data : bytes):

        """Update buffer content at given offset with new data.
        
        Parameters:

         offset:
        
            Offset in bytes where to start update

         data:
        
            Content to update with.
        """
        pass
