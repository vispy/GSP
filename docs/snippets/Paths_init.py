# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.io import mkdocs

import gsp
import numpy as np

# Snippet to be included in the documentation
with mkdocs():
    positions = gsp.core.Buffer(2*3, np.dtype(np.float32))
    indices_data = gsp.core.Buffer(2, np.dtype(np.int32))
    indices_item = gsp.core.Buffer(2, np.dtype(np.int32))
    indices = gsp.core.List(indices_data, indices_item)
    paths = gsp.visual.Paths(positions, indices,
                             line_colors=(0,0,0,0),
                             line_widths=1.0,
                             line_styles = gsp.core.LineStyle.solid,
                             line_joins = gsp.core.LineJoin.round,
                             line_caps = gsp.core.LineCap.round)
