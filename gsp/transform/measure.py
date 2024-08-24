# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np
from gsp.io.command import command
from gsp.transform import Transform


class Measure(Transform):
    """
    A Measure transform allows to convert a measure expressed in
    some units (Pixel, Point, Inch, etc.) to normalized device
    coordinates ([-1,+1] x [-1,+1]). This conversion is always
    relative to a given Viewport whose width and height dictates the
    conversion.

    !!! Notes

        The normalization of a measure (conversion to NDC) migth be
        different on the x or y axis depending on the size of the related
        viewport. This means, for example, that the expression `10*pixel`
        is translated differently along `x` (1st component) and `y` axis
        (second component). The `z` coordinate is not changed during
        conversion since measures are targeting 2D coordinates.

    Examples
    --------

    ``` python
    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, color=(1,1,0,1))

    # 10 pixels from bottom left corner
    pixel = transform.Pixel()
    P = [-1,-1,0] + 10*pixel

    # 10 points from left, 20 points from bottom
    point = transform.Point()
    P = [-1,-1,0] + (10,20,0)*point
    ```
    """

    # See https://numpy.org/doc/stable/user/c-info.beyond-basics.html
    __array_priority__ = 2

    @command("transform.Measure")
    def __init__(self):
        super.__init__(__no_command__ = True)


    def evaluate(self, variables):
        """
        Evaluate the transform
        """

        if "dpi" in variables.keys():
            dpi = variables["dpi"]
            width, height = 1,1
            scale = 1
        elif "viewport" in variables.keys():
            viewport = variables["viewport"]
            dpi = viewport._canvas._dpi
            width, height = viewport.size
            xlim,ylim = viewport.xlim, viewport.ylim
            scale = xlim[1]-xlim[0], ylim[1]-ylim[0], 1
        elif "canvas" in variables.keys():
            canvas = variables["canvas"]
            dpi = canvas._dpi
            width, height = canvas.size
            scale = 1
        else:
            raise ValueError("Neither dpi, Canvas nor Viewport have been specified")

        if "size" in variables.keys():
            width, height = variables["size"]

        if self._next:
            value = self._next.evaluate(variables)
        elif self._buffer is not None:
            value = self._buffer
        else:
            raise ValueError("Transform is not bound")

        value = np.asanyarray(value)

        # Canvas normalized device coordinates goes from 0 to +1
        # Viewport normalized device coordinates goes from -1 to +1
        scale = scale*np.array([1/width, 1/height, 0])

        if len(value.shape) == 0 or value.shape[-1] == 1:
            scale = scale[0]
        elif value.shape[-1] == 2:
            scale = scale[:2]

        return scale * value

    def __mul__(self, other):
        if isinstance(other, (int,float,tuple,np.ndarray)):
            return self(other)
        return Transform.__mul__(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def dpi(self, variables):
        """
        Extract dpi value from given variables
        """

        if "dpi" in variables.keys():
            dpi = variables["dpi"]
        elif "canvas" in variables.keys():
            dpi = variables["canvas"]._dpi
        elif "viewport" in variables.keys():
            dpi = variables["viewport"]._canvas._dpi
        else:
            raise ValueError("Neither dpi, Canvas nor Viewport have been specified")
        return dpi

class Pixel(Measure):
    """
    Conversion of a measure to pixel.
    """

    @command("transform.Pixel")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)


    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return measure


class Inch(Measure):
    """
    Conversion of a measure to inch.
    """

    @command("transform.Inch")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)

    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return self.dpi(variables) * measure

class Point(Measure):
    """
    Conversion of a measure to point
    """

    @command("transform.Point")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)

    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return self.dpi(variables)/72 * measure

class Centimeter(Measure):
    """
    Conversion of a measure to centimeter
    """

    @command("transform.Centimeter")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)

    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return self.dpi(variables)/2.54 * measure

class Millimeter(Measure):
    """
    Conversion of a measure to millimeter
    """

    @command("transform.Millimeter")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)

    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return 0.1*self.dpi(variables)/2.54 * measure

class Meter(Measure):
    """
    Conversion of a measure to meter
    """

    @command("transform.Meter")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)

    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return 10e2*self.dpi(variables)/2.54 * measure

class Kilometer(Measure):
    """
    Conversion of a measure to kilometer
    """

    @command("transform.Kilometer")
    def __init__(self):
        Transform.__init__(self,
                           __no_command__ = True)

    def evaluate(self, variables):
        """Evaluate the transform"""

        measure = Measure.evaluate(self, variables)
        return 1e5*self.dpi(variables)/2.54 * measure
