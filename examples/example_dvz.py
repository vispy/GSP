# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Nicolas P. Rougier, Cyrille Rossant - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import gsp
    import numpy as np

    # GSP direct mode
    # import matplotlib
    # import matplotlib.pyplot as plt
    from gsp.backend.datoviz import \
        Canvas, Viewport, Buffer, Datatype, Pixels
    from gsp.backend.datoviz import default_app

    RNG = np.random.default_rng()
    count = 1_000_000
    canvas = Canvas(512, 512, 100, 1, False)
    viewport = Viewport(canvas, 0, 0, 512, 512)

    # Explicit creation of datatype
    # -----------------------------
    # vec2 = Datatype("f:x / f:y")
    # vertices = np.random.uniform(0, 512, (100,2)).astype(np.float32)
    # vertices = Buffer(100, vec2, vertices.tobytes())

    # Implicit creation of datatype
    # -----------------------------
    vec3 = np.dtype([("x", np.float32),
                     ("y", np.float32),
                     ("z", np.float32)])
    vertices = (512*RNG.random((count, 3), np.float32)).view(vec3)
    vertices = Buffer.from_numpy(vertices)

    # count = 52
    # vertices = np.zeros((count, 3), dtype=np.float32)
    # t = np.linspace(-1, 1, count, dtype=np.float32)
    # vertices[:, 0] = 256 + 256*.75 * np.cos(np.pi*t)
    # vertices[:, 1] = 256 + 256*.75 * np.sin(np.pi*t)
    # vertices = vertices.view(vec3)

    # Explicit creation of datatype
    # -----------------------------
    # rgba = Datatype("f:r / f:g / f:b / f:a")
    # colors = np.random.uniform(0, 512, (100,4)).astype(np.float32)
    # colors = Buffer(100, rgba, colors.tobytes())

    # Implicit creation of datatype
    # -----------------------------
    rgba = np.dtype([("r", np.float32),
                     ("g", np.float32),
                     ("b", np.float32),
                     ("a", np.float32)])
    colors = (np.ones((count, 4), np.float32)).view(rgba)
    colors["a"] = 1
    colors = Buffer.from_numpy(colors)

    scatter = Pixels(viewport, vertices, colors)

    # Direct mode
    default_app().run()

    # Client mode
    # for command in gsp.commands():
    #     print(command.yaml_dump())
