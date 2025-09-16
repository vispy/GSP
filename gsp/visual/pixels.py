# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import Buffer, Color
from gsp.transform import Transform
from gsp.io.command import command

class Pixels(Visual):
    """
    Pixels are the smallest entities that can be rendered on
    screen (pixel or fragment) or on paper (dot). They can be colored
    but have no dimension and correspond to the true mathematical
    notion of a point.

    ??? note "IN/OUT variables "
        ```glsl

        // Rendering stage 1
        in uniform vec4 viewport;               // in("viewport")
        in attribute [ vec2 | vec3 ] positions; // in("positions")
        in [ attribute | uniform ] vec4 colors; // in("colors")

        // Rendering stage 2
        out attribute vec3 screen;              // out("screen[positions]")

        // Rendering stage 3
        out attribute vec4 colors;              // out("colors")
        ```

    ```bash exec="1"
    python docs/snippets/Pixels_init.py
    ```
    """

    @command("visual.Pixels")
    def __init__(self, positions : Transform | Buffer,
                       colors : Transform | Buffer | Color):
        """
        Create a Pixels visual at given positions and given
        colors. If positions is a transform, it is first evaluated and
        produce the "screen" and "depth" buffers. If the type of
        positions is vec2, the z coordinate of all pixels is set to
        the default z coordinate (0). If colors is a transform, it is
        first evaluated and produce the "colors" buffer.

        Parameters
        ----------
        positions:
            Pixel positions (vec3 or vec2)
        colors:
            Pixel colors (vec4)
        """

        super().__init__()

        # These variables are available prior to rendering
        self._in_variables = {
            "positions" : positions,
            "colors" : colors,
            "viewport" : None,
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        n = len(positions)
        self._out_variables = {
            "screen[positions]" : np.empty((n,3), np.float32),
        }
