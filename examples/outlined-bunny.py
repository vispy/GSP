# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
# This example demonstrates how to add an outline to a mesh. This is done using
# two meshed. One totally black with a thick stroke width and a second one that
# is drawn over. The result is a black outline.
# -----------------------------------------------------------------------------
import gsp, glm
gsp.use("matplotlib")

interactive = 1
canvas   = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera   = glm.Camera("perspective", theta=-10, phi=1.5)
colormap = transform.Colormap("magma")
depth    = transform.Depth()

V,F = glm.mesh("data/bunny-4096.obj")
black = core.Color(0,0,0,1)
white = core.Color(1,1,1,1)
FC = colormap(depth)

outer = visual.Mesh(viewport, V, F, black, black, 6)
outer.render(camera.transform)

inner = visual.Mesh(viewport, V, F, white, white, 3)
inner.render(camera.transform)

mesh = visual.Mesh(viewport, V, F, FC, black, 0.1)
mesh.render(camera.transform)

# Terminal output: matplotlib backend + imgcat (OSX/iterm)
if not interactive:
    from imgcat import imgcat
    imgcat(canvas.figure)

# Interactive: matplotlib backends only
elif interactive:
    camera.connect(viewport.axes, "motion",  outer.render)
    camera.connect(viewport.axes, "motion",  inner.render)
    camera.connect(viewport.axes, "motion",  mesh.render)
    canvas.run()

