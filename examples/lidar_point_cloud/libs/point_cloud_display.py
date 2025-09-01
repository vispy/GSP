# Experiment to handle intellisense in VSCode
import matplotlib.figure
import numpy as np

from . camera import Camera
from gsp.matplotlib import core, visual, glm
import gsp as gsp

"""
Library to display point clouds using GSP.
"""

def display_gsp(point_positions: np.ndarray, point_colors: np.ndarray, canvas_width=1024, canvas_height=1024):
    """
    Display the point cloud using GSP's visual.Pixels.
    """

    # Create a canvas and viewport
    canvas = core.Canvas(canvas_width, canvas_height, 100.0)
    viewport = core.Viewport(canvas, 0, 0, canvas_width, canvas_height, [1,1,1,1])

    # Create a Pixels visual
    # pixels = visual.Pixels(point_positions, colors=gsp.black)
    pixels = visual.Pixels(point_positions, colors=point_colors)

    # display in points
    # sizes = glm.float(len(point_positions))
    # sizes[...] = 40
    # pixels = visual.Points(point_positions, sizes, gsp.grey, gsp.black, [0.5])
    # pixels = visual.Points(point_positions, sizes, point_colors, gsp.black, [0])

    # Connect the camera to the viewport
    camera = Camera("perspective", theta=-30, phi=0, log_fps_enabled=True, scale=5.0)

    camera.connect(viewport, "motion", pixels.render)

    # Render the pixels visual
    print('Rendering pixels visual...')
    camera.run()

def display_gsp_dual_resolution(point_positions: np.ndarray, point_colors: np.ndarray):
    """
    Display the point cloud using GSP's visual.Pixels.

    TODO: it is halfbacked. not yet finished
    """

    # Create a canvas and viewport
    canvas = core.Canvas(256, 256, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 256, 256, [1,1,1,1])

    # Create a Pixels visual
    pixels_monochrome = visual.Pixels(point_positions, colors=gsp.grey)
    pixels_color = visual.Pixels(point_positions, colors=point_colors)

    # display in points
    # sizes = glm.float(len(point_positions))
    # sizes[...] = 30
    # pixels = visual.Points(point_positions, sizes, gsp.grey, gsp.black, [0])
    # pixels = visual.Points(point_positions, sizes, point_colors, gsp.black, [0])

    # Connect the camera to the viewport
    camera = Camera("perspective", theta=-30, phi=0, log_fps_enabled=True)

    def update(viewport, model, view, proj):
        if mode_low_res:
            # Render in low resolution
            pixels_monochrome.render(viewport, model, view, proj)
        else:
            # Render in high resolution
            pixels_color.render(viewport, model, view, proj)

    camera.connect(viewport, "motion", update)

    # kludge to display key presses
    mode_low_res = False
    def on_key_press(event):
        # gsp.log.info(f'Key pressed: {event.key}')
        if event.key != 'shift':
            return
        nonlocal mode_low_res
        mode_low_res = True
        # update(viewport, camera.model, camera.view, camera.proj)
        print(f'Low resolution mode: {mode_low_res}')

    def on_key_release(event):
        # gsp.log.info(f'Key released: {event.key}')
        if event.key != 'shift':
            return
        nonlocal mode_low_res
        mode_low_res = False
        # update(viewport, camera.model, camera.view, camera.proj)
        print(f'Low resolution mode: {mode_low_res}')

    camera.figure.canvas.mpl_connect('key_press_event', on_key_press)
    camera.figure.canvas.mpl_connect('key_release_event', on_key_release)


    # Render the pixels visual
    print('Rendering pixels visual...')
    camera.run()

