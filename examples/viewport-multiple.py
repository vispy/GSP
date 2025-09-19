# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Multiple viewports
==================

This example show how to have several viewports.
"""
from common.launcher import parse_args

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)

# Fixed viewport sizes and positions (in pixels)
# core.Viewport(canvas, 0, 0, 256, 256, (1,0,0,1))
# core.Viewport(canvas, 0, 256, 256, 256, (0,1,0,1))
# core.Viewport(canvas, 256, 0, 256, 256, (0,0,1,1))
# core.Viewport(canvas, 256, 256, 256, 256, (1,1,0,1))

# Proportional viewport sizes and positions
viewport1 = core.Viewport(canvas, 0.0, 0.0, 0.5, 0.5, (1,0,0,1))
viewport2 = core.Viewport(canvas, 0.0, 0.5, 0.5, 0.5, (0,1,0,1))
viewport3 = core.Viewport(canvas, 0.5, 0.0, 0.5, 0.5, (0,0,1,1))
viewport4 = core.Viewport(canvas, 0.5, 0.5, 0.5, 0.5, (1,1,0,1))

# Show or save the result
render(canvas, [viewport1, viewport2, viewport3, viewport4], [])
