# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference import (Object, command)
from gsp.backend.reference.core.buffer import Buffer
from gsp.backend.reference.core.viewport import Viewport
from gsp.backend.reference.transform import Transform

class Pixels(Object):

    @command("")
    def __init__(self, viewport : Viewport,
                       positions: Buffer,
                       colors   : Buffer):

        """
        Set of pixels specified as positions and colors
        

        Parameters:

         positions:
        
            Position(s) as (x,y,z)

         colors:
        
            Color(s)  as (r,g,b,a).

        **Note**

          - Color corresponds to a list of 4 floats
        """
        
        Object.__init__(self)
        self.viewport = viewport
        self.positions = positions
        self.colors = colors

    @command("render")
    def render(self, transform: Transform):

        """
        Render the visual using given transform.
        

        Parameters:

         transform:
        
            Transform to be applied to position(s)
        """
        
        pass
