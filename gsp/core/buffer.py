# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union
from typeguard import typechecked

from gsp.core.object import OID, Object
from gsp.core.command import command
from gsp.core.datatype import Datatype

class Buffer(Object):

    @typechecked
    @command("")
    def __init__(self, size : int,
                       dtype : Datatype):

        """Request the creation of a uni-dimensional array with `size`
        elements of type `dtype`.
        
        === "Python"

            ```Pycon
            >>> vec3 = Datatype("f:x / f:y / f:z")
            >>> array = Buffer(100, vec3)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Buffer",
	        "params": {
                    "size": 100,
                    "datatype" : 1,
                }
	    }
            ```

        Parameters:

         size:
        
            Number of elements

            **→** `size` is strictly positive

         dtype:
        
            Element datatype
        
        
        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object

        **Future**{: .future}

          - Arrays can be partitionned :octicons-comment-discussion-16:

        """
        
        Object.__init__(self)
        self.size = size
        self.dtype = dtype

    def __repr__(self):
        return f"Buffer [id={self.id}]: {self.size},{self.dtype}"
