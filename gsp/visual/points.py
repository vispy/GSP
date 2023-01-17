# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union, List

from gsp.core.object import Object
from gsp.core.command import command
from gsp.core.buffer import Buffer



class Points(Object):

    @command("")
    def __init__(self,
                 position : Buffer,
                 size : Union[Buffer, float], 
                 fill_color : Union[Buffer, List[float]],
                 stroke_color : Union[Buffer, List[float]],
                 stroke_width : Union[Buffer, float]):

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

