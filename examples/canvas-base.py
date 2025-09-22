# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Canvas (base)
=============

This example shows how to create a canvas with a size specified using
some units (centimeter) and how t enter the event loop (matplotlib).
"""

from gsp import transform
from common.launcher import parse_args

# Parse command line arguments
core, visual, render = parse_args()

# Create a GSP scene
cm = transform.Centimeter()
canvas = core.Canvas(10*cm, 10*cm, 100.0)

# Show or save the result
render(canvas, [], [])
