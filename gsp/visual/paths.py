# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.visual import Visual
from gsp.core import List, Buffer, Color, LineCap, LineJoin, LineStyle
from gsp.transform import Transform
from gsp.io.command import command

class Paths(Visual):
    """Paths is a set of contiguous lines passing through a series of
    positions (path). Each path can be colored and styled and possess
    a thickness. Paths always face the viewer such that their apparent
    thickness is constant. Their end points ([caps]) can be styled
    following the SVG specification (butt, round or cap). Their
    [joins] can be styled following partially the SVG specification
    (round, miter or bevel). The number of paths inside a Paths visual
    is dictated by the indices variables (see [below]).

    [caps]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap
    [joins]: https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
    [below]: #number-of-paths

    # Elements

    The number of elements (paths) composing a visual is fully
    specified by the `indices` and `positions` parameters. Considering
    a positions paramters with **n** position, `indices` can be: 

    - `int` (equal to p)

      : This indicates paths are composed of **p** consecutives
      positions.  this require **p** to be a divider of **n**. The
      total number of paths **N** is equal to **n/p**.

    - `Buffer` 

      : Each item of the list describes a path made of the given number of
        consecutive positions. This require the sum of the list to be less
        or equal to **n**. The total number of paths is the length of the
        list **N**.

    - `List`

      : Each item of the list describe a path made of indexed positions.
        The total number of paths is the length of the list **N**. When a
        buffer is used in place of a list, each item must be separated by
        the value -1 indicating the end of a path.


    **Example**
    ```python
    Paths([a,b,c,d], 2)                # results in two paths: (a,b) and (c,d)
    Paths([a,b,c,d], [2,2])            # results in two paths: (a,b) and (c,d)
    Paths([a,b,c,d], [[0,1], [2,3]])   # results in two paths: (a,b) and (c,d)
    ```
    
    
    # Attributes

    Each attribute of the visual can be assigned per visual (all
    paths), per path, per position or per vertex, depending on the
    nature of the attribute and the possible limitations of the
    server. Let's consider a set of **n** positions that results in
    **P** paths producing **N** vertices.

    Attribute   | Type       | per visual (1) | per path (P) | per positions (n) | per vertex (N) |
    ------------|------------|----------------|--------------|-------------------|----------------|
    line_colors | vec4       | ✓              | ✓︎︎            | ✓                 | ✓              |
    line_widths | float      | ✓              | ✓︎︎            | ✓                 | ✓              |
    line_styles | int        | ✓              | ✓            | -                 | -              |
    line_joins  | int        | ✓              | ✓︎︎            | -                 | -              |
    line_caps   | ivec2      | ✓              | ✓            | -                 | -              |

    # Output variables

    During rendering, a number of variables are produced and can be
    referred to in the definition of attributes using the [Out][]
    transform using their name. The  size of these variables are
    dependents on their nature. Let's  consider a set of **n**
    positions that results in **P** paths producing **N** vertices.
    
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
    path/caps              | ivec2   | P    | Line caps      |
    path/joins             | int     | P    | Line joins     |
    path/style             | int     | P    | Line style     |


    ```bash exec="0"
    python docs/snippets/Paths_init.py
    ```

    """

    @command("visual.Paths")
    def __init__(self, positions    : Transform | Buffer,
                       indices      : Transform | Buffer | List | int,
                       line_colors  : Transform | Buffer | Color,
                       line_widths  : Transform | Buffer | float,
                       line_styles  : Transform | Buffer | LineStyle,
                       line_joins   : Transform | Buffer | LineJoin,
                       line_caps    : Transform | Buffer | LineCap):
        """

        Parameters
        ----------
        positions : Transform | Buffer
            Paths positions (vec3)
        indices : Transform | List | int
            Position indices composing paths (int)       
        line_caps : Transform | Buffer | LineCap
            Paths end caps (int)
        line_colors : Transform | Buffer | Color
            Paths line colors (vec4)
        line_widths : Transform | Buffer | Measure
            Paths line width (float)
        """

        super().__init__()

        # These variables are available prior to rendering and may be
        # tracked
        self._in_variables = {
            "positions" : positions,
            "indices" : indices,
            "line_colors" : line_colors,
            "line_widths" : line_widths,
            "line_styles" : line_styles,
            "line_joins" : line_joins,
            "line_caps" : line_caps,
            "viewport" : None
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        if isinstance(positions, Transform):
            positions = positions.evaluate({"dpi":100})
        n = len(positions)

        # Determining the number of paths:
        if isinstance(indices, (int)):
            npaths = len(positions) // indices
        else:
            npaths = len(indices)
        
        self._out_variables = {
            "screen[positions]" : np.empty((n,3), np.float32),
            "screen[paths]"    :  np.empty((npaths,3), np.float32),
            "line_caps" :         np.empty((n,2), np.uint8),
            "line_colors" :       np.empty((n,4), np.float32),
            "line_widths" :       np.empty(n, np.float32),
        }

    # # Private
    # def _generate_indices(self, position, indices):
    #     """This function generates list of list of indices that can be
    #     used to generate paths (from the positions buffer)
    #     """

    #     n = len(positions)
    #     if isinstance(indices, (int)):
    #         if n % len(indices) == 0:
    #             indices = np.arange(0, n).reshape(len(indices),-1)
    #             return indices
    #         else:
    #             raise ValueError("When indices is an integer, it
    #             must be a divider of the number of positions")
    #     elif isinstance(indices, (list,tuple)):
            
            
    #         indices = [indices

    #         np.arange(0, n).reshape(len(indices),-1)
            
        
                
