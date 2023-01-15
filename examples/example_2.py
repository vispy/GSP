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
                
    # -------------------------------------------------------------------
    RNG = np.random.default_rng()
    count = 10_000
    canvas = Canvas(512, 512, 100, 1, False)
    viewport = Viewport(canvas, 10, 10, 512-20, 512-20)
    
    vec3 = Datatype("f:x/f:y/f:z")
    vertices = 2*RNG.random((count,3), np.float32) - 1
    vertices = Buffer(count, vec3, vertices.tobytes())
    
    vec4 = Datatype("f:r/f:g/f:b/f:a")
    colors = np.zeros((count,4), np.float32)
    colors[:,3] = 1
    colors = Buffer(count, vec4, colors.tobytes())

    from camera import Camera
    camera = Camera("perspective", theta=0, phi=0)
    transform = Matrix(camera.transform.tobytes())
    
    scatter = Pixels(viewport, vertices, colors, transform)
    # -------------------------------------------------------------------
    
    if not direct_mode:
        for command in gsp.commands():
            print(command.yaml_dump())
    else:
        plt.show()


