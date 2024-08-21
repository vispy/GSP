# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
Pixels visual (colormap)
=======================

This example shows the Pixels visual where pixels are colored according to screen coordinates (x,y) and depth (z) using a colormap.
"""
import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
colormap = transform.Colormap("magma")
depth = transform.Out("screen[positions].z")
n = 500_000
P = glm.as_vec3(np.random.uniform(-1, +1, (n,3)))
C = colormap(depth)
pixels = visual.Pixels(P, C)

from camera import Camera
camera = Camera("perspective", theta=50, phi=50)
camera.connect(viewport, "motion",  pixels.render)
camera.save("output/pixels-colormap.png")
camera.run()
