# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np
from enum import IntEnum

class Type:
    """
    Types specific to the procotol
    """

class Measure:
    """
    Representation of a measure
    """

    def __init__(self, value : float,
                       unit :  str = None):
        """
        Representation of a measure

        Parameters
        ----------
        value: float
            Values of the measure

        unit: str
            Unit of the measure
        """

        self._value = value
        self._unit = unit


class Color:
    """ Representation of a color in the sRGB colorspace. """

    def __init__(self, red :   float,
                       green : float,
                       blue :  float,
                       alpha : float):
        """
        Representation of a color in the sRGB colorspace.

        Parameters
        ----------

        red:

            Normalized value for the red channel

        green:

            Normalized value for the green channel

        blue:

            Normalized value for the blue channel

        alpha:

            Normalized value for he alpha channel.
        """

        self._color = np.array([red, green, blue, alpha])

    def __array__(self):
        return self._color

    def __getitem__(self, index):
        return self._color[index]

    def __len__(self):
        return len(self._color)


class Marker(IntEnum):
    """

    **Attributes**

    | Name          | Visual                    | Reference                   |
    |---------------|---------------------------|-----------------------------|
    | `point`       | :material-circle:         | [material-circle]           |
    | `triangle`    | :material-triangle:       | [material-triangle]         |
    | `square`      | :material-square:         | [material-square]           |
    | `minus`       | :material-minus-thick:    | [material-minus-thick]      |
    | `plus`        | :material-plus-thick:     | [material-plus-thick]       |
    | `cross`       | :material-close-thick:    | [material-close-thick]      |
    | `star`        | :material-star:           | [material-star]             |
    | `club`        | :material-cards-club:     | [material-cards-club]       |
    | `heart`       | :material-cards-heart:    | [material-cards-heart]      |
    | `spade`       | :material-cards-spade:    | [material-cards-spade]      |
    | `diamond`     | :material-cards-diamond:  | [material-cards-diamond]    |
    | `arrow`       | :material-arrow-up-thick: | [material-arrow-up-thick]   |

    [material-circle]:   https://pictogrammers.com/library/mdi/icon/circle/
    [material-square]:   https://pictogrammers.com/library/mdi/icon/square/
    [material-triangle]: https://pictogrammers.com/library/mdi/icon/triangle/
    [material-plus-thick]: https://pictogrammers.com/library/mdi/icon/plus-thick/
    [material-minus-thick]: https://pictogrammers.com/library/mdi/icon/minus-thick
    [material-star]: https://pictogrammers.com/library/mdi/icon/star/
    [material-close-thick]: https://pictogrammers.com/library/mdi/icon/close-thick/
    [material-cards-club]: https://pictogrammers.com/library/mdi/icon/cards-club/
    [material-cards-heart]: https://pictogrammers.com/library/mdi/icon/cards-heart/
    [material-cards-spade]: https://pictogrammers.com/library/mdi/icon/cards-spade/
    [material-cards-diamond]: https://pictogrammers.com/library/mdi/icon/cards-diamond/
    [material-map-marker]: https://pictogrammers.com/library/mdi/icon/map-marker/
    [material-disc]: https://pictogrammers.com/library/mdi/icon/disc/
    [material-arrow-up-thick]: https://pictogrammers.com/library/mdi/icon/arrow-up-thick/
    """

    point : int    = 1
    triangle : int = 2
    square : int   = 3
    minus : int    = 4
    plus : int     = 5
    cross : int    = 6
    star : int     = 7
    club : int     = 8
    heart : int    = 9
    spade : int    = 10
    diamond : int  = 11
    arrow : int    = 12

    __markers__ = None

    @classmethod
    def path(cls, marker):
        if cls.__markers__ is None:
            from . svg import svg_to_path

            cls.__markers__ =  {
                Marker.point :
                svg_to_path(
                    "M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"),

                Marker.triangle :
                svg_to_path(
                    "M1,21H23L12,2Z"),

                Marker.square :
                svg_to_path(
                    "M3,3V21H21V3"),

                Marker.minus :
                svg_to_path(
                    "M20 14H4V10H20"),

                Marker.plus :
                svg_to_path(
                    "M20 14H14V20H10V14H4V10H10V4H14V10H20V14Z"),

                Marker.cross :
                svg_to_path(
                    "M20 6.91L17.09 4L12 9.09L6.91 4L4 6.91L9.09 12L4 17.09L6.91 20L12 14.91L17.09 20L20 17.09L14.91 12L20 6.91Z"),

                Marker.star :
                svg_to_path(
                    "M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z"),

                Marker.club :
                svg_to_path(
                    "M12,2C14.3,2 16.3,4 16.3,6.2C16.21,8.77 14.34,9.83 14.04,10C15.04,9.5 16.5,9.5 16.5,9.5C19,9.5 21,11.3 21,13.8C21,16.3 19,18 16.5,18C16.5,18 15,18 13,17C13,17 12.7,19 15,22H9C11.3,19 11,17 11,17C9,18 7.5,18 7.5,18C5,18 3,16.3 3,13.8C3,11.3 5,9.5 7.5,9.5C7.5,9.5 8.96,9.5 9.96,10C9.66,9.83 7.79,8.77 7.7,6.2C7.7,4 9.7,2 12,2Z"),

                Marker.heart :
                svg_to_path(
                    "M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5C2,5.41 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.41 22,8.5C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z"),

                Marker.spade :
                svg_to_path(
                    "M12,2C9,7 4,9 4,14C4,16 6,18 8,18C9,18 10,18 11,17C11,17 11.32,19 9,22H15C13,19 13,17 13,17C14,18 15,18 16,18C18,18 20,16 20,14C20,9 15,7 12,2Z"),

                Marker.diamond :
                svg_to_path(
                    "M19,12L12,22L5,12L12,2"),

                Marker.arrow :
                svg_to_path(
                    "M14,20H10V11L6.5,14.5L4.08,12.08L12,4.16L19.92,12.08L17.5,14.5L14,11V20Z")
            }

        return cls.__markers__[marker]


class LineStyle(IntEnum):
    solid:                 int = 1

    dotted:                int = 2
    densely_dotted:        int = 3
    loosely_dotted:        int = 4

    dashed:                int = 5
    densely_dashed:        int = 6
    loosely_dashed:        int = 7

    dashdotted:            int = 8
    densely_dashdotted:    int = 9
    loosely_dashdotted:    int = 10

    dashdotdotted:         int = 11
    densely_dashdotdotted: int = 12
    loosely_dashdotdotted: int = 13

class LineCap(IntEnum):
    butt:  int = 1
    round: int = 2
    cap:   int = 3

class LineJoin(IntEnum):
    miter: int = 1
    round: int = 2
    bevel: int = 3

class Shading(IntEnum):
    flat : int    = 1
    gouraud : int = 2
    phong : int   = 3

class Render(IntEnum):
    front_back : int = 0
    front : int      = 1
    back : int       = 2
