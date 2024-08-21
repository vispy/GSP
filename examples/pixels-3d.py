# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
Pixels visual (3d, interactive)
===============================

This example show the **Pixels** visual where pixels are spread
randomly inside a cube that can be rotated and zoomed using the mouse.
"""
import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 250_000
P = glm.as_vec3(np.random.uniform(-1, +1, (n,3)))
pixels = visual.Pixels(P, colors=[0,0,0,1])

from camera import Camera
camera = Camera("perspective", theta=50, phi=50)
camera.connect(viewport, "motion",  pixels.render)
camera.save("output/pixels-3d.png")
camera.run()
