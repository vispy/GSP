# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np

def dtype_to_Datatype(dtype):
    """Convert a numpy type into a Datatype"""

    from gsp.backend.reference.core.datatype import Datatype

    datatype = ""
    dtype = str(dtype)
    if dtype.startswith("["):
        for item in eval(dtype):
            if len(item) == 2:
                iname, itype = item
                isize = 1
            else:
                iname, itype, isize = item
                isize = np.prod(isize)
            iname = iname.strip()
            itype = itype.strip()
            datatype += "%s:%s:%d/" % (itype,iname,isize)
    elif dtype.startswith("("):
        itype, isize = eval(dtype)
        isize = np.prod(isize)
        datatype += "%s::%d/" % (itype,isize)
    else:
        datatype += "%s/" % (dtype)
    return Datatype(datatype[:-1])

def ndarray_to_Buffer(array):
    """Convert a numpy array into a Buffer"""

    from gsp.backend.reference.core.buffer import Buffer

    if (isinstance(array, np.ndarray)):
        datatype = dtype_to_Datatype(array.dtype)
        return Buffer(array.size, datatype, array.tobytes())
    raise ValueError(f"Unknown type for {array}, cannot convert to Buffer")


def ndarray_to_bytes(array):
    """Convert a numpy array to bytes"""

    if (isinstance(array, np.ndarray)):
        return array.tobytes()
    raise ValueError(f"Unknown type for {array}, cannot convert to bytes")

def vec3_to_Buffer(array):
    """Convert a numpy vec3 array to Buffer"""
    
    return array.gsp_buffer

def vec4_to_Buffer(array):
    """Convert a numpy vec4 array to Buffer"""
    
    return array.gsp_buffer

