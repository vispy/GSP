# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
# This example demonstrates usage of the JIT depth buffer. It is used with a
# colormap to vary color according to the depth of a point (not to be confused
# with the z coordinate).
# -----------------------------------------------------------------------------
import gsp
import glm
import meshio
import numpy as np
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera = glm.Camera("perspective", theta=-20, phi=2.5)

bunny = meshio.read("data/bunny-4096.obj")
verts = 2*glm.fit_unit_cube(bunny.points).astype(np.float32)
faces = bunny.cells[0].data.astype(np.uint64)
colormap = transform.Colormap("magma")
depth = transform.Depth()

edge_colors = glm.vec4(len(faces))
edge_colors.rgba = 0,0,0,1
outline = visual.Mesh(viewport, verts, faces, edge_colors, edge_colors, 2)
outline.render(camera.transform)

fill_colors = colormap(depth)
mesh = visual.Mesh(viewport, verts, faces, fill_colors, edge_colors, .25)
mesh.render(camera.transform)


# Interaction with mouse (matplotlib backends only)
if gsp.mode.startswith("matplotlib"):
    camera.connect(viewport.axes, "motion",  outline.render)
    camera.connect(viewport.axes, "motion",  mesh.render)
    canvas.run()

