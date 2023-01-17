# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy developmet team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np

class Viewport:
        
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.extent = x, y, width, height
        self.axes = canvas.figure.add_axes([x / canvas.width,
                                            y / canvas.height,
                                            width / canvas.width,   
                                            height / canvas.height])
        self.axes.autoscale(False)
        self.axes.set_xlim(0, width)
        self.axes.set_ylim(0, height)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        for position in ["top", "bottom", "left", "right"]:
            self.axes.spines[position].set_visible(False)

        # Matplotlib takes care of placing the viewport at the right
        # position such that we don't need to translate it ourselves.
        x, y = 0, 0
        w, h = width,height
        d = 0

        transform = np.array([[w/2, 0, 0, x+w/2],
                              [0, h/2, 0, y+h/2],
                              [0, 0, d/2,   d/2],
                              [0, 0, 0,       1]], dtype=np.float32)
        from gsp.backend.matplotlib.transform import Mat4x4
        self.transform = Mat4x4(transform.tobytes())

