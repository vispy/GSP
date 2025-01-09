# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

from gsp import Object
from gsp.io.command import command

class Canvas(Object):
    """
    A Canvas is a two-dimensional drawing area of size
    width × height pixels using the specified dpi (dots per
    inch).

    ???+ info Note

        - A canvas uses a standard color space with at least 8 bits per channel.
        - Blending mode is alpha blending
        - The `(0,0)` coordinates corresponds to the bottom left corner.
        - A typographical point is 1/72 inch.



    ```bash exec="1"
    python docs/snippets/Canvas_init.py
    ```
    """

    @command("core.Canvas")
    def __init__(self, width : int,
                       height : int,
                       dpi : float):
        """
        Create a new Canvas

        Parameters
        ----------
        width:
            Width of the drawing area in pixels.
        height:
            Height of the drawing area in pixels.
        dpi:
            Dots per inch
        """
        Object.__init__(self)


    @command("render")
    def render(self, target : str):
        """
        Render the canvas the to specified target. If no target is
        specified, return a raw image as bytes.

        ```bash
        python docs/snippets/Canvas_render.py
        ```

        Parameters
        ----------
        target:
            Filename of the target
        """
        pass
