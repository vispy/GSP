# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

import numpy as np
from gsp import glm
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

    IN variables (client & server side):
     - positions (vec2 or vec3)
     - colors (vec3 or vec4)

    OUT variables (server side):
     - screen[positions] (vec2)
     - depth[positions] (float)
    """

    @command("visual.Pixels")
    def __init__(self, positions : Transform | Buffer,
                       colors : Transform | Buffer | Color):
        """
        Create a visual of n pixels at given positions with given
        colors.

        Parameters
        ----------
        positions:
            Pixel positions (vec3)
        colors:
            Pixel colors (vec4)
        """

        super().__init__()

        n = len(positions)

        self._in_variables = {
            "positions" : positions,
            "colors" : colors,
            "viewport" : None,
        }

        # These variables exists nonly during rendering and are
        # available on server side only.
        self._out_variables = {
            "screen[positions]" : np.empty((n,3), np.float32),
            "depth[positions]" : np.empty(n, np.float32)
        }
