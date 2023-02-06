# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 VisPy development team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.transform.transform import Transform

class Depth(Transform):
    
    @command("transform.Depth")
    def __init__(self):
        """A depth transform is a JIT transform whose output is
        computed when a visual is rendered. For a visual with n
        vertices, the output is a Buffer of n floats containing the
        depth coordinate of each vertices.
        """
        
        Transform.__init__(self,
                           __no_command__ = True)

