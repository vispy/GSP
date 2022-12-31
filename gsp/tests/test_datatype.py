# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp
import numpy as np
from gsp.core import Datatype

def test_simple_type():
    gsp.mode("client", reset=True)
    datatype = Datatype("f:x:1/f:y:1/f:z:1/f:w:1")
    assert repr(datatype) ==  "Type [id=1]: f:x:1/f:y:1/f:z:1/f:w:1"

def test_size():
    gsp.mode("client", reset=True)
    datatype = Datatype("f:x:1/f:y:1/f:z:1/f:w:1")
    assert datatype.size == 16

def test_numpy_type():

    gsp.mode("client", reset=True)
    datatypes = {
        "RGB":  Datatype("u:r:1/u:g:1/u:b:1"),
        "RGBA": Datatype("u:r:1/u:g:1/u:b:1/u:a:1"),
        "ARGB": Datatype("u:a:1/u:r:1/u:g:1/u:b:1"),
        
        "rgb":  Datatype("f:r:1/f:g:1/f:b:1"),
        "rgba": Datatype("f:r:1/f:g:1/f:b:1/f:a:1"),
        "argb": Datatype("f:a:1/f:r:1/f:g:1/f:b:1"),

        "ivec2": Datatype("i::2"),
        "ivec3": Datatype("i::3"),
        "ivec4": Datatype("i::4"),

        "vec2": Datatype("f::2"),
        "vec3": Datatype("f::3"),
        "vec4": Datatype("f::4"),
                  
        "xy":   Datatype("f:x:1/f:y:1"),
        "xyz":  Datatype("f:x:1/f:y:1/f:z:1"),
        "xyzw": Datatype("f:x:1/f:y:1/f:z:1/f:w:1"),

        "mat2x2": Datatype("f::4"),
        "mat3x3": Datatype("f::9"),
        "mat4x4": Datatype("f::16") }

    for key in datatypes.keys():
        d1 = datatypes[key].dtype
        d2 = Datatype.from_numpy(Datatype.to_numpy(d1)).dtype
        assert d1==d2
    

    
