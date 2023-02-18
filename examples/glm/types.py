# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
""" Convenient numpy types that are GSP aware. """
import gsp
import numpy as np

class mtarray(np.ndarray):
    """Memory Tracked Array"""

    def __new__(cls, *args, **kwargs):
        Z = np.ndarray.__new__(cls, *args, **kwargs)
        if gsp.mode and gsp.mode.startswith("client"):
            Z.gsp_buffer = gsp.core.Buffer(len(Z), Z.ntype, Z.tobytes())
            Z.gsp_update = False
        return Z

    def __array_finalize__(self, obj):
        if not isinstance(obj, mtarray):
            self._extents = 0, self.size*self.itemsize
            self.__class__.__init__(self)
            self._dirty = self._extents
        else:
            self._extents = obj._extents

    def clear(self):
        """ Clear dirty region"""

        if isinstance(self.base, mtarray):
            self.base._dirty = None
        elif self._dirty:
            self._dirty = None

    @property
    def dirty(self):
        """ Dirty region as (start, stop) in bytes """

        if isinstance(self.base, mtarray):
            return self.base.dirty
        elif self._dirty:
            return self._dirty
        return None

    def _update(self, start, stop):
        """ Update dirty region """
        
        if isinstance(self.base, mtarray):
            self.base._update(start, stop)
        else:
            if not hasattr(self, "_dirty") or self._dirty is None:
                self._dirty = start, stop
            else:
                start = min(self._dirty[0], start)
                stop = max(self._dirty[1], stop)
                self._dirty = start, stop
            if gsp.mode and gsp.mode.startswith("client") and not self.gsp_update:
                data = self.view(np.ubyte)
                start, stop = self._dirty
                self.gsp_buffer.set_data(start, data[start:stop].tobytes())
                
    def _compute_extents(self, Z):
        """Compute extents (start, stop) in bytes in the base array"""

        if Z.base is not None:
            base = Z.base.__array_interface__['data'][0]
            view = Z.__array_interface__['data'][0]
            offset = view - base
            shape = np.array(Z.shape) - 1
            strides = Z.strides[-len(shape):]
            size = (shape*strides).sum() + Z.itemsize
            return offset, offset+size
        return 0, Z.size*Z.itemsize

    def __getitem__(self, key):
        Z = np.ndarray.__getitem__(self, key)
        if not hasattr(Z, 'shape') or Z.shape == ():
            return Z        
        Z._extents = self._compute_extents(Z)
        return Z

    def __setitem__(self, key, value):
        Z = np.ndarray.__getitem__(self, key)
        if Z.shape == ():
            key = tuple(np.mod(np.array(key), self.shape))
            offset = np.ravel_multi_index(key, self.shape, mode='wrap')*self.itemsize
            self._update(offset, offset+self.itemsize)
        # Test for fancy indexing
        elif (Z.base is not self and (isinstance(key, list) or
               (hasattr(key, '__iter__') and
                any(isinstance(k, (list,np.ndarray)) for k in key)))):
            raise NotImplementedError("Fancy indexing not supported")
        else:
            Z._extents = self._compute_extents(Z)            
            self._update(Z._extents[0], Z._extents[1])
        np.ndarray.__setitem__(self, key, value)

    def __getslice__(self, start, stop):
        return self.__getitem__(slice(start, stop))

    def __setslice__(self, start, stop,  value):
        self.__setitem__(slice(int(start), int(stop)), value)

    def __iadd__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__iadd__(self, other)

    def __isub__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__isub__(self, other)

    def __imul__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__imul__(self, other)

    def __idiv__(self, other):
        self._update(self._extents[0], self._extents[1])
        return np.ndarray.__idiv__(self, other)

    
class matrix(mtarray):
    """Generic matrix is not usable on its own. It is meant to be
    later specialized by specifying the mtype. This generic class only
    implements tracking of any modifications of the undelyring array
    using the 'modified' flag. It's the responsability of the user to
    set this flag to False when the state of the array is considered
    to be not modified anymore (e.g. after uploading it somewhere
    else)."""

    shape = None
    ntype = None
        
    def __new__(subtype, shape=1, dtype=float, buffer=None, offset=0,
                strides=None, order=None, info=None):
        obj = super().__new__(subtype, subtype.shape, np.float32,
                              buffer, offset, strides, order)
        return obj



class vector(mtarray):
    """Generic vector is not usable on its own. It is meant to be
    later specialized by specifying the vtype and the swizzle. This
    generic class only implements tracking of any modifications of the
    underlying array using the 'modified' flag. It is the
    responsability of the user to set this flag to False when the
    state of the array is considered to be not modified anymore
    (e.g. after uploading it somewhere else)."""

    swizzle = None
    vtype = None
    ntype = None

    def __new__(subtype, shape, dtype=float, buffer=None, offset=0,
                strides=None, order=None, info=None):
        obj = super().__new__(subtype, shape, subtype.vtype,
                              buffer, offset, strides, order)
        return obj
    
    
    def __setattr__(self, key, value):
        for swizzle in self.swizzle:
            if set(key).issubset(set(swizzle)):
                value = np.asarray(value)
                shape = value.shape
                indices = [swizzle.index(c) for c in key]
                self.gsp_update = True
                if not len(shape):
                    for index in indices:
                        self[...,index] = value
                elif shape[-1] == 1:
                    for index in indices:
                        self[...,index] = np.squeeze(value)
                elif shape[-1] == len(key):
                    for index in indices:
                        if self[...,index].size == value[...,index].size:
                            self[...,index] = value[...,index].reshape(self[...,index].shape)
                        else:
                            self[...,index] = value[...,index]
                else:
                    raise IndexError
                self.gsp_update = False
                if gsp.mode.startswith("client"):
                    data = self.view(np.ubyte)
                    start,stop = self._dirty
                    self.gsp_buffer.set_data(start, data[start:stop].tobytes())
                return
        super().__setattr__(key, value)

        
    def __getattr__(self, key):
        for swizzle in self.swizzle:
            if set(key).issubset(set(swizzle)):
                return self[..., [swizzle.index(c) for c in key]]
        return super().__getattribute__(key)


class vec2(vector):
    """vec2 numpy array with swizzle capacity and modification tracking."""
    swizzle = "xy",
    vtype = np.dtype((np.float32,2))
    ntype = np.dtype([("x",np.float32),
                      ("y",np.float32)])

class vec3(vector):
    """vec3 numpy array with swizzle capacity and modification tracking."""
    swizzle = "xyz", "rgb"
    vtype = np.dtype((np.float32,3))
    ntype = np.dtype([("x",np.float32),
                      ("y",np.float32),
                      ("z",np.float32)])

class vec4(vector):
    """vec4 numpy array with swizzle capacity and modification tracking."""
    swizzle = "xyzw", "rgba"
    vtype = np.dtype((np.float32,4))
    ntype = np.dtype([("x",np.float32),
                      ("y",np.float32),
                      ("z",np.float32),
                      ("w",np.float32)])

class mat2x2(matrix):
    """mat2x2 numpy array with modification tracking."""
    ntype = np.dtype((np.float32, (2,2)))
    shape = (2,2)
    
class mat3x3(matrix):
    """mat3x3 numpy array with modification tracking."""
    ntype = np.dtype((np.float32, (3,3)))
    shape = (3,3)
        
class mat4x4(matrix):
    """mat4x4 numpy array with modification tracking."""
    ntype = np.dtype((np.float32, (4,4)))
    shape = (4,4)
