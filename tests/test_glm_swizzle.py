# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
import pytest
import numpy as np
from gsp.glm import vec2, vec3, vec4

def test_ordered():
    Z1 = vec2(10)
    Z1.xy = 1,2
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 1, 2
    assert(np.array_equal(Z1, Z2))

def test_unordered():
    Z1 = vec2(10)
    Z1.yx = 2,1
    print(Z1)
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 1, 2
    assert(np.array_equal(Z1, Z2))

def test_rgba():
    Z1 = vec4(10)
    Z1.rgba = 1,2,3,4
    Z2 = np.ones((10,4), dtype=np.float32)
    Z2[:] = 1, 2,3,4
    assert(np.array_equal(Z1, Z2))

def test_mix():
    Z1 = vec4(10)
    Z1.xyba = 1,2,3,4
    Z2 = np.ones((10,4), dtype=np.float32)
    Z2[:] = 1, 2,3,4
    assert(np.array_equal(Z1, Z2))

def test_set_1():
    Z1 = vec2(10)
    Z1.x = 1*np.ones(10)
    Z1.y = 2*np.ones(10)
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:] = 1,2
    assert(np.array_equal(Z1, Z2))

def test_set_2():
    Z1 = vec2(10)
    Z1.x = np.arange(10)
    Z1.y = 2*np.arange(10)
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0] = np.arange(10)
    Z2[:,1] = 2*np.arange(10)
    assert(np.array_equal(Z1, Z2))

def test_set_3():
    Z1 = vec2(10)
    Z1.xy = np.arange(10), 2*np.arange(10)
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0] = np.arange(10)
    Z2[:,1] = 2*np.arange(10)
    assert(np.array_equal(Z1, Z2))

def test_set_4():
    Z1 = vec2(10)
    Z1.xy = np.arange(20).reshape(10,2)
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[...] = np.arange(20).reshape(10,2)
    assert(np.array_equal(Z1, Z2))

def test_repeated_target():
    Z1 = vec2(10)
    Z1.xy = 1,2
    Z1.xy = Z1.yy
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 2, 2
    assert(np.array_equal(Z1, Z2))

def test_repeated_source():
    Z1 = vec2(10)
    Z1.xxy = 1,2,0
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 2, 0
    assert(np.array_equal(Z1, Z2))

def test_multidimensional():

    Z = vec4(10)
    Z[1].z = 1
