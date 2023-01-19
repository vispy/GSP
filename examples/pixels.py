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
camera = Camera("perspective", theta=0, phi=0)
viewport = core.Viewport(canvas, 0, 0, 512, 512)
positions = np.random.uniform(-1, 1, (n,3)).astype(np.float32)
colors = np.random.uniform(0, 1, (n,4)).astype(np.float32)
pixels = visual.Pixels(viewport, positions.view(vec3), colors.view(rgba))
pixels.render(transform.Mat4x4(camera.transform))

canvas.run()

