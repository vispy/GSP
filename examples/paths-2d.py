# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Paths visual (2D)
=================

This example shows the Paths visual where a curve is split into
segments that are colored using a colormap.
"""

import gsp
gsp.use("matplotlib")

black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])

n = 256
T = np.linspace(-7.4, -0.5, n)
P = glm.vec3(n)
P[:,0] = 0.9 * np.sin(T)
P[:,1] = 0.9 * np.cos(1.6*T)
P[:,2] = 0.0

I = np.repeat(np.arange(n),2)[1:-1].reshape(-1,2)
D = np.linspace(0, 1, len(I))
colormap = transform.Colormap("plasma")

paths = visual.Paths(P, I.tolist(),
                     line_colors = colormap(D),
                     line_widths = 1+20.0*D,
                     line_styles = gsp.core.LineStyle.solid,
                     line_joins = gsp.core.LineJoin.miter,
                     line_caps = gsp.core.LineCap.round)

from common.camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  paths.render)
# camera.save("output/paths-2d.png")
camera.run()
