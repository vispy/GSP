# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Segments visual (2D)
====================

This example shows the Segment visual that can be zoomed using the
mouse and an orthographic camera.
"""
from common.launcher import parse_args
from gsp_matplotlib import glm
from gsp import transform
import gsp

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0.0, 0.0, 1.0, 1.0, white)
pixel = transform.Pixel()

P = glm.vec3((4,2))
P[0] =  (-0.75, -0.75,0), (-0.75,  0.75,0)
P[1] = (-0.75,  0.75,0), ( 0.75,  0.75,0)
P[2] = ( 0.75,  0.75,0), ( 0.75, -0.75,0)
P[3] = ( 0.75, -0.75,0), (-0.75, -0.75,0)
S1 = visual.Segments(P,
                     line_caps = gsp.core.LineCap.round,
                     line_colors = black,
                     line_widths=0.5)
S1.render(viewport)

P = glm.vec3((4,2))
P[0] = (-128, -128, 0), (-128,  128, 0)
P[1] = (-128,  128, 0), ( 128,  128, 0)
P[2] = ( 128,  128, 0), ( 128, -128, 0)
P[3] = ( 128, -128, 0), (-128, -128, 0)
# P = P._tracker.gsp_buffer * pixel
# P = P
# print(type (P*pixel))
# print( (P*pixel).evaluate({"dpi": 100}))

S2 = visual.Segments(P * pixel,
                     line_caps = gsp.core.LineCap.round,
                     line_colors = black,
                     line_widths=0.5)
S2.render(viewport)

# Show or save the result
render(canvas, [viewport], [S1, S2])
