# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp
import numpy as np
from gsp.core.canvas import Canvas
from gsp.core.viewport import Viewport

if __name__ == '__main__':

    gsp.mode("client")

    canvas = Canvas(512, 512, 100, 1, False)

    viewport = Viewport(canvas, 0, 0, 512, 512)

#    vec2 = np.dtype([("x", "f4"), ("y", "f4")])
#    vertices = np.array([(-1,-1), (+1,-1), (+1,+1), (-1,+1)], vec2)
#    vertices = Array.from_numpy(vertices)
