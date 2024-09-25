# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
import pytest
import numpy as np
from gsp.glm import *
from gsp.glm import ndarray


def test_dtypes():
    assert(ndarray.mat2_t(np.float32).base == np.float32)
    assert(ndarray.mat2_t(np.float32).shape == (2,2))
    assert(ndarray.mat3_t(np.float32).base == np.float32)
    assert(ndarray.mat3_t(np.float32).shape == (3,3))
    assert(ndarray.mat4_t(np.float32).base == np.float32)
    assert(ndarray.mat4_t(np.float32).shape == (4,4))

def test_default_type():
    assert(mat2().dtype == np.float32)
    assert(mat3().dtype == np.float32)
    assert(mat4().dtype == np.float32)

def test_default_shape():
    assert(mat2().shape == (2,2))
    assert(mat3().shape == (3,3))
    assert(mat4().shape == (4,4))

def test_ctype():
    assert(bmat2(1).dtype == np.ubyte)
    assert(bmat3(1).dtype == np.ubyte)
    assert(bmat4(1).dtype == np.ubyte)

def test_shape():
    assert(mat2(10).shape == (10,2,2))
    assert(mat3(10).shape == (10,3,3))
    assert(mat4(10).shape == (10,4,4))

    assert(mat2((3,3)).shape == (3,3,2,2))
    assert(mat3((3,3)).shape == (3,3,3,3))
    assert(mat4((3,3)).shape == (3,3,4,4))
