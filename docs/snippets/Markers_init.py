# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.io import mkdocs

import numpy as np
from gsp import core, visual

# Snippet to be included in the documentation
with mkdocs():
    positions = core.Buffer(3, np.dtype(np.float32))
    sizes =  core.Buffer(3, np.dtype(np.float32))
    markers = visual.Markers(positions,
                             types=core.Marker.star,
                             sizes=sizes,
                             axis=None,
                             angles=0.0,
                             fill_colors=(0,0,0,1),
                             line_colors=(0,0,0,0),
                             line_widths=0.0)
