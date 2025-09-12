import numpy as np
import gsp
from .example_launcher import ExampleLauncher

##############################################
# Parse command line arguments
#

core, visual = ExampleLauncher.parse_args()

##############################################
# Create a GSP scene
#

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1, 1, 1, 1])
n = 250_000
P = gsp.glm.to_vec3(np.random.uniform(-1, +1, (n, 2)))
pixels = visual.Pixels(P, colors=[0, 0, 0, 1])
pixels.render(viewport)

#############################################
# Show or save the result
#

ExampleLauncher.show(canvas, viewport, [pixels])
