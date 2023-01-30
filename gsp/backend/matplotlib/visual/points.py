# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from gsp.backend.matplotlib.transform import Mat4x4


class Points:
    def __init__(self, viewport,
                       positions, sizes, fill_colors,
                       edge_colors, edge_widths):

        self.viewport = viewport
        self.positions = positions
        if not isinstance(sizes, np.ndarray):
            self.sizes = sizes * np.ones(len(positions), np.float32)
        else:
            self.sizes = sizes
        self.fill_colors = fill_colors
        self.edge_colors = edge_colors
        self.edge_widths = edge_widths

        V = self.positions.view(np.float32).reshape(-1,3)
        FC = self.fill_colors.view(np.float32).reshape(-1,4)
        EC = self.edge_colors.view(np.float32).reshape(-1,4)
        X, Y = V[:,0], V[:,1]
        S = self.sizes

        self.scatter = self.viewport.axes.scatter(X,Y)
        self.scatter.set_facecolors(FC)
        self.scatter.set_edgecolors(EC)
        self.scatter.set_sizes(S)
        self.scatter.set_visible(True)
        self.scatter.set_antialiaseds(True)
        self.scatter.set_linewidths(edge_widths)
        self.transform = Mat4x4(np.zeros(16,np.float32))

    def render(self, transform):

        self.transform.M = transform        
        FC = self.fill_colors.view(np.float32).reshape(-1,4)
        EC = self.edge_colors.view(np.float32).reshape(-1,4)
        V = self.positions.view(np.float32).reshape(-1,3)
        V = self.transform(V)
        I = np.argsort(-V[:,2])
        V = V[I]

        cmap = plt.get_cmap("magma")
        Z = -V[:,2]
        norm = mpl.colors.Normalize(vmin=Z.min(),vmax=Z.max())
        FC = cmap(norm(Z))
        self.scatter.set_facecolors(FC)
        
        self.scatter.set_offsets(V[:,:2])
        
