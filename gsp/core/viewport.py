# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp import Object
from gsp.io.command import command
from gsp.core.canvas import Canvas

class Viewport(Object):
    """
    A viewport is a rectangular two-dimensional surface from a
    canvas, located at (x, y) coordinates (bottom left corner) with
    size equal to width×height pixels and a background color.

    !!! Notes

        Future implementation will allows viewports to have an
        arbitrary rotation.

    ```python exec="yes"
    from gsp.io import mkdocs
    mkdocs(print,
    '''
    from gsp.core import Canvas, Viewport
    canvas = Canvas(512, 512, 100.0)
    viewport = Viewport(canvas, 0, 0, 512, 512, (0,0,0,1))
    ''')
    ```
    """

    @command("core.Viewport")
    def __init__(self, canvas : Canvas,
                       x : int,
                       y : int,
                       width : int,
                       height : int,
                       color : tuple):
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
        color: Color
            Background color of the viewport
        """

        Object.__init__(self)


    @command()
    def render(self, target : str):
        """
        Render the viewport to the specified target. If no target is
        specified, return a raw image as bytes.

        ```python exec="yes"
        from gsp.io import mkdocs
        mkdocs(print,
        '''
        from gsp.core import Canvas, Viewport
        canvas = Canvas(512, 512, 100.0)
        viewport = Viewport(canvas, 0, 0, 512, 512, (0,0,0,1))
        viewport.render("png")
        ''')
        ```

        Parameters
        ----------
        target:
            Filename of the target
        """
        pass
