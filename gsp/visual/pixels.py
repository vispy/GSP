# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union, TypeAlias

Color = list[float,float,float,float]

from gsp.core.object import Object
from gsp.core.command import command
from gsp.core.buffer import Buffer

class Pixels(Object):

    @typechecked
    @command("")
    def __init__(self, positions: Buffer,
                       colors   : Union[Buffer, Transform, Color]):

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
        self.vertices = vertices
        self.colors = colors
        self.transform = transform
