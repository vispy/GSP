# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

import io
import numpy as np

# from datoviz.app import App
from . import default_app


# -------------------------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------------------------

APP = default_app()


# -------------------------------------------------------------------------------------------------
# Canvas
# -------------------------------------------------------------------------------------------------

class Canvas:

    def __init__(self, width, height,  dpi, dpr, offscreen):
        self.width = width
        self.height = height
        self.dpi = dpi
        self.dpr = dpr
        self.offscreen = offscreen

        self._canvas = APP.canvas(width=width, height=height, flags=3)

    def view(self, offset=(0, 0), shape=(0, 0)):
        return self._canvas.view(offset, shape)

    # def render(self, format):
    #     self.figure.canvas.draw()
    #     with io.BytesIO() as output:
    #         self.figure.savefig(output, format='raw')
    #         output.seek(0)
    #         data = np.frombuffer(output.getvalue(), dtype=np.uint8)
    #     return data.reshape(self.ratio * self.height,
    #                         self.ratio * self.width,
    #                         -1)
