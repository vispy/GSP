# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from glm.types import mtarray

def check(Z):
    assert(Z.dirty == (min(Z.ravel().view(np.byte).nonzero()[0]),
                       max(Z.ravel().view(np.byte).nonzero()[0]+1)))

def zeros(shape, dtype):
    Z = mtarray(shape, dtype=dtype)
    Z[...] = 0
    Z.clear()
    return Z

def test_ellipis():
    Z = zeros(9, np.byte)
    Z[...] = 1.123; check(Z)

    Z = zeros(9, np.float32)
    Z[...] = 1.123; check(Z)

    Z = zeros((3,3), np.byte)
    Z[...] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[...] = 1.123; check(Z)

def test_first_item():
    Z = zeros(9, np.byte)
    Z[0] = 1.123; check(Z)

    Z = zeros(9, np.float32)
    Z[0] = 1.123; check(Z)

    Z = zeros((3,3), np.byte)
    Z[0,0] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[0,0] = 1.123; check(Z)

def test_last_item():
    Z = zeros(9, np.byte)
    Z[-1] = 1.123; check(Z)

    Z = zeros(9, np.float32)
    Z[-1] = 1.123; check(Z)

    Z = zeros((3,3), np.byte)
    Z[-1,-1] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[-1,-1] = 1.123; check(Z)
    
def test_1d_slice():
    Z = zeros(9, np.float32)
    Z[1:] = 1.123; check(Z)

    Z = zeros(9, np.float32)
    Z[:-1] = 1.123; check(Z)

    Z = zeros(9, np.float32)
    Z[2:3] = 1.123; check(Z)

def test_2d_slice():
    Z = zeros((3,3), np.float32)
    Z[1:,1:] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[:-1,:-1] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[2:3,2:3] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[1,:] = 1.123; check(Z)

    Z = zeros((3,3), np.float32)
    Z[:,-1] = 1.123; check(Z)
    
def test_structured_type():
    Z = zeros((3,3), [("x", np.float32), ("y", np.byte)])
    Z["x"] = 1.123; check(Z)

    Z = zeros((3,3), [("x", np.float32), ("y", np.byte)])
    Z["y"] = 1; check(Z)

def test_inplace_modifications():
    Z = zeros(9, np.float32)
    Z += 1.123; check(Z)

    Z = zeros(9, np.float32)
    Z[2:-2] += 1.123; check(Z)

    Z = zeros((3,3), [("x", np.float32), ("y", np.byte)])
    Z["x"] += 1.123; check(Z)

    Z = zeros((3,3), [("x", np.float32), ("y", np.byte)])
    Z["y"] -= 1; check(Z)

    Z = zeros((3,3), [("x", np.float32), ("y", np.byte)])
    Z["x"][1:2] += 1.123; check(Z)

def test_fancy_indexing():
    Z = zeros(9, np.float32)
    with pytest.raises(NotImplementedError):
        Z[[1]] = 1.123

