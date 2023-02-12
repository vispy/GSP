# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
# This example demonstrates usage of the JIT depth buffer. It is used with a
# colormap to vary color according to the depth of a point (not to be confused
# with the z coordinate).
# -----------------------------------------------------------------------------
import gsp, glm
import numpy as np
gsp.use("matplotlib/iterm")
# gsp.use("yaml")
        
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
camera = glm.Camera("perspective", theta=10, phi=10)
colormap = transform.Colormap("magma")
depth = transform.Depth()

positions = glm.vec3(10_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))
fill_colors = colormap(depth)
edge_colors = glm.vec4(len(positions))
edge_colors.rgba = 0,0,0,1

points = visual.Points(viewport, positions, 25.0, fill_colors, edge_colors, 0.5)
points.render(camera.transform)

# matplotlib backend specific
if gsp.mode.startswith("matplotlib"):
    camera.connect(viewport.axes, "motion",  points.render)
    canvas.run()

