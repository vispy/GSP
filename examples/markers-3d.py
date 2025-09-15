# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Markers visual (3D)
==================

This example shows several star markers placed on the surface of a
sphere. It can be zoomed and rotated.
"""
import gsp
gsp.use("matplotlib")

black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, white)
colormap = transform.Colormap("gray_r")
depth = transform.Out("screen[positions].z")

n = 256
P = glm.vec3(n)
T = np.pi * (3 - np.sqrt(5)) * np.arange(n)
Z = np.linspace(1 - 1.0 / n, 1.0 / n - 1, n)
R = np.sqrt(1 - Z*Z)
P.xy, P.z = (R*np.sin(T), R*np.cos(T)), Z

markers = visual.Markers(P,
                         types = [core.Marker.star]*n,
                         sizes = 256.0,
                         axis = P,
                         angles = 0.0,
                         fill_colors = colormap(depth),
                         line_colors = white,
                         line_widths = 0.0)

from examples.common.camera import Camera
camera = Camera("perspective")
camera.connect(viewport, "motion",  markers.render)
camera.save("output/markers-3d.png")
camera.run()
