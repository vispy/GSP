# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
The Canvas corresponds to a finite two-dimensional drawing area.
"""
from typing import Union
from gsp.core.command import command
from gsp.core.object import Object, OID

class Canvas(Object):
    """ """
        
    @command("")
    def __init__(self, width :     int, 
                       height :    int,
                       dpi :       float):
        """A Canvas is a two-dimensional drawing area of size `width`
        × `height` pixels using specified `dpi` ([dots per
        inch][dpi]).

        [dpi]: https://en.wikipedia.org/wiki/Dots_per_inch
        
        Parameters:

          width:
        
            Width of the drawing area in pixels.

          height:
        
            Height of the drawing area in pixels.

          dpi:
            Dots per inch

        **Note**

        - A canvas uses a [standard color space][srgb] with at least 8
         bits per channel.

        - The `(0,0)` coordinates corresponds to the bottom left corner.

        - A (typographical) [point][point] is 1/72 inch.

        [srgb]: https://en.wikipedia.org/wiki/SRGB
        [point]: https://en.wikipedia.org/wiki/Point_(typography)

        """
        
        Object.__init__(self)
        self.width = width
        self.height = height
        self.dpi = dpi
