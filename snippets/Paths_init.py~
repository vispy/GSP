# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.io import mkdocs

import numpy as np
from gsp import core, visual

# Snippet to be included in the documentation
with mkdocs():
    positions = core.Buffer(2*3, np.dtype(np.float32))
    markers = visual.Segments(positions,
                              line_caps=core.LineCap.round,
                              line_colors=(0,0,0,0),
                              line_widths=0.0)
