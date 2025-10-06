import os
import matplotlib.image as mpl_img

import gsp
from gsp_matplotlib import glm
from common.launcher import parse_args

# import gsp
__dirname__ = os.path.dirname(os.path.abspath(__file__))

# Parse command line arguments
core, visual, render = parse_args()

#  Create a canvas and a viewport

canvas = core.Canvas(256, 256, 100.0)
viewport = core.Viewport(canvas, 0, 0, 256, 256, [1, 1, 1, 1])

# Create a cube with paths

cube_path_positions = glm.vec3(8)
cube_path_positions[...] = [
    (-1.0, -1.0, +1.0),
    (+1.0, -1.0, +1.0),
    (-1.0, +1.0, +1.0),
    (+1.0, +1.0, +1.0),
    (-1.0, -1.0, -1.0),
    (+1.0, -1.0, -1.0),
    (-1.0, +1.0, -1.0),
    (+1.0, +1.0, -1.0),
]
cube_path_face_indices = [
    [0, 1],
    [1, 3],
    [3, 2],
    [2, 0],
    [4, 5],
    [5, 7],
    [7, 6],
    [6, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]

colormap = gsp.transform.Colormap("gray", vmin=0.0, vmax=0.75)
depth = gsp.transform.Out("screen[paths].z")
paths_visual = visual.Paths(
    cube_path_positions,
    cube_path_face_indices,
    line_colors=colormap(depth),
    line_widths=5.0 * (1 - 1.25 * depth),
    line_styles=gsp.core.LineStyle.solid,
    line_joins=gsp.core.LineJoin.round,
    line_caps=gsp.core.LineCap.round,
)
paths_visual.render(viewport)

# Read the image_data numpy array from a file and create a texture

image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data = mpl_img.imread(image_path)
texture = core.Texture(image_data, image_data.shape)

# Create an image visual
image_visual = visual.Image(
    positions=[[-1, 1, -1]],
    texture_2d=texture,
    image_extent=(-1, 1, -1, 1),
)
image_visual.render(viewport)

# Show or save the result

render(canvas, [viewport], [paths_visual, image_visual])
