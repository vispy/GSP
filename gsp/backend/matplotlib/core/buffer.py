# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from gsp.converters import str_to_dtype

class Buffer:
    def __init__(self, count, dtype, data):

        if isinstance(dtype, str):
            dtype = str_to_dtype(dtype)
        self._buffer = np.empty(count, dtype=dtype)
        self._buffer[...] = np.frombuffer(data, dtype)

    def set_data(self, offset, data):
        data = np.frombuffer(data, self._buffer.dtype)
        start = offset // self._buffer.dtype.itemsize
        stop = start + len(data)
        self._buffer[start:stop] = data

    def __array__(self):
        return self._buffer
