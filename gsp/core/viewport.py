# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp import Object
from gsp.io.command import command
from gsp.core.canvas import Canvas
from gsp.core.types import Color

class Viewport(Object):
    """
    A viewport is a rectangular two-dimensional surface from a
    canvas, located at (x, y) coordinates (bottom left corner) with
    size equal to width×height pixels and a background color.

    !!! Notes

        Future implementation will allows viewports to have an
        arbitrary rotation.

    ```bash exec="1"
    python docs/snippets/Viewport_init.py
    ```
    """

    @command("core.Viewport")
    def __init__(self, canvas : Canvas,
                       x : int,
                       y : int,
                       width : int,
                       height : int,
                       color : Color | list | tuple):
        """
        A viewport is a rectangular two-dimensional surface.

        Parameters
        ----------

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
        color:
            Background color of the viewport
        """

        Object.__init__(self)


    @command()
    def render(self, target : str):
        """
        Render the viewport to the specified target. If no target is
        specified, return a raw image as bytes.

        ```bash
        python docs/snippets/Viewport_render.py
        ```

        Parameters
        ----------
        target:
            Filename of the target
        """
        pass
