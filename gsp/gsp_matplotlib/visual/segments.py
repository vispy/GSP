# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from .. import glm
from ...gsp import visual
from ...gsp.io.command import command
from ...gsp.transform import Transform
from ...gsp.core import Viewport, Buffer, Color, LineCap

import matplotlib.patheffects as path_effects
from matplotlib.collections import LineCollection

class Segments(visual.Segments):

    __doc__ = visual.Segments.__doc__

    @command("visual.Points")
    def __init__(self, positions   : Transform | Buffer,
                       line_caps   : Transform | Buffer | LineCap,
                       line_colors : Transform | Buffer | Color,
                       line_widths : Transform | Buffer | float):

        super().__init__(positions, line_caps, line_colors,
                         line_widths, __no_command__ = True)


    def render(self, viewport=None, model=None, view=None, proj=None):

        super().render(viewport, model, view, proj)
        model = model if model is not None else self._model
        view = view if view is not None else self._view
        proj = proj if proj is not None else self._proj

        # Disable tracking for newly created glm.ndarray (or else,
        # this will create GSP buffers)
        tracker = glm.ndarray.tracked.__tracker_class__
        glm.ndarray.tracked.__tracker_class__ = None

        # Create the collection if necessary
        if viewport not in self._viewports:
            collection = LineCollection([], clip_on=True, snap=False, capstyle="round")
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect('resize_event',
                               lambda event: self.render(viewport))

        # If render has been called without model/view/proj, we don't
        # render Such call is only used to declare that this visual is
        # to be rendered on that viewport.
        if self._transform is None:
            # Restore tracking
            glm.ndarray.tracked.__tracker_class__ = tracker
            return

        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ self._transform.T)
        positions = positions.reshape(-1,2,3)

        # Invert depth buffer values before sorting
        # This in place inversion is important for subsequent transforms
        depth = -positions[:,:,2].mean(axis=1)
        sort_indices = np.argsort(depth)

        collection.set_segments(positions[sort_indices][...,:2])
        self.set_variable("screen[positions]", positions)
        self.set_variable("screen[segments]", depth)

        line_colors = self.eval_variable("line_colors")
        if isinstance(line_colors, np.ndarray) and (len(line_colors) == len(positions)):
            collection.set_edgecolors(line_colors[sort_indices])
        else:
            collection.set_edgecolors(line_colors)

        line_widths = self.eval_variable("line_widths")
        if isinstance(line_widths, np.ndarray) and (len(line_widths) == len(positions)):
            collection.set_linewidths(line_widths[sort_indices])
        else:
            collection.set_linewidths(line_widths)

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
