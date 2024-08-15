# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
"""
This example show the Pixels visual where pixels are spread
randomly inside a cube that can be rotated using the mouse.
"""
import gsp
gsp.use("matplotlib")

import numpy as np
from gsp import glm

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, (1,1,1,1))
P = glm.vec3(250_000)
P.xyz = np.random.uniform(-1, +1, (len(P),3))
pixels = visual.Pixels(P, colors=(0,0,0,1))

# Run the camera
from camera import Camera
camera = Camera("perspective", theta=50, phi=50)
camera.connect(viewport, "motion",  pixels.render)
camera.run()
