# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.io import mkdocs

# Snippet to be included in the documentation
with mkdocs():
    from gsp.core.canvas import Canvas
    canvas = Canvas(512, 512, 100.0)
    canvas.render("png")
