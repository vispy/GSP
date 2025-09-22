# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
This example shows how to create a canvas and save it to a file.

Keywords: canvas, save, render
"""

from common.launcher import parse_args

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)

# Show or save the result
render(canvas, [], [])
