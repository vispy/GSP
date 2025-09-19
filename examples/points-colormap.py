# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Points visual (Colormap)
========================

This example shows the Points visual where point colors are set
according to their depth (screen coordinate) and a colormap (magma).
This results in dynamic colors where most front points are alwyas
painted with the same color.
"""
import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm
from gsp import transform
import gsp

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, gsp.white)
colormap = transform.Colormap("magma")
depth = transform.Out("screen[positions].z")
positions = glm.vec3(10_000)
positions[...] = np.random.uniform(-1, +1, (len(positions),3))
fill_colors = colormap(depth)
points = visual.Points(positions, 25.0, fill_colors, gsp.black, 0.25)

# Show or save the result
render(canvas, [viewport], [points])
