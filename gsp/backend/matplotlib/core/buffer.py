# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from . datatype import Datatype

class Buffer:
    def __init__(self, count, dtype, data):
        self.buffer = np.frombuffer(data, dtype)

