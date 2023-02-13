# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
# This example demonstrates how to add an outline to a mesh. This is done using
# two meshed. One totally black with a thick stroke width and a second one that
# is drawn over. The result is a black outline.
# -----------------------------------------------------------------------------
import gsp, glm
import numpy as np
gsp.use("matplotlib")

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=-10, phi=1.5)
colormap = transform.Colormap("magma")
depth    = transform.Depth()

V,F = glm.mesh("data/bunny-4096.obj")
EC = core.Color(0,0,0,1)
FC = colormap(depth)

outline = visual.Mesh(viewport, V, F, EC, EC, 3)
outline.render(camera.transform)

mesh = visual.Mesh(viewport, V, F, FC, EC, 0.1)
mesh.render(camera.transform)

# Interaction with mouse (matplotlib backends only)
if gsp.mode.startswith("matplotlib"):
    camera.connect(viewport.axes, "motion",  outline.render)
    camera.connect(viewport.axes, "motion",  mesh.render)
    canvas.run()

