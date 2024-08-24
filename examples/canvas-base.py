# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
Canvas (base)
=============

This example shows how to create a canvas with a size specified using
some units (centimeter) and how t enter the event loop (matplotlib).
"""
import gsp
gsp.use("matplotlib")

cm = transform.Centimeter()
canvas = core.Canvas(10*cm, 10*cm, 100.0)

plt.savefig("output/canvas-base.png")
plt.show()
