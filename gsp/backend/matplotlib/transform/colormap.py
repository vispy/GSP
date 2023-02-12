# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.transform import Transform

class Colormap(Transform):
    def __init__(self, colormap=None):
        Transform.__init__(self)
        self._colormap = colormap

    def copy(self):
        transform = Transform.copy(self)
        transform._colormap = self._colormap
        return transform
        
    def evaluate(self, buffers=None):
        if self._next:
            buffer = self._next.evaluate(buffers)
        else:
            buffer = self._buffer
        cmap = plt.get_cmap(self._colormap)
        norm = mpl.colors.Normalize(vmin=buffer.min(), vmax=buffer.max())
        return cmap(norm(buffer))

