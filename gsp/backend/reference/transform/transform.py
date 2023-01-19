# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
# See https://stackoverflow.com/questions/33533148
from __future__ import annotations
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core import Buffer


class Transform(Object):

    def __init__(self):
        """A Transform allows to apply a transformation to a
        buffer. This transformation is specific to each transform but
        any transform can be bound to a specific buffer and used in
        place of a Buffer where needed. Several transforms can be
        chained.

        """
        
        Object.__init__(self)
        self.buffer = None
        self.next = None
        

    def bind(self, buffer : Buffer) -> Transform:

        """Bind the transform to the given buffer and return a
        new bound Transform.
        
        Parameters:

         buffer:
        
            Buffer to bind

        """

        _transform = self.copy()
        _transform.buffer = buffer
        return _transform

    def chain(self, transform : Transform) -> Transform:

        """Chain the current transform with the given transform that
        will be applied after this one.
        
        Parameters:

         transform:
        
            Transform to be chain.

        """

        _transform = self.copy()
        _transform.next = transform
        return _transform

