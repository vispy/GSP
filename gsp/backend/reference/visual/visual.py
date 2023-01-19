# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.core import Object

class Visual(Object):
    def __init__(self):
        Object.__init__(self)

    def __repr__(self):
        return f"Visual [id={self.id}]"

    
