# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import Buffer, Color, Texture
from gsp.transform import Transform
from gsp.io.command import command


class Image(Visual):

    @command("visual.Image")
    def __init__(self, positions: Transform | Buffer, texture_2d: Texture, image_extent: tuple):

        super().__init__()

        # These variables are available prior to rendering
        self._in_variables = {
            "positions": positions,
            "texture_2d": texture_2d,
            "image_extent": image_extent,
            "viewport": None,
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        n = len(positions)
        self._out_variables = {
            "screen[positions]": np.empty((n, 3), np.float32),
        }
