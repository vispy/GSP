# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command

class Color(Object):
    
    @command("core.Color")
    def __init__(self, red : float,
                       green : float,
                       blue : float,
                       alpha : float):

        """Representation of a color in the [sRGB] colorspace.

           [sRGB]: https://en.wikipedia.org/wiki/sRGB
        
        Parameters:

         red:
        
            Normalized value for the red channel

         green:
        
            Normalized value for the green channel

         blue:
        
            Normalized value for the blue channel

         alpha:
        
            Normalized value for he alpha channel.

            (0.0 means fully transparent, 1.0 means fully opaque)
        """
        
        Object.__init__(self)
        self.color = red, green, blue, alpha

