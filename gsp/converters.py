# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np

def dtype_to_str(dt):
    if dt.names:
        elements = []
        for name in dt.names:
            size = int(np.prod(dt[name].shape))
            type = dt[name].base.str
            elements.append (f"{type}:{name}:{size}")
        return ",".join(elements)
    else:
        size = int(np.prod(dt.shape))
        type = dt.base.str
        return f"{type}::{size}"

def str_to_dtype(desc):
    dt = []
    elements = desc.split(",")
    for element in elements:
        type,name,size = element.split(":")
        if name :
            if size and int(size) > 1:
                dt.append((name, type, int(size)))
            else:
                dt.append((name, type))
        else:
            if size and int(size) > 1:
                dt.append((type, int(size)))
            else:
                dt.append(type)
    if len(dt) == 1 and not len(name):
        dt = dt[0]
    return np.dtype(dt)


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

def Datatype_to_dtype(datatype):
    dtype = []
    datatype = datatype.replace(" ", "")
    for item in datatype.split("/"):
        if not len(item): continue
        item = item.split(":")
        if len(item) == 3:
            itype, iname, isize = item
            if not len(iname):
                dtype.append((itype, (int(isize),)))
            else:
                dtype.append((iname, itype, (int(isize),)))
        elif len(item) == 2:
            itype, iname = item
            dtype.append((iname, itype, (1,)))
        elif len(item) == 1:
            itype = item[0]
            dtype.append((itype, (1,)))
    if len(dtype) == 1:
        dtype = dtype[0]
        if len(dtype) == 3:
            return np.dtype(dtype[1:])
        else:
            return np.dtype(dtype)
    else:
        return np.dtype(dtype)


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

def mat4x4_to_Mat4x4(array):
    """Convert a numpy mat4x4 array to Buffer"""

    from gsp.backend.reference.transform import Mat4x4
    return Mat4x4(array.tobytes())

