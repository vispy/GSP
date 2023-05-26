# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

import numpy as np

from .app import default_app


# -------------------------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------------------------

APP = default_app()


# -------------------------------------------------------------------------------------------------
# Pixels
# -------------------------------------------------------------------------------------------------

class Pixels:
    def __init__(self, viewport, vertices, colors):
        count = len(vertices.buffer)

        self._pixel = APP.pixel(count)

        # HACK: renormalization
        w, h = viewport.extent[2:]

        x = vertices.buffer['x']
        y = vertices.buffer['y']
        x = -1 + 2 * x / w
        y = -1 + 2 * y / h

        pos = np.c_[x, y, np.zeros(count)].astype(np.float32)

        r = colors.buffer['r']
        g = colors.buffer['g']
        b = colors.buffer['b']
        a = colors.buffer['a']
        col = np.c_[r, g, b, a].astype(np.float32)
        col = (255 * col).astype(np.uint8)

        self.viewport = viewport
        self.vertices = vertices
        self.colors = colors

        # Set the pixel arrays.
        self._pixel.position(pos)
        self._pixel.color(col)

        # Add the visual to the viewport.
        self.viewport._view.add(self._pixel)
