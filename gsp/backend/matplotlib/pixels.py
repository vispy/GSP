import numpy as np

class Pixels:
    def __init__(self, viewport, vertices, colors):
        self.viewport = viewport
        self.vertices = vertices
        self.colors = colors

        vertices = vertices.buffer.view(np.float32).reshape(-1,3)
        X,Y,Z = vertices[:,0], vertices[:,1], vertices[:,2]
        C = colors.buffer.view(np.float32).reshape(-1,4)
                
        # The marker size in points**2 (typographic points are 1/72 in)
        # 1 pixel size is 1 / self.viewport.canvas.dpi inch
        # We want size * size * 1/72 = 1/dpi -> size = sqrt(72/dpi)
        dpi = self.viewport.canvas.dpi
        size = 1/dpi
        self.viewport.axes.scatter(X, Y, size, C,
                                   marker=",",
                                   linewidths=0,
                                   antialiaseds=False)
