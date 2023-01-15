# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""Graphic Server Protocol / visual.Pixels

This is the matplotlib implementation of the Graphic Server Protocol (GSP) that
It allows to issue commands, parse them and build corresponding objects.
"""
import numpy as np

class Pixels:
    def __init__(self, viewport, vertices, colors, transform):
        self.viewport = viewport
        self.vertices = vertices
        self.colors = colors
        self.transform = transform

        V = vertices.buffer.view(np.float32).reshape(-1,3)
        V = self.transform.apply(V, self.viewport.transform)
        X,Y,Z = V[:,0], V[:,1], V[:,2]
        I = np.argsort(Z)
        X, Y = X[I], Y[I]

        # X,Y,Z = vertices[:,0], vertices[:,1], vertices[:,2]
        C = colors.buffer.view(np.float32).reshape(-1,4)
                
        # The marker size is in points**2 (typographic points are 1/72 in)
        # 1 pixel size is 1 / self.viewport.canvas.dpi inch
        # We want size * size * 1/72 = 1/dpi -> size = sqrt(72/dpi)
        dpi = self.viewport.canvas.dpi
        size = 1/dpi

        self.viewport.axes.scatter(X, Y, 5, C)


#        self.viewport.axes.scatter(X, Y, size, C,
#                                   marker=",",
#                                   linewidths=0,
#                                   antialiaseds=False)
