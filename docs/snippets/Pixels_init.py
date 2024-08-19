# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.io import mkdocs

import numpy as np
from gsp import core, visual

# Snippet to be included in the documentation
with mkdocs():
    positions = core.Buffer(3, np.dtype(np.float32))
    pixels = visual.Pixels(positions, colors=(0,0,0,1))
