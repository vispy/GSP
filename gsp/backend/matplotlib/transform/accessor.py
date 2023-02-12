# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.transform import Transform

class Accessor(Transform):
    def __init__(self, key=None):
        Transform.__init__(self)
        self._key = key

    def copy(self):
        transform = Transform.copy(self)
        transform._key = self._key
        return transform
        
    def evaluate(self, buffers=None):
        if self._next:
            buffer = self._next.evaluate(buffers)
        elif buffer is None:
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
    def __init__(self, key=None):
        Accessor.__init__(self, "x")

class Y(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "y")

class Z(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "z")

class W(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "w")

class R(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "r")

class G(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "g")

class B(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "b")

class A(Accessor):
    def __init__(self, key=None):
        Accessor.__init__(self, "a")


