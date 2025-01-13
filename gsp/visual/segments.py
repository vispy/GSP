# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import Buffer, Color, LineCap, LineJoin
from gsp.transform import Transform
from gsp.io.command import command

class Segments(Visual):
    """
    Segments are line segments between two vertices. They can be
    colored and styled (dash pattern). They possess a thickness but
    always face the viewer such that their apparent thickness is
    constant. Their end points (caps) can be styled following the SVG
    specification (butt, round or cap).

    ??? note "IN/OUT variables "
        ```glsl

        // Rendering stage 1
        in uniform vec4 viewport;                     // in("viewport")
        in attribute [ vec2 | vec3 ] positions;       // in("positions")
        in [ attribute | uniform ] int line_caps;     // in("fill_colors")
        in [ attribute | uniform ] vec4 line_colors;  // in("line_colors")
        in [ attribute | uniform ] float line_widths; // in("line_widths")

        // Rendering stage 2
        out attribute vec3 screen;                    // out("screen[positions]")
        out attribute vec3 segments;                  // out("screen[segments]")

        // Rendering stage 3
        out attribute int line_caps;                  // out("line_caps")
        out attribute vec4 line_colors;               // out("line_colors")
        out attribute float line_widths;              // out("line_widths")
        ```

    ```bash exec="1"
    python docs/snippets/Segments_init.py
    ```
    """

    @command("visual.Markers")
    def __init__(self, positions   : Transform | Buffer,
                       line_caps   : Transform | Buffer | LineCap,
                       line_colors : Transform | Buffer | Color,
                       line_widths : Transform | Buffer | float):
        """
        Create a visual of n segments at given *positions* with
        given *line_colors*, *line_widths* and *line_caps*.

        Parameters
        ----------
        positions : Transform | Buffer
            Segments positions (2,vec3)
        line_caps : Transform | Buffer | LineCap
            Segments end caps (int)
        line_colors : Transform | Buffer | Color
            Segments line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Segments line width (float)
        """

        super().__init__()

        # These variables are available prior to rendering and may be
        # tracked
        self._in_variables = {
            "positions" : positions,
            "line_caps" : line_caps,
            "line_colors" : line_colors,
            "line_widths" : line_widths,
            "viewport" : None
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        n = len(positions)
        self._out_variables = {
            "screen[positions]" : np.empty((n,2,3), np.float32),
            "screen[segments]" :  np.empty(n, np.float32),
            "line_caps" :         np.empty(n, np.uint8),
            "line_colors" :       np.empty((n,4), np.float32),
            "line_widths" :       np.empty(n, np.float32),
        }
