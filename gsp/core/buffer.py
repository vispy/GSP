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

    # Convenience method, not part of the protocol
    @classmethod
    def from_numpy(cls, Z):
        import numpy as np
        
        if (isinstance(Z, np.ndarray)):
            return Buffer(Z.size, Datatype.from_numpy(Z.dtype), Z.tobytes())
        raise ValueError(f"Unknown type for {Z}, cannot convert to Buffer")

    @typechecked
    @command("")
    def __init__(self, count : int,
                       dtype : Datatype,
                       data  : bytes):

        """Request the creation of a uni-dimensional buffer with `count`
        elements of type `dtype` and `data` content.
        
        === "Python"

            ```Python
            import struct
            data = [0,0,1,1,2,2]
            data = struct.pack("f"*len(data), *data)
            vec3 = Datatype("f:x/f:y")
            buffer = Buffer(3, vec3, data)
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
                    "dtype" : 1,
                    "data" : "AAAAAAAAAAAAIA/AACAPwAAAEAAAABA" 
                }
	    }
            ```
        
        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `CREATE`     | 3            | :material-check: | :material-check: |


        Parameters:

         count:
        
            Number of elements

         dtype:
        
            Element datatype

         data:
        
            Content of the buffer

        
        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object

        **Future**{: .future}

          - Arrays can be partitionned :octicons-comment-discussion-16:

        """
        
        Object.__init__(self)
        self.count = count
        self.dtype = dtype
        self.data = data

    def __repr__(self):
        return f"Buffer [id={self.id}]: {self.count},{self.dtype}"
