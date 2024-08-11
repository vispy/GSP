# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.io import mkdocs

# Snippet to be included in the documentation
with mkdocs():
    from gsp.core.data import Data
    data = Data(nbytes=512, dtype=[("color", 1, "u4")])
