# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) -- Client/Server example
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
# This example shows how the client / server protocol works. In the
# first part # (client), we draw a scence (points.py) using the text
# backend. This backend displays in the console command are created in
# the backgroudn while registering them in the `commands()` list. In
# the second part (server), we use the matplotlib backend to execute
# commands one after the other. The result shoudl be identical to the
# `points.py` example.
# -----------------------------------------------------------------------------

import gsp, glm
import numpy as np

# --- Client part -------------------------------------------------------------
gsp.use("client/text")

canvas = core.Canvas(512, 512, 100.0)
camera = glm.Camera("perspective", theta=10, phi=10)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
colormap = transform.Colormap("magma")
depth = transform.Depth()

positions = glm.vec3(10_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))
fill_colors = colormap(depth)
edge_colors = glm.vec4(len(positions))
edge_colors.rgba = 0,0,0,1

points = visual.Points(viewport, positions, 25.0, fill_colors, edge_colors, 0.5)
points.render(camera.transform)

# --- Server part -------------------------------------------------------------
from gsp.backend.reference import commands, objects
gsp.use("matplotlib")

for command in commands():
    command.execute(globals(), locals())

for key, obj in objects().items():
    if isinstance(obj, core.Canvas):
        canvas = obj
    elif isinstance(obj, core.Viewport):
        viewport = obj
    elif isinstance(obj, visual.Points):
        points = obj

# matplotlib backend specific
camera.connect(viewport.axes, "motion",  points.render)
canvas.run()

