# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import logging
import numpy as np

# import gsp
# gsp.mode("direct/matplotlib")
# gsp.mode("client/json")
logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':

    # direct_mode, n = False, 10_000
    direct_mode, n = True, 10_000
    
    if not direct_mode:
        import gsp
        gsp.mode("client", reset=True, record=True, output=False)
        from gsp.core import Canvas, Viewport, Buffer, Datatype
        from gsp.visual import Pixels
        from gsp.transform import Mat4x4
    else:
        import matplotlib
        import matplotlib.pyplot as plt
        from gsp.backend.matplotlib.core import Canvas, Viewport, Buffer, Datatype
        from gsp.backend.matplotlib.visual import Pixels
        from gsp.backend.matplotlib.transform import Mat4x4

        
    vec3 = np.dtype([("x", np.float32),
                     ("y", np.float32),
                     ("z", np.float32)])
    rgba = np.dtype([("r", np.float32),
                     ("g", np.float32),
                     ("b", np.float32),
                     ("a", np.float32) ])

    canvas = Canvas(512, 512, 100)
    viewport = Viewport(canvas, 0, 0, 512, 512)

    positions = np.random.uniform(-1, 1, (n,3)).astype(np.float32)
    colors = np.random.uniform(0, 1, (n,4)).astype(np.float32)
    colors[:,-1] = 1

    pixels = Pixels(viewport,
                    Buffer.from_numpy(positions.view(vec3)),
                    Buffer.from_numpy(colors.view(rgba)))

    from camera import Camera
    camera = Camera("perspective", theta=0, phi=0)
    transform = Mat4x4(camera.transform.tobytes())
    pixels.render(transform)
        
    
    if not direct_mode:
        # for command in gsp.commands():
        #     print(command.yaml_dump())
        # for command in gsp.commands():
        #     print(command.json_dump())

        import matplotlib
        import matplotlib.pyplot as plt
        from gsp.backend.matplotlib import Canvas, Viewport, Buffer, Datatype
        from gsp.backend.matplotlib.visual import Pixels
        from gsp.backend.matplotlib.transform import Mat4x4
        for command in gsp.commands():
            command.execute( globals(), locals())
        plt.show()
    else:
        pixels.render(transform)
        plt.show()


