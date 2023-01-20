# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.backend.matplotlib.transform import Mat4x4
        
class Pixels:

    def __init__(self, viewport, positions, colors):
        "Build the visual on viewport using the given properties"
        
        self.viewport = viewport
        self.positions = positions
        self.colors = colors

        # Even with antialias off, marker coverage leaks on
        # neighbouring pixels if the position is not an exact divider
        # of viewport size (in pixels). We could round vertices at
        # time of rendering but it is easier to set a very small size
        # whose coverage is more or less guarantedd to be one pixel.
        size = 0.01 * (72/self.viewport.canvas.dpi)**2
        self.scatter = self.viewport.axes.scatter([], [], size)
        self.scatter.set_antialiaseds(False)
        self.scatter.set_linewidths(0)
        self.transform = Mat4x4(np.zeros(16,np.float32))

        
    def render(self, transform):
        "Render the visual on viewport using the given transform."

        self.transform.M = transform        
        C = self.colors.view(np.float32).reshape(-1,4)
        V = self.positions.view(np.float32).reshape(-1,3)
        V = self.transform(V)
        I = np.argsort(-V[:,2])
        V, C = V[I], C[I]
        self.scatter.set_offsets(V[:,:2])
        self.scatter.set_facecolors(C)
