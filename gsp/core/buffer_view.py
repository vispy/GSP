# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union
from typeguard import typechecked

from gsp.core.object import OID, Object
from gsp.core.command import command
from gsp.core.buffer import Buffer

class BufferView(Object):

    @typechecked
    @command("")
    def __init__(self, buffer : Buffer,
                       key : str):

        """Partial view of an existing `buffer` indexed by `key`.
        
        === "Python"

            ```Python
            import struct
            data = [0,0,1,1,2,2]
            data = struct.pack("f"*len(data), *data)
            vec3 = Datatype("f:x/f:y")
            buffer = Buffer(3, vec3, data)
            view = BufferView(buffer, "x")
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "BufferView",
	        "params": {
                    "buffer": 1,
                    "key" : "x",
                }
	    }
            ```
        

        Parameters:

         buffer:
        
            Buffer to take view from

         key:
        
            Field to be accessed

        
        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object

        **Future**{: .future}

          No dicussion for the time being.
        """

        
        Object.__init__(self)
        self.buffer = buffer
        self.key = key
    
    def __repr__(self):
        return f'BufferView [id={self.id}]: Buffer[id={self.array.id}]["{self.key}"]'


