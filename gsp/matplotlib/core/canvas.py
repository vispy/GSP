# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import io
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from gsp import core
from gsp import transform

class Canvas(core.Canvas):

    __doc__ = core.Canvas.__doc__

    def __init__(self, width : int,
                       height : int,
                       dpi : float):

        super().__init__(width, height, dpi,
                         __no_command__ = True)

        if isinstance(width, transform.Transform):
            width = width.evaluate(variables = { "dpi": dpi })
        if isinstance(height, transform.Transform):
            height = height.evaluate(variables = { "dpi": dpi })

        self._width = width
        self._height = height
        self._dpi = dpi

        self._figure = plt.figure(frameon=False, dpi=self._dpi)
        self._figure.patch.set_alpha(0.0)
        self._figure.set_size_inches(self._width / self._dpi,
                                     self._height /self._dpi)

        canvas = self._figure.canvas
        canvas.mpl_connect('resize_event', lambda event: self._figure.canvas.draw())


    @property
    def size(self):
        # figure.dpi and canvas.dpi might be different because system
        # such as OSX will double the dpi (retina display)
        dpi = self._dpi
        return self._figure.get_size_inches() * dpi


    def render(self, target : str):
        if target is None:
            self._figure.canvas.draw()
            with io.BytesIO() as output:
                self._figure.savefig(output, format="raw")
                output.seek(0)
                data = np.frombuffer(output.getvalue(), dtype=np.uint8)
            return data.reshape(self._height, self._width, -1)
        else:
            self._figure.savefig(target, dpi=self._dpi)
