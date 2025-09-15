# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Markers visual (2D)
==================

This example shows the Markers visual with different sizes can be zoomed
using the mouse and an orthographic camera.
"""
import gsp
gsp.use("matplotlib")

black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, white)

n = 600
P = glm.vec3(n)
A = glm.float(n)
R = np.linspace(0.05, 0.95, n)
T = np.linspace(0, 10.125*2*np.pi, n)
P.xy = R*np.cos(T), R*np.sin(T)

angles = glm.float(n)
angles[...] = 180.0*T/np.pi
sizes = glm.float(n)
sizes[...] = np.linspace(0.05, 12.0,n)**2
types = core.Marker.star
markers = visual.Markers(P, types, sizes, None, angles, black, white, 0.5)

from examples.common.camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  markers.render)
camera.save("output/markers-2d.png")
camera.run()
