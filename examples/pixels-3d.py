# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Pixels visual (3D)
==================

This example shows the Pixels visual where pixels are spread
randomly inside a cube that can be rotated and zoomed using the mouse
and a perspective camera.
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
P = glm.as_vec3(np.random.uniform(-1, +1, (n,3)))
pixels = visual.Pixels(P, colors=[0,0,0,1])
pixels.render(viewport)

# Show or save the result
render(canvas, [viewport], [pixels])