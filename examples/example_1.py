# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import GSP
import numpy as np
from canvas import Canvas
from viewport import Viewport
from array import Array
from datatype import Datatype

if __name__ == '__main__':

    GSP.mode("client")

    canvas = Canvas(512, 512, 100, 1, False)
    
    viewport = Viewport(canvas, 0, 0, 512, 512)

#    vec2 = np.dtype([("x", "f4"), ("y", "f4")])
#    vertices = np.array([(-1,-1), (+1,-1), (+1,+1), (-1,+1)], vec2)
#    vertices = Array.from_numpy(vertices)
    
