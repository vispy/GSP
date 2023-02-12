# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from gsp.converters import str_to_dtype
from gsp.converters import dtype_to_str

def test_dtype_to_str_float():

    dt_str = "<f4::1"
    dt_numpy  = np.dtype(np.float32)
    assert(dt_str == dtype_to_str(dt_numpy))

    dt_str = "<f4::1"
    dt_numpy = np.dtype("<f4")
    assert(dt_str == dtype_to_str(dt_numpy))

    dt_str = "<f4::1"
    dt_numpy = np.dtype("f")
    assert(dt_str == dtype_to_str(dt_numpy))

    dt_str = "<f4:x:1"
    dt_numpy = np.dtype([("x", np.float32)])
    assert(dt_str == dtype_to_str(dt_numpy))

    dt_str = "<f4::4"
    dt_numpy = np.dtype((np.float32,4))
    assert(dt_str == dtype_to_str(dt_numpy))

    dt_str = "<f4::16"
    dt_numpy = np.dtype((np.float32,(4,4)))
    assert(dt_str == dtype_to_str(dt_numpy))

def test_str_to_dtype_float():

    dt_str = "f::"
    dt_numpy = np.dtype(np.float32)
    assert(dt_numpy == str_to_dtype(dt_str))

    dt_str = "f4::"
    dt_numpy =  np.dtype(np.float32)
    assert(dt_numpy == str_to_dtype(dt_str))

    dt_str = "<f4::"
    dt_numpy = np.dtype(np.float32)
    assert(dt_numpy == str_to_dtype(dt_str))

    dt_str = "<f4::1"
    dt_numpy = np.dtype(np.float32)
    assert(dt_numpy == str_to_dtype(dt_str))

    dt_str = "<f4::16"
    dt_numpy = np.dtype((np.float32,16))
    assert(dt_numpy == str_to_dtype(dt_str))

    dt_str = "<f4:x:"
    dt_numpy = np.dtype([("x", np.float32)])
    assert(dt_numpy == str_to_dtype(dt_str))

def test_dtype_to_str_vec2():

    dt_str = "<f4:x:1,<f4:y:1"
    dt_numpy = np.dtype([("x", np.float32),
                         ("y", np.float32)])
    assert(dt_str == dtype_to_str(dt_numpy))

def test_str_to_dtype_vec2():

    dt_str = "<f4:x:,<f4:y:"
    dt_numpy = np.dtype([("x", np.float32),
                         ("y", np.float32)])
    assert(dt_numpy == str_to_dtype(dt_str))

def test_dtype_to_str_vec3():

    dt_str = "<f4:x:1,<f4:y:1,<f4:z:1"
    dt_numpy = np.dtype([("x", np.float32),
                         ("y", np.float32),
                         ("z", np.float32)])
    assert(dt_str == dtype_to_str(dt_numpy))

def test_str_to_dtype_vec3():

    dt_str = "<f4:x:,<f4:y:,<f4:z:"
    dt_numpy = np.dtype([("x", np.float32),
                         ("y", np.float32),
                         ("z", np.float32)])
    assert(dt_numpy == str_to_dtype(dt_str))

def test_dtype_to_str_vec4():

    dt_str = "<f4:x:1,<f4:y:1,<f4:z:1,<f4:w:1"
    dt_numpy = np.dtype([("x", np.float32),
                         ("y", np.float32),
                         ("z", np.float32),
                         ("w", np.float32)])
    assert(dt_str == dtype_to_str(dt_numpy))

def test_str_to_dtype_vec4():

    dt_str = "<f4:x:,<f4:y:,<f4:z:,<f4:w:"
    dt_numpy = np.dtype([("x", np.float32),
                         ("y", np.float32),
                         ("z", np.float32),
                         ("w", np.float32)])
    assert(dt_numpy == str_to_dtype(dt_str))

def test_dtype_to_str_mat4x4():
    dt_str = "<f4::16"
    dt_numpy = np.dtype((np.float32, (4,4)))
    assert(dtype_to_str(dt_numpy) == dt_str)

# @pytest.mark.xfail
def test_str_to_dtype_mat4x4():
    dt_str = "<f4::16"
    dt_numpy = np.dtype((np.float32, (4,4)))
    assert(str_to_dtype(dt_str) == dt_numpy)

