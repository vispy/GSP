# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from __future__ import annotations

from gsp import Object
from gsp.io.command import command
import numpy as np


class Texture(Object):
    """
    A texture is a rectangular two-dimensional image that can be
    applied to a surface in 3D space.
    """

    @command("core.Texture")
    def __init__(self, texture_data: np.ndarray, shape: tuple):
        """
        A texture is a rectangular two-dimensional image.

        Parameters
        ----------

        texture_data:
            The image data of the texture.
        shape:
            The shape of the texture (height, width, channels).
        """
        Object.__init__(self)
