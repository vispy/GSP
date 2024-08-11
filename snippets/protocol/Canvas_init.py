
from gsp.io import mkdocs2

with mkdocs2():
    from gsp.core.canvas import Canvas
    canvas = Canvas(512, 512, 101.0)
