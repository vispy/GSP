# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core.buffer import Buffer
from gsp.backend.reference.core.viewport import Viewport
from gsp.backend.reference.transform import Transform

class Points(Object):

    @command("")
    def __init__(self,
                 viewport : Viewport,
                 position : Buffer,
                 size : float,
                 fill_color : Buffer,
                 stroke_color : Buffer,
                 stroke_width : float):

        """A set of pixels.

        Parameters:

         position:
        
           Position of the point (pixels)

         size:
        
           Diameter of the point (pixels)

         fill_color:
        
           Fill color (red, green, blue, alpha)
        
         stroke_color:
        
           Stroke color (red, green, blue, alpha)
        
         stroke_width:
        
           Stroke width (pixels)


        **Note**

          - Color corresponds to a list of 4 floats

        """
        
        Object.__init__(self)
        self.position = position
        self.size = size
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    @command("render")
    def render(self,
               transform : Transform):
        pass
