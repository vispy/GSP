# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp.gsp import core, log
from gsp.gsp_matplotlib import glm
import matplotlib.pyplot as plt
import time

class Camera():
    """
    Interactive trackball camera.

    This camera can be used for static or interactive rendering with mouse
    controlled movements. In this latter case, it is necessary to connect the
    camera to a matplotlib axes using the `connect` method and to provide an
    update function that will be called each time an update is necessary
    relatively to the new transform.

    In any case, the camera transformation is kept in the `Camera.transform`
    variable.
    """

    def __init__(self, mode="perspective", theta=0, phi=0, zoom = 1.0, zdist=5.0, scale=1, log_fps=False):
        """
        mode : str
          camera mode ("ortho" or "perspective")

        theta: float
          angle around z axis (degrees)

        phi: float
          angle around x axis (degrees)

        zoom : float
          Zoom level           

        zdist : float
          Distance of the camera on the z-axis

        scale: float
          scale factor

        log_fps: bool
          If True, log the frames per second (FPS) during rendering. Good for performance monitoring.
        """

        self.aperture = 35
        self.aspect = 1
        self.near = 1
        self.far = 100
        self.mode = mode
        self.scale = scale
        self.zoom = zoom
        self.zoom_max = 5.0
        self.zoom_min = 0.1
        self.log_fps = log_fps

        if mode == "ortho":
            self.proj = glm.ortho(-1,+1,-1,+1, self.near, self.far)
            self.trackball = None
            self.view = np.eye(4)
            self.model = np.eye(4)
        else:
            self.trackball = glm.Trackball(theta, phi)
            self.proj = glm.perspective(
                self.aperture, self.aspect, self.near, self.far)
            self.view = glm.translate((0, 0, -zdist)) @ glm.scale((scale,scale,scale))
            self.model = self.trackball.model.T
        self.updates = {"motion"  : [],
                        "scroll"  : [],
                        "press"   : [],
                        "release" : []}

    def run(self):
        """
        Run the camera
        """

        self.update("motion")
        plt.show()

    def save(self, filename):
        """
        Save current camera output to filename
        """

        self.update("motion")
        plt.savefig(filename)


    def update(self, event):
        """
        Update all connected objects
        """

        for update in self.updates[event]:
            update(self.viewport, self.model, self.view, self.proj)

    def canvas_draw(self):
        """
        Draw the canvas. And measure the time taken to render if log_fps is True.
        """
        if self.log_fps:
            time_start = time.time()
    
        self.figure.canvas.draw()
    
        if self.log_fps:
            time_end = time.time()
            render_time = time_end - time_start
            fps = 1 / render_time
            log.info(f"Canvas drawn in {fps:.2f} fps")

    def connect(self, viewport: core.Viewport, event: str, update):
        """
        viewport: core.Viewport
           The viewport to connect the camera to

        event: string
           Which event to connect to (motion, scroll, press, release)

        update: function(transform)
           Function to be called with the new transform to update the scene
           (transform is a 4x4 matrix).
        """

        self.viewport = viewport
        self.axes = viewport._axes
        self.figure = self.axes.get_figure()

        # self.update = update
        if update not in self.updates[event]:
            self.updates[event].append(update)

        self.mouse = None
        self.cidscroll = self.figure.canvas.mpl_connect(
            'scroll_event', self.on_scroll)
        self.cidpress = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

        def format_coord(*args):
            phi = self.trackball.phi
            theta = self.trackball.theta
            return "Θ : %.1f, ɸ: %.1f" % (theta, phi)
        if self.trackball is not None:
            self.axes.format_coord = format_coord

        xlim = self.axes.get_xlim()[1]
        ylim = self.axes.get_ylim()[1]
        aspect = ylim/xlim
        self.axes.zoom = self.zoom
        self.axes.set_xlim(-self.zoom, self.zoom)
        self.axes.set_ylim(-self.zoom*aspect, self.zoom*aspect)
        self.canvas_draw()


    def on_scroll(self, event):
        """
        Scroll event for zooming in/out
        """
        if event.inaxes != self.axes:
            return

        if event.button == "up":
            self.zoom  = max(0.9*self.zoom, self.zoom_min)
        elif event.button == "down":
            self.zoom = min(1.1*self.zoom, self.zoom_max)

        xlim = self.axes.get_xlim()[1]
        ylim = self.axes.get_ylim()[1]
        aspect = ylim/xlim
        self.axes.zoom = self.zoom
        self.axes.set_xlim(-self.zoom, self.zoom)
        self.axes.set_ylim(-self.zoom*aspect, self.zoom*aspect)
        self.update("scroll")
        self.canvas_draw()


    def on_press(self, event):
        """
        Press event (initiate drag)
        """
        if event.inaxes != self.axes:
            return

        self.mouse = event.button, event.xdata, event.ydata
        self.update("press")
        self.canvas_draw()


    def on_motion(self, event):
        """
        Motion event to rotate the scene
        """
        if self.mouse is None:            return
        if event.inaxes != self.axes:     return
        if self.trackball is None:        return

        button, x, y = event.button, event.xdata, event.ydata
        dx, dy = x-self.mouse[1], y-self.mouse[2]
        self.mouse = button, x, y
        self.trackball.drag_to(x, y, dx, dy)
        self.model = self.trackball.model.T
        self.update("motion")
        self.canvas_draw()


    def on_release(self, event):
        """
        Release event (end of drag)
        """
        self.mouse = None
        self.update("release")
        self.canvas_draw()


    def disconnect(self):
        """
        Disconnect camera from the axes
        """
        self.figure.canvas.mpl_disconnect(self.cidscroll)
        self.figure.canvas.mpl_disconnect(self.cidpress)
        self.figure.canvas.mpl_disconnect(self.cidrelease)
        self.figure.canvas.mpl_disconnect(self.cidmotion)