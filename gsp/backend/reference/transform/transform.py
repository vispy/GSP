# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from __future__ import annotations
from gsp.backend.reference.core import Buffer
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.transform.operator import Operator

class Transform(Object):

    @command("transform.Transform")
    def __init__(self, base : Transform = None,
                       next : Transform = None,
                       buffer : Buffer = None):
        """A Transform allows to apply an arbitratry transformation to
        a buffer. Any transform can be bound to a specific buffer and
        used in place of a Buffer where needed. Several transforms can
        be chained or composed together.

        Parameters:

         base:
        
           The base transform this transform is based on. When non
           null, all transform parameters are read from the base.

         next:
        
           A transformation can be chained with another transform
           (`next`). In such case, the **`next` transform is applied
           first** and result is passed to the current transform.

         buffer:

           Buffer on which to apply the transform. When non null, the
           transformation is bound and cannot be modified anymore.

        """
        
        Object.__init__(self)
        self._base = base
        self._buffer = buffer
        self._next = next

    @command()
    def set_base(self, base : Transform = None):
        """Set a new base for the transform

           Parameters:

            base:
        
             The base transform this transform is based on
        """
        
        self._base = base

    @command()
    def set_next(self, next : Transform = None):
        """Compose transform with `next` that will be applied before
        this one.

        Parameters:

         next:

          Next transform

        """

        self._next = next
        
    @command()
    def set_buffer(self, buffer : Buffer = None):
        """Bind the transform to the given buffer.

        Parameters:

         buffer:

          Buffer to bind
        """

        self._buffer = buffer

    @property
    def base(self):
        if self._base:
            return self._base.base
        return self

    @property
    def buffer(self):
        """Bound buffer"""
        return self._buffer
    
    @property
    def next(self):
        """Next transform"""
        return self._next
    
    @property
    def last(self):
        """Last transform in the chain"""
            
        last = self
        while last._next: last = last._next
        return last

    @property
    def bound(self):
        """Bound buffer (if any)"""
        
        return self.last.buffer 

    def copy(self):
        """Shallow copy"""
        
        transform = self.__class__()
        transform.set_buffer(self._buffer)
        transform.set_base(self.base)
        if self._next:
            transform.set_next(self._next.copy())
        return transform

    def __call__(self, other):
        """Chain self with other"""

        transform = self.copy()
        if isinstance(other, Transform):
            transform.set_next(other.copy())
            transform.set_buffer(None)
        elif isinstance(other, Buffer):
            if self.bound:
                raise ValueError("Transform is already bound")
            transform.last.set_buffer(other)
        return transform

    def __add__(self, other):
        return Operator("+", self, other)

    def __sub__(self, other):
        return Operator("-", self, other)

    def __mul__(self, other):
        return Operator("*", self, other)

    def __div__(self, other):
        return Operator("/", self, other)

