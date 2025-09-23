# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Pixels visual (colormap)
=======================

This example shows the Pixels visual where pixels are colored according to screen coordinates (x,y) and depth (z) using a colormap.
"""
import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm
from gsp import transform

# Parse command line arguments
core, visual, render = parse_args()

print("Warning: This example may take a while to render due to the large number of pixels.")

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
colormap = transform.Colormap("magma")
depth = transform.Out("screen[positions].z")
n = 500_000
P = glm.as_vec3(np.random.uniform(-1, +1, (n,3)))
C = colormap(depth)
pixels = visual.Pixels(P, C)
pixels.render(viewport)

# Show or save the result
render(canvas, [viewport], [pixels])