import numpy as np
from . datatype import Datatype

class Buffer:

    @classmethod
    def from_numpy(cls, Z):
        import numpy as np
        if (isinstance(Z, np.ndarray)):
            return Buffer(Z.size, Z.dtype, Z.tobytes())
        raise ValueError(f"Unknown type for {Z}, cannot convert to Buffer")

    def __init__(self, count, datatype, data):
        self.buffer = np.frombuffer(data, datatype.dtype)
        self.data = data

