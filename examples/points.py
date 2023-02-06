# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import glm
import numpy as np
# from gsp.backend.text import (core, visual, transform)
# from gsp.backend.yaml import (core, visual, transform)
# from gsp.backend.json import (core, visual, transform)
# from gsp.backend.datoviz import (core, visual, transform)
import matplotlib as mpl; mpl.use("module://imgcat")
from gsp.backend.matplotlib import (core, visual, transform)

canvas = core.Canvas(512, 512, 100.0)
camera = glm.Camera("perspective", theta=10, phi=10)
viewport = core.Viewport(canvas, 0, 0, 512, 512)

positions = glm.vec3(10_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))

fill_colors = glm.vec4(len(positions))
fill_colors.rgba = 1,1,1,1

edge_colors = glm.vec4(len(positions))
edge_colors.rgba = 0,0,0,1

points = visual.Points(viewport, positions, 25.0, fill_colors, edge_colors, 0.5)
points.render(camera.transform)

# matplotlib backend specific
camera.connect(viewport.axes, "motion",  points.render)
canvas.run()

