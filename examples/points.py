# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from glm.camera import Camera
from glm.types import vec2, vec3, vec4

# from gsp.backend.text import (core, visual, transform)
# from gsp.backend.yaml import (core, visual, transform)
# from gsp.backend.json import (core, visual, transform)
# from gsp.backend.datoviz import (core, visual, transform)
from gsp.backend.matplotlib import (core, visual, transform)

n = 10_000
canvas = core.Canvas(512, 512, 100.0)
camera = Camera("perspective", theta=10, phi=10)
viewport = core.Viewport(canvas, 0, 0, 512, 512)

positions = vec3(n)
positions.xyz = np.random.uniform(-1, +1, (n,3))

fill_colors = vec4(n)
fill_colors.rgba = 1,1,1,1

edge_colors = vec4(n)
edge_colors.rgba = 0,0,0,1

points = visual.Points(viewport, positions, 25.0, fill_colors, edge_colors, 0.5)
points.render(camera.transform)

# matplotlib backend specific
camera.connect(viewport.axes, "motion",  points.render)
canvas.run()

