import io
import numpy as np

from .app import default_app


class Canvas:

    def __init__(self, width, height,  dpi, dpr, offscreen):
        self.width = width
        self.height = height
        self.dpi = dpi
        self.dpr = dpr
        self.offscreen = offscreen

        with default_app().commands() as cmd:
            self._canvas = cmd.Canvas(width=width, height=height)

    # def render(self, format):
    #     self.figure.canvas.draw()
    #     with io.BytesIO() as output:
    #         self.figure.savefig(output, format='raw')
    #         output.seek(0)
    #         data = np.frombuffer(output.getvalue(), dtype=np.uint8)
    #     return data.reshape(self.ratio * self.height,
    #                         self.ratio * self.width,
    #                         -1)
