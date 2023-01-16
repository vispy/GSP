import numpy as np
from gsp.backend.matplotlib import Buffer
from gsp.backend.matplotlib import Datatype

class Matrix:

    datatype = Datatype("f::16")

    def __init__(self, data):
        self.buffer = Buffer(1, self.datatype, data)

    def __call__(self, V):

        V = np.asarray(V, dtype=np.float32)
        shape = V.shape
        V = V.reshape(-1,3)
        ones = np.ones(len(V), dtype=np.float32)
        V = np.c_[V.astype(np.float32), ones]  # Homogenous coordinates
        M = np.frombuffer(self.buffer.data,
                          self.datatype.dtype)
        M = M.reshape(4,4)
        V = V @ M.T                 # Transformed coordinates
        V = V/V[:,3].reshape(-1,1)  # Normalization
        V = V[:,:3]                 # Normalized device coordinates
        return V.reshape(shape)


