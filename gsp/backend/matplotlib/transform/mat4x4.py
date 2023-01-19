# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.core import Datatype

class Mat4x4:

    datatype = Datatype("f::16")

    @classmethod
    def ndarray_to_bytes(array):
        return array.tobytes()
    
    def __init__(self, data : bytes):
        self.data = data

    def __call__(self, V):

        V = np.asarray(V, dtype=np.float32)
        shape = V.shape
        V = V.reshape(-1,3)
        ones = np.ones(len(V), dtype=np.float32)
        V = np.c_[V.astype(np.float32), ones]  # Homogenous coordinates
        M = self.data
        V = V @ M.T                 # Transformed coordinates
        V = V/V[:,3].reshape(-1,1)  # Normalization
        V = V[:,:3]                 # Normalized device coordinates
        return V.reshape(shape)


