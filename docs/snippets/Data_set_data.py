# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.io import mkdocs

# Snippet to be included in the documentation
with mkdocs():
    import numpy as np
    from gsp.core.data import Data

    nbytes = 2*np.float32(0).nbytes
    data = Data(nbytes=nbytes, dtype=["f4"])
    data.set_data(0, bytes(nbytes))
