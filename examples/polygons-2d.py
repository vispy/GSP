# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Polygon visual (2D)
===================

This example shows the Polygons visual where a set of 2D regular polygons.
"""

import gsp
gsp.use("matplotlib")

black, white, gray = [0,0,0,1], [1,1,1,1], [0,0,0,0.05]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])

n = 3
radius = 0.85*(1/n)
OX = np.linspace(-1+1/n, +1-1/n, n)
OY = np.linspace(+1-1/n, -1+1/n, n)
I  = np.arange(0+3,n*n+3)
P = glm.vec3(I.sum())
index, n = 0, I[0]
for oy in OY:
    for ox in OX:
        for theta  in np.linspace(0, 2*np.pi, n, endpoint=False):
            P[index] = ox+radius*np.cos(theta), oy+radius*np.sin(theta), 0
            index = index + 1
        n = n + 1

polys = visual.Polygons(P, I,
                        fill_colors = gray,
                        line_colors = black,
                        line_widths = 2.0,
                        line_styles = gsp.core.LineStyle.solid,
                        line_joins = gsp.core.LineJoin.round)

from common.camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  polys.render)
# camera.save("output/polygons-2d.png")
camera.run()
