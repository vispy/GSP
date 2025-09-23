# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Points visual (3D)
==================

This example shows the Points visual with different sizes can be
roated and zoomed using the mouse and a perspective camera. Points
size is updated accordin to zoom level.
"""
import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm
import gsp

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, gsp.white)

n = 5_000
positions = glm.vec3(n)
positions[...] = np.random.uniform(-1, +1, (n, 3))

_sizes = np.random.uniform(25, 40, n)
sizes = glm.float(n)
sizes[...] = _sizes

_linewidths = 0.25
linewidths = glm.float(n)
linewidths[...] = _linewidths

points = visual.Points(positions, sizes, gsp.grey, gsp.white, linewidths)
points.render(viewport)

def update(viewport, model, view, proj, camera):
    sizes[...] =  1/(camera.zoom**2) * _sizes
    linewidths[...] = 1/(camera.zoom) * _linewidths
    points.render(viewport, model, view, proj)

# Show or save the result
render(canvas, [viewport], [points], onRender=update)