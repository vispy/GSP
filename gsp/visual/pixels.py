# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union
from typeguard import typechecked

from gsp.core.object import OID, Object
from gsp.core.command import command

class Pixels(Object):


    @typechecked
    @command("")
    def __init__(self, viewport : Viewport,
                       vertices : Buffer,
                       colors   : Buffer ):

        """Request the creation several colored pixels whose positions
        are given by `vertices` and colors by `colors.
        
        === "Python"

            ```Python
        
            canvas = Canvas(512, 512, 100, 1, False)
            viewport = Viewport(canvas, 0, 0, 512, 512)
            vertices = Buffer.from_numpy(np.random.uniform(0, 512, (100,2)))
            colors = Buffer.from_numpy(np.random.uniform(0, 512, (100,4)))
            pixels = Pixels(viewport, vertices, colors)
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Pixels",
	        "params": {
                    "viewport": 2,
                    "vertices" : 4,
                    "colors" : 6
                }
	    }
            ```
        
        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `CREATE`     | 3            | :material-check: | :material-check: |


        Parameters:

         viewport:
        
            Viewport to use to display pixels

         vertices:
        
            Pixel positions as (x,y,z)

         colors:
        
            Pixel colors as (r,g,b,a)

        
        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object

        **Future**{: .future}

        No discussion for the time being.

        """
        
        Object.__init__(self)
        self.viewport = viewport
        self.vertices = vertices
        self.colors = colors

    def __repr__(self):
        return f"Buffer [id={self.id}]: {self.viewport},{self.vertices},{self.colors}"
