# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.backend.matplotlib import transform
from gsp.backend.matplotlib.core import Buffer

class Transform:

    def __init__(self):
        self._next = None
        self._buffer = None
        self._base = None
    
    def set_base(self, base):
        self._base = base

    def set_next(self, next):
        self._next = next
        
    def set_buffer(self, buffer):
        self._buffer = buffer

    def evaluate(self, buffers=None):
        raise NotImplementedError("Generic transforms cannot be evaluated")

    @property
    def base(self):
        if self._base:
            return self._base.base
        return self

    @property
    def buffer(self):
        return self._buffer
    
    @property
    def next(self):
        return self._next
    
    @property
    def last(self):
        last = self
        while last._next: last = last._next
        return last

    @property
    def bound(self):
        return self.last.buffer is not None

    def copy(self):
        transform = self.__class__()
        transform.set_buffer(self._buffer)
        transform.set_base(self.base)
        if self._next:
            transform.set_next(self._next.copy())
        return transform

    def __call__(self, other):
        transform = self.copy()
        if isinstance(other, Transform):
            transform.set_next(other.copy())
            transform.set_buffer(None)
        elif isinstance(other, (Buffer, np.ndarray)):
            if self.bound:
                raise ValueError("Transform is already bound")
            transform.last.set_buffer(other)
        else:
            raise ValueError("Unknown type")
        return transform

    def __add__(self, other):
        return transform.Add(self, other)

    def __sub__(self, other):
        return transform.Sub(self, other)

    def __mul__(self, other):
        return transform.Mul(self, other)

    def __div__(self, other):
        return transform.Div(self, other)

