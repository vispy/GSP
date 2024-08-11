# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.io import mkdocs

# Snippet to be included in the documentation
with mkdocs():
    from gsp.transform import Colormap
    colormap = Colormap("viridis")
    colormap.set_colormap("inferno")
