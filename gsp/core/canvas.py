# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
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

    ```python exec="yes"
    from gsp.io import mkdocs
    mkdocs(print,
    '''
    from gsp.core.canvas import Canvas
    canvas = Canvas(512, 512, 100.0)
    ''')
    ```
    """

    @command("core.Canvas")
    def __init__(self, width : int = 512,
                       height : int = 512,
                       dpi : float = 100.0):
        """
        Create a new Canvas

        Parameters
        ----------

        width : int

            Width of the drawing area in pixels.

        height : int

            Height of the drawing area in pixels.

        dpi : float

            Dots per inch

        """
        Object.__init__(self)


    @command("render")
    def render(self, target : str = None):
        """
        Render the canvas the to specified target. If no target is
        specified, return a raw image as bytes.

        ```python exec="yes"
        from gsp.io import mkdocs
        mkdocs(print,
        '''
        from gsp.core.canvas import Canvas
        canvas = Canvas(512, 512, 100.0)
        canvas.render("png")
        ''')
        ```

        Parameters
        ----------

        target : str
            Filename of the target
        """
        pass
