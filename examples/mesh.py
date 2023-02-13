# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp, glm
gsp.use("matplotlib")

canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=-20, phi=2.5)
colormap = transform.Colormap("magma")
depth    = transform.Depth()

V,F = glm.mesh("data/bunny-4096.obj")
EC = core.Color(0.00, 0.00, 0.00, 1.00)
FC = core.Color(1.00, 1.00, 1.00, 0.85)
mesh = visual.Mesh(viewport, V, F, FC, EC, 0.25)
mesh.render(camera.transform)

# Interaction with mouse (matplotlib backends only)
if gsp.mode.startswith("matplotlib"):
    camera.connect(viewport.axes, "motion",  mesh.render)
    canvas.run()

