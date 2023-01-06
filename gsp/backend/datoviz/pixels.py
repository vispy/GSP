import numpy as np

from .app import default_app


class Pixels:
    def __init__(self, viewport, vertices, colors):
        self.viewport = viewport
        self.vertices = vertices
        self.colors = colors

        vertices = vertices.buffer.view(np.float32).reshape(-1, 3)  # (n, 3)
        X, Y, Z = vertices[:, 0], vertices[:, 1], vertices[:, 2]  # (n,)
        C = colors.buffer.view(np.float32).reshape(-1, 4)  # (n, 4)

        canvas = viewport.canvas._canvas
        x, y, w, h = viewport.extent

        # HACK
        X = -1 + 2*X/w
        Y = -1 + 2*Y/h
        C = (255 * C).astype(np.uint8)

        n = len(X)
        arr = np.zeros(
            n, dtype=[('pos', 'f4', 3), ('color', 'u1', 4), ('size', 'f4')])
        arr['pos'] = np.c_[X, Y, Z * 0]
        arr['color'][:] = C
        arr['size'][:] = 10.0

        with default_app().commands() as cmd:
            g = cmd.Graphics(1, flags=3)  # default MVP and viewport

            vb = cmd.VertexBuffer(arr)
            g.set_vertex_buffer(vb)

            with canvas.record() as r:
                r.viewport(0, 0, 0, 0)  # HACK
                r.draw(g, 0, n)
