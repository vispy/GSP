# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
This example shows how to create a canvas and save it to a file.

Keywords: canvas, save, render
"""

import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
# canvas.render("./output/canvas-save.png")
