# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 VisPy development team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.transform import transform

class Mat4x4(transform.Transform):

    @command("transform.Mat4x4")
    def __init__(self,
                 data : bytes):
        """A matrix transform corresponds to a 4x4 matrix that can be
        applied to a Buffer with homogenous coordinates (4 floats).

        Parameters:

         data:
        
            Content of the matrix as 16 floats.
        """

        Object.__init__(self)
        self._buffer = (1, "f::16", data)
