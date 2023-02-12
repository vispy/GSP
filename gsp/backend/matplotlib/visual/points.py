# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.transform import Mat4x4, Transform

class Points:
    def __init__(self, viewport,
                       positions, sizes, fill_colors,
                       edge_colors, edge_widths):

        self.viewport = viewport
        self.positions = np.asarray(positions)

        if not isinstance(sizes, np.ndarray):
            self.sizes = sizes * np.ones(len(self.positions), np.float32)
        else:
            self.sizes = sizes
        if isinstance(fill_colors, Buffer):
            self.fill_colors = np.asarray(fill_colors)
        else:
            self.fill_colors = fill_colors

        if isinstance(edge_colors, Buffer):
            self.edge_colors = np.asarray(edge_colors)
        else:
            self.edge_colors = edge_colors

        self.edge_widths = edge_widths

        V = self.positions.view(np.float32).reshape(-1,3)
        X, Y = V[:,0], V[:,1]
        S = self.sizes

        self.scatter = self.viewport.axes.scatter(X,Y)

        if isinstance(self.fill_colors, np.ndarray):
            FC = self.fill_colors.view(np.float32).reshape(-1,4)
            self.scatter.set_facecolors(FC)

        if isinstance(self.edge_colors, np.ndarray):
            EC = self.edge_colors.view(np.float32).reshape(-1,4)
            self.scatter.set_edgecolors(EC)
            
        self.scatter.set_sizes(S)
        self.scatter.set_visible(True)
        self.scatter.set_antialiaseds(True)
        self.scatter.set_linewidths(edge_widths)
        self.transform = Mat4x4(np.zeros(16,np.float32))

    def render(self, transform):

        self.transform.set_data(transform)
        V = self.positions.view(np.float32).reshape(-1,3)
        V = self.transform(V)
        I = np.argsort(-V[:,2])
        V = V[I]
        self.scatter.set_offsets(V[:,:2])
        
        depth = -V[:,2]
        if isinstance(self.fill_colors, Transform):
            FC = self.fill_colors.evaluate({"depth": depth,
                                            "index" : I})
            self.scatter.set_facecolors(FC)

        if isinstance(self.edge_colors, Transform):
            EC = self.edge_colors.evaluate({"depth": depth,
                                            "index" : I})
            self.scatter.set_edgecolors(EC)
        
