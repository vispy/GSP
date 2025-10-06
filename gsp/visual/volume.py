# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import Buffer, Color
from gsp.transform import Transform
from gsp.io.command import command


class Volume(Visual):
    """
    A volume is a three-dimensional shape composed of a set of voxels.
    """

    @command("visual.Volume")
    def __init__(
        self,
        positions: Transform | Buffer,
        sizes: Transform | Buffer | float,
        fill_colors: Transform | Buffer | Color,
    ):
        super().__init__()

        # These variables are available prior to rendering and may be
        # tracked
        self._in_variables = {
            "positions": positions,
            "fill_colors": fill_colors,
            "sizes": sizes,
            "viewport": None,
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        n = len(positions)
        self._out_variables = {
            "screen[positions]": np.empty((n, 3), np.float32),
            "fill_colors": np.empty((n, 4), np.float32),
            "sizes": np.empty(n, np.float32),
        }
