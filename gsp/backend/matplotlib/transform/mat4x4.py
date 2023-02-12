# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.transform import Transform


class Mat4x4(Transform):

    def __init__(self, data):
        Transform.__init__(self)
        self._data = np.frombuffer(data, dtype=np.float32).reshape((4,4))

    def set_data(self, data):
        if isinstance(data, Mat4x4):
            self._data[...] = data._data
        else:
            self._data[...] = data
        
    def __call__(self, V):

        V = np.asarray(V, dtype=np.float32)
        shape = V.shape
        V = V.reshape(-1,3)
        ones = np.ones(len(V), dtype=np.float32)
        V = np.c_[V.astype(np.float32), ones]  # Homogenous coordinates
        V = V @ self._data.T                   # Transformed coordinates
        V = V/V[:,3].reshape(-1,1)             # Normalization
        V = V[:,:3]                            # Normalized device coordinates
        return V.reshape(shape)
