# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
Pixels visual (2d)
==================

This example show the Pixels visual where pixels are spread
randomly inside a square that can be zoomed using the mouse.
"""
import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 250_000
P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)))
pixels = visual.Pixels(P, colors=[0,0,0,1])

from camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  pixels.render)
camera.save("output/pixels-2d.png")
camera.run()
