# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Segments visual (2D)
====================

This example shows the Segment visual that can be zoomed using the
mouse and an orthographic camera.
"""
import gsp
gsp.use("matplotlib")

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


from common.camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  S1.render)
camera.connect(viewport, "motion",  S2.render)
# camera.save("output/segments-fixed-size.png")
camera.run()
