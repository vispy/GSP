# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import Buffer, Color
from gsp.transform import Transform
from gsp.io.command import command

class Points(Visual):
    """
    Points are discs with a given size (diameter) and posses a
    surface that can be filled and stroked. They always face the
    viewer such that their rendered shape is a disc, independentely of
    any transform.

    ??? note "IN/OUT variables "
        ```glsl

        // Rendering stage 1
        in uniform vec4 viewport;                    // in("viewport")
        in attribute [ vec2 | vec3 ] positions;      // in("positions")
        in [ attribute | uniform ] float sizes;      // in("sizes")
        in [ attribute | uniform ] vec4 fill_colors; // in("fill_colors")
        in [ attribute | uniform ] vec4 line_colors; // in("line_colors")
        in [ attribute | uniform ] vec4 line_widths; // in("line_widths")

        // Rendering stage 2
        out attribute vec3 screen;              // out("screen[positions]")

        // Rendering stage 3
        out attribute float sizes;             // out("sizes")
        out attribute vec4  fill_colors;       // out("fill_colors")
        out attribute vec4  line_colors;       // out("line_colors")
        out attribute float line_widths;       // out("line_widths")
        ```

    ```bash exec="1"
    python docs/snippets/Points_init.py
    ```
    """

    @command("visual.Points")
    def __init__(self, positions   : Transform | Buffer,
                       sizes       : Transform | Buffer | float,
                       fill_colors : Transform | Buffer | Color,
                       line_colors : Transform | Buffer | Color,
                       line_widths : Transform | Buffer | float):
        """
        Create a visual of n points at given *positions* with
        given *sizes*, *flll_colors*., *line_colors* and
        *line_widths*.

        Parameters
        ----------
        positions : Transform | Buffer
            Points position (vec3)
        sizes : Transform | Buffer | Measure
            Point sizes (float)
        fill_colors : Transform | Buffer | Color
            Points fill colors (vec4)
        line_colors : Transform | Buffer | Color
            Points line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Points line colors (vec4)
        """

        super().__init__()

        # These variables are available prior to rendering and may be
        # tracked
        self._in_variables = {
            "positions" : positions,
            "sizes" : sizes,
            "fill_colors" : fill_colors,
            "line_colors" : line_colors,
            "line_widths" : line_widths,
            "viewport" : None
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        n = len(positions)
        self._out_variables = {
            "screen[positions]" : np.empty((n,3), np.float32),
            "sizes" :             np.empty(n, np.float32),
            "fill_colors" :       np.empty((n,4), np.float32),
            "line_colors" :       np.empty((n,4), np.float32),
            "line_widths" :       np.empty(n, np.float32),
        }
