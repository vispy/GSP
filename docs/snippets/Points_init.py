# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.io import mkdocs

import numpy as np
from gsp import core, visual

# Snippet to be included in the documentation
with mkdocs():
    positions = core.Buffer(3, np.dtype(np.float32))
    points = visual.Points(positions,
                           sizes=5.0,
                           fill_colors=(0,0,0,1),
                           line_colors=(0,0,0,0),
                           line_widths=0.0)
