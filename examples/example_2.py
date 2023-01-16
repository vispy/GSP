# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import numpy as np
    direct_mode = True
    
    if not direct_mode:
        import gsp
        gsp.mode("client", reset=True, record=True, output=False)
        from gsp.core import Canvas, Viewport, Buffer, Datatype
        from gsp.visual import Pixels
        from gsp.transform import Matrix
    else:
        import matplotlib
        import matplotlib.pyplot as plt
        from gsp.backend.matplotlib import Canvas, Viewport, Buffer, Datatype
        from gsp.backend.matplotlib.visual import Pixels
        from gsp.backend.matplotlib.transform import Matrix

        
    vec3 = np.dtype([("x", np.float32),
                     ("y", np.float32),
                     ("z", np.float32)])
    rgba = np.dtype([("r", np.float32),
                     ("g", np.float32),
                     ("b", np.float32),
                     ("a", np.float32) ])

    canvas = Canvas(512, 512, 100, 1, False)
    viewport = Viewport(canvas, 0, 0, 512, 512)

    n = 10_000
    positions = np.random.uniform(-1, 1, (n,3)).astype(np.float32)
    colors = np.random.uniform(0, 1, (n,4)).astype(np.float32)
    colors[:,-1] = 1

    pixels = Pixels(viewport,
                    Buffer.from_numpy(positions.view(vec3)),
                    Buffer.from_numpy(colors.view(rgba)))

    from camera import Camera
    camera = Camera("perspective", theta=0, phi=0)
    transform = Matrix(camera.transform.tobytes())

    if not direct_mode:
        for command in gsp.commands():
            print(command.yaml_dump())
    else:
        pixels.render(transform)
        plt.show()


