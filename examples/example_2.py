# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

if __name__ == '__main__':

    import gsp
    import numpy as np
    from gsp.core import Canvas, Viewport, Buffer, Datatype

    gsp.mode("client", reset=True, record=True, output=False)
    
    canvas   = Canvas(512, 512, 100, 1, False)
    viewport = Viewport(canvas, 0, 0, 512, 512)

    # Explicit creation of datatype
    # -----------------------------
    # vec2 = Datatype("f:x / f:y")
    # vertices = np.random.uniform(0, 512, (100,2)).astype(np.float32)
    # vertices = Buffer(100, vec2, vertices.tobytes())

    # Implicit creation of datatype
    # -----------------------------
    vertices = np.random.uniform(0, 512, (100,2)).astype(np.float32)
    vertices = Buffer.from_numpy(vertices)

    
    # Explicit creation of datatype
    # -----------------------------
    # rgba = Datatype("f:r / f:g / f:b / f:a")
    # colors = np.random.uniform(0, 512, (100,4)).astype(np.float32)
    # colors = Buffer(100, rgba, colors.tobytes())
    
    # Implicit creation of datatype
    # -----------------------------
    colors = np.random.uniform(0, 512, (100,4)).astype(np.float32)
    colors = Buffer.from_numpy(colors)

    
#    scatter = gsp.visual.pixels(viewport, vertices, colors)
#    canvas.render()

    for command in gsp.commands():
        print(command.yaml_dump())

