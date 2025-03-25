# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Paths visual (2D)
=================

This example shows the Paths visual where a set of 2D paths with
increasing line widths is displayed. Some code is commented to show
the different ways to specify path sizes.
"""

import gsp
gsp.use("matplotlib")

black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])

n = 50
P = glm.vec3(2*n).reshape(-1,2,3)
P[:] = (0.0, -0.5, 0.0), (0.0, +0.5, 0.0)
P[:,0,0] = np.linspace(-0.75, +0.75, n)
P[:,1,0] = P[:,0,0] + 0.1
line_widths = np.linspace(0.1, 5.0, n)

# Paths with same size
# I = 2

# Paths with (potentially) different size
# I = 2*np.ones(n, dtype=int)

# Indexed paths
I = np.arange(2*n).reshape(-1,2).tolist()

paths = visual.Paths(P, I,
                     line_colors = black,
                     line_widths = line_widths,
                     line_styles = gsp.core.LineStyle.solid,
                     line_joins = gsp.core.LineJoin.round,
                     line_caps = gsp.core.LineCap.round)

from camera import Camera
camera = Camera("ortho")
camera.connect(viewport, "motion",  paths.render)
# camera.save("output/paths-2d.png")
camera.run()
