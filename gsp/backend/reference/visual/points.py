# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core.buffer import Buffer

class Points(Object):

    @command("")
    def __init__(self,
                 position : Buffer,
                 size : Buffer,
                 fill_color : Buffer,
                 stroke_color : Buffer,
                 stroke_width : Buffer):

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
        self.fill_color = fill
        self.stroke_color = stroke
        self.stroke_width = stroke_width

