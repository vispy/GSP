# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
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

@register("ndarray", "Matrix")
def ndarray_to_Matrix(obj):
    return Matrix(obj)

@register("list", "Buffer")
def list_to_Buffer(obj):
    # WARN: Do we need to keep track of obj/Buffer such as not create
    #       several buffers pointing at the same underlying object?
    #       In the current implementation, Buffer is created each time
    #       this convertes is called such that if the obj has been
    #       mofidied, it shoudl be ok
    Z = glm.ndarray.tracked(obj)
    return Z._tracker.gsp_buffer

@register("list", "List")
def list_to_List(obj):
    count = [len(sublist) for sublist in obj]
    count = glm.ndarray.tracked(count)
    items = [item for sublist in obj for item in sublist]
    items = glm.ndarray.tracked(items)

    return List(items, count)


@register("ndarray", "Buffer")
def ndarray_to_Buffer(obj):
    # WARN: Do we need to keep track of obj/Buffer such as not create
    #       several buffers pointing at the same underlying object?
    #       In the current implementation, Buffer is created each time
    #       this convertes is called such that if the obj has been
    #       mofidied, it shoudl be ok
    Z = glm.ndarray.tracked(obj)
    return Z._tracker.gsp_buffer

@register("tracked", "Buffer")
def tracked_to_Buffer(obj):
    return obj._tracker.gsp_buffer

class Tracker:
    def __init__(self, ndarray):
        if ndarray is not None:
            self.ndarray = ndarray
            self.gsp_buffer = Buffer(len(ndarray), ndarray.dtype, ndarray.data)
            self.gsp_buffer.set_data(0, ndarray.tobytes())

    def set_data(self, offset, bytes):
        self.gsp_buffer.set_data(offset, bytes)

glm.ndarray.tracked.__tracker_class__ = Tracker
