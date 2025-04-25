# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import List, Buffer, Color, LineCap, LineJoin, LineStyle
from gsp.transform import Transform
from gsp.io.command import command

class Polygons(Visual):
    """Polygons is a closed set of contiguous lines passing through a
    series of positions (poygon). Each polygon can be colored and
    styled and possess a thickness. Polygons always face the viewer
    such that their apparent thickness is constant. Their [joins] can
    be styled following partially the SVG specification (round, miter
    or bevel). The number of polygons inside a Polygons visual is dictated
    by the indices variables (see [below]).

    [joins]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
    [below]: #number-of-paths

    # Elements

    The number of elements (polygons) composing a visual is fully
    specified by the `indices` and `positions` parameters. Considering
    a positions paramters with **n** position, `indices` can be: 

    - `int` (equal to p)

      : This indicates paths are composed of **p** consecutives
      positions.  this require **p** to be a divider of **n**. The
      total number of paths **N** is equal to **n/p**.

    - `Buffer` 

      : Each item of the list describes a path made of the given number of
        consecutive positions. This require the sum of the list to be less
        or equal to **n**. The total number of polygons is the length of the
        list **N**.

    - `List`

      : Each item of the list describe a polygon made of indexed positions.
        The total number of polygonss is the length of the list **N**.


    **Example**
    ```python
    Polygons([a,b,c,d], 2)                # results in two paths: (a,b) and (c,d)
    Polygons([a,b,c,d], [2,2])            # results in two paths: (a,b) and (c,d)
    Polygons([a,b,c,d], [[0,1], [2,3]])   # results in two paths: (a,b) and (c,d)
    ```
    
    
    # Attributes

    Each attribute of the visual can be assigned per visual (all
    paths), per polygon, per position or per vertex, depending on the
    nature of the attribute and the possible limitations of the
    server. Let's consider a set of **n** positions that results in
    **P** polygons producing **N** vertices.

    Attribute   | Type       | per visual (1) | per polygon (P) | per positions (n) | per vertex (N) |
    ------------|------------|----------------|-----------------|-------------------|----------------|
    fill_colors | vec4       | ✓              | ✓︎︎               | -                 | -              |
    line_colors | vec4       | ✓              | ✓︎︎               | -                 | -              |
    line_widths | float      | ✓              | ✓︎︎               | -                 | -              |
    line_styles | int        | ✓              | ✓               | -                 | -              |
    line_joins  | int        | ✓              | ✓︎︎               | -                 | -              |

    # Output variables

    During rendering, a number of variables are produced and can be
    referred to in the definition of attributes using the [Out][]
    transform using their name. The  size of these variables are
    dependents on their nature. Let's  consider a set of **n**
    positions that results in **P** polygons producing **N** vertices.
    
    Variable name (string) | Type    | Size | Comment                                       |
    -----------------------|---------|------|-----------------------------------------------|
    positions/2D           | vec2    | n    | Positions coordinates (screen)                |
    vertex/positions/2D    | vec2    | N    | Path vertex coordinates (screen)              |
    vertex/positions/3D    | vec3    | N    | Path vertex coordinates (space)               |
    vertex/curvilinear/2D  | float   | N    | Curvilinear coordinates along path (2d space) |
    vertex/curvilinear/3D  | float   | N    | Curvilinear coordinates along path (3d space) |

    After rendering, once every transforms has been evaluated, a number
    of variables are readable by other visuals:
    
    Variable name (string) | Type    | Size | Comment        |
    -----------------------|---------|------|----------------|
    vertex/colors          | vec4    | N    | Line color     |
    vertex/widths          | float   | N    | Line width     |
    path/joins             | int     | P    | Line joins     |
    path/style             | int     | P    | Line style     |


    ```bash exec="0"
    python docs/snippets/Polygons_init.py
    ```

    """

    @command("visual.Polygons")
    def __init__(self, positions    : Transform | Buffer,
                       indices      : Transform | Buffer | List | int,
                       fill_colors  : Transform | Buffer | Color,
                       line_colors  : Transform | Buffer | Color,
                       line_widths  : Transform | Buffer | float,
                       line_styles  : Transform | Buffer | LineStyle,
                       line_joins   : Transform | Buffer | LineJoin):
        """
        Parameters
        ----------
        positions : Transform | Buffer
            Polygons positions (vec3)
        indices : Transform | List | int
            Position indices composing polygons
        fill_colors : Transform | Buffer | Color
            Polygons fill color (vec4)
        line_colors : Transform | Buffer | Color
            Polygons line color (vec4)
        line_widths : Transform | Buffer | Measure
            Polygons line width (float)
        line_styles : Transform | Buffer | Measure
            Polygons line style (float)
        line_joins : Transform | Buffer | LineJoin
            Paths line join (int)
        """

        super().__init__()

        # These variables are available prior to rendering and may be
        # tracked
        self._in_variables = {
            "positions" : positions,
            "indices" : indices,
            "fill_colors" : fill_colors,
            "line_colors" : line_colors,
            "line_widths" : line_widths,
            "line_styles" : line_styles,
            "line_joins" : line_joins,
            "viewport" : None
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        if isinstance(positions, Transform):
            positions = positions.evaluate({"dpi":100})
        n = len(positions)

        # Determining the number of polygons:
        if isinstance(indices, (int)):
            npolys = len(positions) // indices
        else:
            npolys = len(indices)
        
        self._out_variables = {
            "screen[positions]" : np.empty((n,3), np.float32),
            "screen[polygons]"  :  np.empty((npolys,3), np.float32),
            "line_caps" :         np.empty((n,2), np.uint8),
            "fill_colors" :       np.empty((n,4), np.float32),
            "line_colors" :       np.empty((n,4), np.float32),
            "line_widths" :       np.empty(n, np.float32),
        }
