import numpy as np
import gsp

def main(core: gsp.core, visual: gsp.visual) -> tuple[gsp.core.viewport.Canvas, gsp.core.viewport.Viewport, list[gsp.visual.visual.Visual]]:

    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
    n = 250_000
    P = gsp.glm.to_vec3(np.random.uniform(-1, +1, (n,2)))
    pixels = visual.Pixels(P, colors=[0,0,0,1])
    pixels.render(viewport)

    visuals = [pixels]
    return (canvas, viewport, visuals)

####################################################

if __name__ == "__main__":
    from .example_argparse import ExampleArgsParse

    # Parse command line arguments
    gsp_core, gsp_visual = ExampleArgsParse.parse(
        example_description="Example showing how to render a large number of pixels. NOTE: still buggy as it uses raw buffers"
    )

    # Run the main function
    canvas, viewport, visuals = main(core=gsp_core, visual=gsp_visual)

    # Show or save the result
    ExampleArgsParse.show(canvas, viewport, visuals)