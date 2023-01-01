import numpy as np

class Buffer:

    @classmethod
    def from_numpy(cls, Z):
        import numpy as np
        if (isinstance(Z, np.ndarray)):
            return Buffer(Z.size, Z.dtype, Z.tobytes())
        raise ValueError(f"Unknown type for {Z}, cannot convert to Buffer")

    def __init__(self, count, dtype, data):
        self.dtype = dtype
        self.buffer = np.frombuffer(data, dtype)

