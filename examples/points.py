# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from camera import Camera
from glm import vec3, rgba

# from gsp.backend.text import (core, visual, transform)
# from gsp.backend.yaml import (core, visual, transform)
# from gsp.backend.json import (core, visual, transform)
# from gsp.backend.datoviz import (core, visual, transform)
from gsp.backend.matplotlib import (core, visual, transform)

n = 10_000
canvas = core.Canvas(512, 512, 100.0)
camera = Camera("perspective", theta=10, phi=10)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
positions = np.random.uniform(-1, +1, (n,3)).astype(np.float32)
fill_colors = np.zeros((n,4), np.float32)
fill_colors[...] = 1,1,1,1
edge_colors = np.zeros((n,4), np.float32)
edge_colors[...] = 0,0,0,1
points = visual.Points(viewport,
                       positions.view(vec3),
                       25,
                       fill_colors.view(rgba),
                       edge_colors.view(rgba),
                       0.5)
points.render(camera.transform)

# matplotlib backend specific
camera.connect(viewport.axes, "motion",  points.render)
canvas.run()

