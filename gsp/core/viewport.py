# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from typing import Union
from typeguard import typechecked

from gsp.core.object import OID, Object
from gsp.core.command import command
from gsp.core.canvas import Canvas

class Viewport(Object):

    @typechecked
    @command("")
    def __init__(self, canvas : Canvas,
                       x :      int,
                       y :      int,
                       width :  int,
                       height : int):

        """Request the creation of a two-dimensional viewport at `x`, `y`
        coordinates with size equal to `width` × `height` logical pixels.
        Viewport needs to be fully contained inside the canvas. When several
        viewports are created, they are rendered in the order of their
        declaration.
        
        === "Python"

            ```Pycon
            >>> canvas = Canvas(800, 400, 100, 1, False)
            >>> viewport = Viewport(canvas, 100, 100, 300, 200, 1)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Viewport",
	        "params": {
                    "canvas": 1,
                    "x" : 100,
                    "y" : 100,
                    "width" : 300,
                    "height" : 200,
                }
	    }
            ```

        === "Result"

            ![](../../assets/images/Viewport.svg){: style="width:100%"}

        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `CREATE`     | 5            | :material-check: | :material-check: |

        Parameters:

          canvas:
        
            Canvas where to create the viewport

            **→** `canvas` must have been created

          x:
        
            X coordinate of the viewport bottom left corner

            **→** Assert `0 <= x < canvas.width - 1`
        
          y:
        
            Y coordinate of the viewport bottom left corner

            **→** Assert `0 <= y < canvas.height - 1`
        
          width:

            Width of the viewport in logical pixels.

            **→** Assert `0 < width <= canvas.width - x`
        
          height:

            Height of the viewport in logical pixels.

            **→** Assert `0 < height <= canvas.height - y`

        
        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object

        **Future**{: .future}

          - Viewports can be equipped with a rendering order :octicons-comment-discussion-16:
          - Viewports can be equipped with a transform :octicons-comment-discussion-16:

        """
        
        Object.__init__(self)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @typechecked
    @command("set_position")
    def set_position(self, x : int,
                           y : int):
        """Set a new position `x`, `y` for the viewport bottom left corner.

        === "Python"

            ```Pycon
            >>> canvas = Canvas(200, 200, 100, 1, False)
            >>> viewport = Viewport(canvas, 10, 10, 100, 100, 1)
            >>> viewport.set_position(0,0)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Viewport/set_position",
	        "params": {
                    "id": 2,
                    "x" : 0,
                    "y" : 0,
                }
	    }
            ```
        
        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `UPDATE`     | 3            | :material-check: | :material-check: |

        Parameters:

          id (int):

            Identification of the viewport.

            **→** Viewport must have been created.

          x:
        
            X coordinate of the bottom left corner

          y:
        
            Y coordinate of the bottom left corner


        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object
        """

        self.x = x
        self.y = y

    
    @typechecked
    @command("set_size")
    def set_size(self, width :  int,
                       height : int):
        """Set a new size `witdh` × `height` for the viewport.

        !!! Note

            Coordinates can be negative or beyond canvas limits such that a
            viewport can be fully outside the canvas area and won't be rendered.

        === "Python"

            ```Pycon
            >>> canvas = Canvas(200, 200, 100, 1, False)
            >>> viewport = Viewport(canvas, 10, 10, 100, 100, 1)
            >>> viewport.set_size(50,50)
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Viewport/set_size",
	        "params": {
                    "id": 2,
                    "width" : 50,
                    "height" : 50,
                }
	    }
            ```

        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `UPDATE`     | 3            | :material-check: | :material-check: |

        Parameters:

          id (int):

            Identification of the viewport.

            **→** Viewport must have been created.

          width:

            Width of the viewport in logical pixels.

          height:

            Height of the viewport in logical pixels.

        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value
          - `INVALID_OBJECT`  : A parameter refers to a non-existent object
        """
        
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Viewport [id={self.id}]: {self.x},{self.y},{self.width},{self.height}"
