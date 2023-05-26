# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Nicolas P. Rougier, Cyrille Rossant - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import numpy as np

    from gsp.backend.datoviz import Canvas, Viewport, Buffer, Datatype, Pixels, run

    RNG = np.random.default_rng()

    # Create a canvas.
    w = h = 512
    dpi = 100
    canvas = Canvas(w, h, dpi, 1, False)

    # Create a viewport.
    viewport = Viewport(canvas, 0, 0, w, h)

    # Number of points.
    count = 100_000

    # Implicit creation of datatype
    # -----------------------------
    vec3 = np.dtype([("x", np.float32),
                     ("y", np.float32),
                     ("z", np.float32)])
    vertices = (w*RNG.random((count, 3), np.float32)).view(vec3)
    vertices = Buffer.from_numpy(vertices)

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

    canvas._canvas.build()

    run()
