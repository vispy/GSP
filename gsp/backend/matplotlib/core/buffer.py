# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from . datatype import Datatype
from gsp.converters import Datatype_to_dtype

class Buffer:
    def __init__(self, count, datatype, data):

        if isinstance(datatype, Datatype):
            dtype = Datatype_to_dtype(datatype.format)
        else:
            dtype = datatype

        self.buffer = np.frombuffer(data, dtype)


    def set_data(self, offset, data):
        pass
