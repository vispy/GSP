# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Pixels visual (2D)
==================

This example shows the Pixels visual where pixels are spread randomly
inside a square that can be zoomed using the mouse and an orthographic
camera.
"""

import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 250_000
P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)))
pixels = visual.Pixels(P, colors=[0,0,0,1])

# Show or save the result
render(canvas, [viewport], [pixels])
