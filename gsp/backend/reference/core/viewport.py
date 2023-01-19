# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core.canvas import Canvas

class Viewport(Object):

    @command("core.Viewport")
    def __init__(self, canvas : Canvas,
                       x :      int,
                       y :      int,
                       width :  int,
                       height : int):
        """A viewport is a rectangular two-dimensional surface from a
        canvas, located at (x, y) coordinates (bottom left corner)
        with size equal to width×height pixels.
        
        Parameters:

          canvas:
        
            Canvas where to create the viewport

          x:
        
            X coordinate of the viewport bottom left corner
        
          y:
        
            Y coordinate of the viewport bottom left corner
        
          width:

            Width of the viewport in pixels.
        
          height:

            Height of the viewport in pixels.

        **Note**

        - Future implementation will allows viewports to have an
          arbitrary rotation.

        """
        
        Object.__init__(self)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    
