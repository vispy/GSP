# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
        
class Pixels:
    
    def __init__(self, viewport, positions, colors):
        "Render the visual on viewport using the given transform."
        
        self.viewport = viewport
        self.positions = positions
        self.colors = colors
        self.scatter = None

    def render(self, transform):
        "Render the visual on viewport using the given transform."
        
        C = self.colors.view(np.float32).reshape(-1,4)
        V = self.positions.view(np.float32).reshape(-1,3)
        V = transform(V)

        I = np.argsort(V[:,2])
        V = V[I]
        C = C[I]
        
        if self.scatter is None:
            size = 1/self.viewport.canvas.dpi
            # size = 1
            self.scatter = self.viewport.axes.scatter([], [], size)
            self.scatter.set_antialiaseds(False)
        
        V = self.viewport.transform(V)
        self.scatter.set_offsets(V[:,:2])
        self.scatter.set_facecolors(C)
