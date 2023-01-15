# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from typing import Union
from GSP import OID, Object, command
from typeguard import typechecked
from array import Array

class MatrixTransform(Object):

    datatype = Datatype("f::16")
    
    @typechecked
    @command("")
    def __init__(self,
                 data : bytes):
        
        Object.__init__(self)
        self.buffer = (16, self.datatype, data)
        

    def __repr__(self):
        return f"MatrixTransform [id={self.id}]"

