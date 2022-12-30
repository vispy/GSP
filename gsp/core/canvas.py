# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
The Canvas corresponds to a finite two-dimensional drawing area.
"""
from typing import Union
from typeguard import typechecked
from gsp.core.command import command
from gsp.core.object import Object, OID

class Canvas(Object):
    """ """
        
    @typechecked
    @command("")
    def __init__(self, width :     int, 
                       height :    int,
                       dpi :       float,
                       dpr :       float,
                       offscreen : bool):
        """Request the creation of a two-dimensional drawing area (that can be
        `offscreen`) of size `width` × `height` logical pixels using specified
        `dpi` (dots per inch) and `dpr` (device pixel ratio). The resulting
        canvas uses a standard color space
        ([sRGBA](https://en.wikipedia.org/wiki/SRGB)) with at least 8 bits per
        channel.

        === "Python"

            ```Pycon
            >>> canvas = Canvas(800, 400, 100, 2, True)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Canvas",
	        "params": {
                    "width" : 800,
                    "height" : 400,
                    "dpi" : 100,
                    "dpr" : 2,
                    "offscreen" : false
                }
	    }
            ```

        === "Result"

            ![](../../assets/images/Canvas.svg){: style="width:100%"}
        
        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `CREATE`     | 5            | :material-check: | :material-check: |

        Parameters:

          width:
        
            Width of the drawing area in pixels.

            **→** `width` must be striclty greater than zero.

          height:
        
            Height of the drawing area in pixels.

            **→** `height` must be striclty greater than zero.

          dpi:
            Dots per inch

            **→** `dpi` must be striclty greater than zero.

          dpr:
            Device pixel ratio

            **→** `dpr` must be striclty greater than zero.

          offscreen:
            Flag indicatng whether canvas is offscreen or not

            **→** `offscreen` can only be set at creation time.

        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value

        **Future**{: .future}

        No dicussion at the moment.

        """
        
        Object.__init__(self)
        self.width = width
        self.height = height
        self.dpi = dpi
        self.dpr = dpr
        self.offscreen = offscreen
        

    @typechecked        
    @command("set_size")
    def set_size(self, width :  int,  
                       height : int):
        """
        Set a new size for the canvas.

        === "Python"

            ```Pycon
            >>> canvas = Canvas(16, 8, 100, 2, True)
            >>> canvas.set_size(16,16)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 2,
                "timestamp": 0,
                "method": "Canvas/set_size",
	        "params": {
                    "id": 1,
                    "width" : 16,
                    "height" : 8,
                }
	    }
            ```
        
        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `UPDATE`     | 2            | :material-check: | :material-check: |

        Parameters:

          id (int):

            Identification of the object 

            **→** Object must have been created.
        
          width:
        
            Width of the canvas in logical pixels.

            **→** `width` must be striclty greater than zero.

          height:
        
            Height of the canvas in logical pixels.

            **→** `height` must be striclty greater than zero.


        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object        
        """

        self.width = width
        self.height = height

    @typechecked        
    @command("set_dpi")
    def set_dpi(self, dpi : float) :
        """
        Set the dots per inch.

        === "Python"

            ```Pycon
            >>> canvas = Canvas(16, 8, 100, 2, True)
            >>> canvas.set_dpi(100)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 2,
                "timestamp": 0,
                "method": "Canvas/set_dpi",
	        "params": {
                    "id": 1,
                    "dpi" : 100,
                }
	    }
            ```


        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `UPDATE`     | 1            | :material-check: | :material-check: |
        
        Parameters:

          id (int):

            Identification of the object 

            **→** Object must have been created.
        
          dpi:
        
            Dots per inch

            **→** `dpi` must be striclty greater than zero.

        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object
        """
        self.dpi = dpi

    @typechecked
    @command("set_dpr")
    def set_dpr(self, dpr : float) :
        """
        Set the device pixel ratio.

        === "Python"

            ```Pycon
            >>> canvas = Canvas(16, 8, 100, 2, True)
            >>> canvas.set_dpr(100)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 2,
                "timestamp": 0,
                "method": "Canvas/set_dpi",
	        "params": {
                    "id": 1,
                    "dpr" : 100,
                }
	    }
            ```

        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `UPDATE`     | 1            | :material-check: | :material-check: |
        
        Parameters:

          dpr:
        
            Device pixel ratio

            **→** `dpr` must be striclty greater than zero.

        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object
        """
        
        self.dpr = dpr

    def __repr__(self):
        return f"Canvas [id={self.id}]: {self.width},{self.height},{self.dpi},{self.dpr}"
