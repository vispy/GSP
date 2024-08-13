# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

#from . data import Data
from . buffer import Buffer
from . canvas import Canvas
from . viewport import Viewport
#from . types import Type, Color, Marker, Measure
#from . types import LineCap, LineStyle, LineJoin


# # This part ensures tracked array have an accompanying
# # gsp buffer that keep track of updates.
# import numpy as np
# from gsp import glm
# from gsp.glm.vlist import *
# from gsp.glm.vec234 import *
# from gsp.glm.mat234 import *
# from gsp.io import register

# class Tracker:
#     def __init__(self, ndarray):
#         if ndarray is not None:
#             self.ndarray = ndarray
#             self.gsp_buffer = Buffer(ndarray.size, ndarray.dtype, ndarray.data)
#             self.gsp_buffer.set_data(0, ndarray.tobytes())

#     def set_data(self, offset, bytes):
#         self.gsp_buffer.set_data(offset, bytes)

# glm.ndarray.tracked.__tracker_class__ = Tracker

# @register("tracked", "Buffer")
# def tracked_to_Buffer(obj):
#     return obj.gsp_buffer
