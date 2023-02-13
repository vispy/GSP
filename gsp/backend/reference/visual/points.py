# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core.buffer import Buffer
from gsp.backend.reference.core.viewport import Viewport
from gsp.backend.reference.transform import Transform
from gsp.backend.reference.transform import Mat4x4
from gsp.backend.reference.core.size import Size
from gsp.backend.reference.core.color import Color

class Points(Object):

    @command("visual.Points")
    def __init__(self,
                 viewport :    Viewport,
                 positions :   Union[Buffer, Transform],
                 sizes :       Union[Buffer, Transform, Size, float],
                 fill_colors : Union[Buffer, Transform, Color],
                 edge_colors : Union[Buffer, Transform, Color],
                 edge_widths : Union[Buffer, Transform, Size, float]):

        """A set of pixels.

        Parameters:

         positions:
        
           Position of points (pixels)

         sizes:
        
           Diameter of points (pixels)

         fill_colors:
        
           Fill colors (red, green, blue, alpha)
        
         edge_colors:
        
           Edge colors (red, green, blue, alpha)
        
         edge_widths:
        
           Edge widths (pixels)

        """
        
        Object.__init__(self)
        self._positions = positions
        self._sizes = sizes
        self._fill_colors = fill_colors
        self._edge_colors = edge_colors
        self._edge_widths = edge_widths

    @command("render")
    def render(self, transform : Mat4x4):
        pass
