# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

from . core.canvas import Canvas
from . core.viewport import Viewport
from . core.buffer import Buffer


# This part ensures tracked array have an accompanying
# gsp buffer that keep track of updates.
import numpy as np
from gsp import glm
from gsp.glm.vlist import *
from gsp.glm.vec234 import *
from gsp.glm.mat234 import *
from gsp.io import register

@register("str", "memoryview")
def str_to_memoryview(obj):
    return memoryview(bytes(obj))

@register("list", "Color")
def list_to_Color(obj):
    return core.Color(*obj)

@register("Color", "list")
def Color_to_list(obj):
    return obj._color.tolist()

@register("list", "tuple")
def list_to_tuple(obj):
    return tuple(obj)

@register("tuple", "list")
def tuple_to_list(obj):
    return list(obj)

@register("int", "Canvas")
def int_to_Object(obj):
    return Object.objects[obj]

@register("ndarray", "Matrix")
def ndarray_to_Matrix(obj):
    return Matrix(obj)

@register("tracked", "Buffer")
def tracked_to_Buffer(obj):
    return obj._tracker.gsp_buffer

class Tracker:
    def __init__(self, ndarray):
        if ndarray is not None:
            self.ndarray = ndarray
            self.gsp_buffer = Buffer(ndarray.size, ndarray.dtype, ndarray.data)
            self.gsp_buffer.set_data(0, ndarray.tobytes())

    def set_data(self, offset, bytes):
        self.gsp_buffer.set_data(offset, bytes)

glm.ndarray.tracked.__tracker_class__ = Tracker
