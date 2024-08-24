# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
Points visual (2D)
==================

This example shows the Points visual with different sizes can be zoomed
using the mouse and an orthographic camera.
"""
import gsp
gsp.use("matplotlib")

black = [0,0,0,1]
white = [1,1,1,1]

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, white)

n = 600

P = glm.vec3(n)
R = np.linspace(0.05, 0.95, n)
T = np.linspace(0, 10.125*2*np.pi, n)
P.xy = R*np.cos(T), R*np.sin(T)

sizes = glm.float(n)
sizes[...] = np.linspace(0.05, 12.0,n)**2

points = visual.Points(P, sizes, black, black, 0.0)

from camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  points.render)
camera.save("output/points-2d.png")
camera.run()
