import gsp
from gsp.matplotlib import core, visual, glm
import numpy as np

###########################################
# Build a scene

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 200
P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)), dtype=np.float32)

# buffer_count = n
# buffer_dtype = P.dtype
# buffer_data = P.data
# positions = core.Buffer(buffer_count, buffer_dtype, buffer_data)
pixels = visual.Pixels(positions=P, colors=[0,0,0,1])
pixels.render(viewport)

##########################################
# Save a command file

commands_filename = "test-command-file-cycle.command.json"
gsp.save(filename=commands_filename)

##########################################
# Now reset everything and reload from command file, then run the queue
# 

# reset objects
gsp.Object.objects = {}

# load commands from file into a command queue
command_queue = gsp.io.json.load(commands_filename)

# KEY: REQUIRED FOR THE GLOBALS
gsp.use("matplotlib")

# Actually run the command queue
command_queue.run(globals(), locals())

##########################################
# Finally display the result via matplotlib

import matplotlib.pyplot as plt
plt.show(block=True)