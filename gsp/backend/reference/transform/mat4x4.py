# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 VisPy development team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core import Datatype

class Mat4x4(Object):

    datatype = Datatype("f::16")
    """[Datatype][gsp.core.Datatype] for the underlying
    [buffer][gsp.core.Buffer] hlding the matrix. This correspond to a
    4x4 matrix of 32 bits float.
    """
    
    @command("")
    def __init__(self,
                 data : bytes):
        """A matrix transform corresponds to a 4x4 matrix that can be
        applied to a Buffer with homogenous coordinates (4 floats).

        Parameters:

         data:
        
            Content of the matrix as 16 floats.
        """

        Object.__init__(self)
        self.buffer = (1, self.datatype, data)
