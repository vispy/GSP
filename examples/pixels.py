# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
import gsp, glm

gsp.use("matplotlib/iterm")

canvas = core.Canvas(512, 512, 100.0)
camera = glm.Camera("perspective", theta=10, phi=10)
viewport = core.Viewport(canvas, 0, 0, 512, 512)

positions = glm.vec3(50_000)
positions.xyz = np.random.uniform(-1, +1, (len(positions),3))

colors = glm.vec4(len(positions))
colors.rgba = 0,0,0,1

pixels = visual.Pixels(viewport, positions, colors)
pixels.render(camera.transform)

canvas.run()

