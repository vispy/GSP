# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
import numpy as np
from ..core import Buffer
from . transform import Transform
from ..io.command import command


class Accessor(Transform):
    """
    Accessor transform allows to access a specific field in a Buffer
    """

    @command("transform.Accessor")
    def __init__(self, buffer : Transform | Buffer = None,
                       key : str = None):
        """
        Accessor transform allows to access a specific field in a Buffer.

        Parameters
        ----------
        key :
            Name of the field to access
        """

        Transform.__init__(self, buffer=buffer,
                           __no_command__ = True)
        self._key = key

    def copy(self):
        transform = Transform.copy(self)
        transform._key = self._key
        return transform

    def evaluate(self, buffers=None):
        if self._next:
            buffer = self._next.evaluate(buffers)
        elif self._buffer is not None:
            buffer = self._buffer
        else:
            raise ValueError("Transform is not bound")

        if buffer.dtype.names:
            buffer = buffer[self._key]
        elif self._key in "xyzw":
            buffer = buffer[..., "xyzw".index(self._key)]
        elif self._key in "rgba":
            buffer = buffer[..., "rgba".index(self._key)]
        else:
            raise IndexError(f"Unknown key {self._key}")

        if "index" in buffers.keys():
            return buffer[buffers["index"]]
        else:
            return buffer


class X(Accessor):

    @command("transform.X")
    def __init__(self, buffer : Transform | Buffer = None):
        "X Accessor (first field)"

        Accessor.__init__(self, buffer, "x",
                          __no_command__ = True)

class Y(Accessor):

    @command("transform.Y")
    def __init__(self, buffer : Transform | Buffer = None):
        "Y Accessor (second field)"

        Accessor.__init__(self, buffer, "y",
                          __no_command__ = True)


class Z(Accessor):

    @command("transform.Z")
    def __init__(self, buffer : Transform | Buffer = None):
        "Z Accessor (third field)"

        Accessor.__init__(self, buffer, "z",
                          __no_command__ = True)

class W(Accessor):

    @command("transform.W")
    def __init__(self, buffer : Transform | Buffer = None):
        "W Accessor (fourth field)"

        Accessor.__init__(self, buffer, "w",
                          __no_command__ = True)


class R(Accessor):

     @command("transform.R")
     def __init__(self, buffer : Transform | Buffer = None):
         "R Accessor (first field)"

         Accessor.__init__(self, buffer, "r",
                           __no_command__ = True)

class G(Accessor):

    @command("transform.G")
    def __init__(self, buffer : Transform | Buffer = None):
        "G Accessor (second field)"

        Accessor.__init__(self, buffer, "g",
                          __no_command__ = True)

class B(Accessor):

    @command("transform.B")
    def __init__(self, buffer : Transform | Buffer = None):
        "B Accessor (third field)"

        Accessor.__init__(self, buffer, "b",
                          __no_command__ = True)

class A(Accessor):

    @command("transform.A")
    def __init__(self, buffer : Transform | Buffer = None):
        "A Accessor (fourth field)"

        Accessor.__init__(self, buffer, "a",
                          __no_command__ = True)
