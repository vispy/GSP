# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from . datatype import Datatype

class Buffer:

    @classmethod
    def from_numpy(cls, Z):
        if (isinstance(Z, np.ndarray)):
            datatype = Datatype.from_numpy(Z.dtype)
            return Buffer(Z.size, datatype, Z.tobytes())
        raise ValueError(f"Unknown type for {Z}, cannot convert to Buffer")

    def __init__(self, count, datatype, data):
        self.buffer = np.frombuffer(data, datatype.dtype)
        self.data = data

