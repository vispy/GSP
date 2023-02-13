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
V,F = glm.mesh("data/bunny-2048.obj")
EC = core.Color(0.00, 0.00, 0.00, 1.00)
FC = core.Color(1.00, 1.00, 1.00, 0.85)
camera = glm.Camera("ortho")

viewport = core.Viewport(canvas, 256, 256, 256, 256)
mesh = visual.Mesh(viewport, V, F, FC, EC, 0.25)
mesh.render(camera.transform @ glm.xrotate(90))

viewport = core.Viewport(canvas, 0, 0, 256, 256)
mesh = visual.Mesh(viewport, V, F, FC, EC, 0.25)
mesh.render(camera.transform @ glm.yrotate(90))

viewport = core.Viewport(canvas, 256, 0, 256, 256)
mesh = visual.Mesh(viewport, V, F, FC, EC, 0.25)
mesh.render(camera.transform)

camera = glm.Camera("perspective", theta=-10, phi=1.5, zdist=4)
viewport = core.Viewport(canvas, 0, 256, 256, 256)
FC = transform.Colormap("magma")(transform.Depth())
mesh = visual.Mesh(viewport, V, F, FC, EC, 0)
mesh.render(camera.transform)


if gsp.mode.startswith("matplotlib"):
    camera.connect(viewport.axes, "motion",  mesh.render)
    canvas.run()

