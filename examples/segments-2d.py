# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Segments visual (2D)
====================

This example shows the Segment visual where a set of 2D segments with
increasing line widths are displayed.
"""
import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm
import gsp

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])

n = 50
P = glm.vec3(2*n).reshape(-1,2,3)
P[:] = (0.0, -0.5, 0.0), (0.0, +0.5, 0.0)
P[:,0,0] = np.linspace(-0.75, +0.75, n)
P[:,1,0] = P[:,0,0] + 0.1
line_widths = np.linspace(0.1, 5.0, n)
segments = visual.Segments(P,
                           line_caps = gsp.core.LineCap.round,
                           line_colors = black,
                           line_widths=line_widths)

# Show or save the result
render(canvas, [viewport], [segments])
