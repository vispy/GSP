# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.matplotlib.transform import Transform

class Depth(Transform):

    def __init__(self):
        Transform.__init__(self)

    def __call__(self):
        raise ValueError("Depth transform cannot be composed")
        
    def evaluate(self, buffers=None):
        if "depth" in buffers.keys():
            return buffers["depth"]
        else:
            raise ValueError("Depth buffer not found")
