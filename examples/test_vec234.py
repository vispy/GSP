# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import pytest
import numpy as np
from glm.types import vec2, vec3, vec4

def test_creation():
    Z = vec2(10)
    assert(Z.shape == (10,2))
    assert(Z.dtype == np.float32)

    Z = vec3(10)
    assert(Z.shape == (10,3))
    assert(Z.dtype == np.float32)

    Z = vec4(10)
    assert(Z.shape == (10,4))
    assert(Z.dtype == np.float32)

def test_view():
    Z = np.zeros(2*10, np.float32).view(vec2)
    assert(Z.shape == (10,2))

    Z = np.zeros(3*10, np.float32).view(vec3)
    assert(Z.shape == (10,3))

    Z = np.zeros(4*10, np.float32).view(vec4)
    assert(Z.shape == (10,4))

def test_swizzle():
    Z1 = vec2(10)
    Z1.xy = 1,2
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 1, 2
    assert(np.array_equal(Z1, Z2))

    Z1 = vec2(10)
    Z1.xy = 2,1
    Z1.xy = Z1.yx
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 1, 2
    assert(np.array_equal(Z1, Z2))

    Z1 = vec2(10)
    Z1.xy = 1,2
    Z1.xy = Z1.yy
    Z2 = np.ones((10,2), dtype=np.float32)
    Z2[:,0], Z2[:,1] = 2, 2
    assert(np.array_equal(Z1, Z2))

    Z1 = vec2(10)
    Z1.xy = np.ones((10,2), dtype=np.float32)
    Z2 = np.ones((10,2), dtype=np.float32)
    assert(np.array_equal(Z1, Z2))

    Z1 = vec3(10)
    Z1.xyz = np.ones((10,3), dtype=np.float32)
    Z2 = np.ones((10,3), dtype=np.float32)
    assert(np.array_equal(Z1, Z2))
    
    
    
# #print(Z.ntype)
# #print(Z.dirty)
# Z.clear()
# Z.x = 1
# #Z.y = 1
# # Z.z = 1
# # Z[:,1] = 1
# #print(Z.dirty)

# #Z[...] = 1,2,3
# # Z.xyz = 3,2,1
# print(Z)
# print(Z.dirty)

# # Z.xyz = 3,2,1
# # Z.r = Z.x
# # Z + Z
# # Z.x += 5

# # # print(Z.modified)
# # #print(Z)
# # Z = np.zeros((10,3),dtype=np.float32).view(vec3)
# # print(Z.dtype)

# # Z[...] = 1,2,3
# # print(Z.xzz)

# # M = mat3x3()
# # print(M)
