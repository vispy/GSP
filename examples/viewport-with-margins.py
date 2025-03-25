# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Viewport with margins
=====================

This example show how to specify margins expressed in pixels (or
inches, centimeters, etc) when creating a viewport.
"""

import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
pixel = transform.Pixel()
viewport = core.Viewport(canvas, x = 10*pixel,
                                 y = 10*pixel,
                                 width = 1.0 - 20*pixel,
                                 height = 1.0 - 20*pixel,
                                 color = (1,1,1,1))
canvas.render("viewport-with-margins.png")
plt.show()
