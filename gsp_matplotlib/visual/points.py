# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from .. import glm
from gsp import visual
from gsp.io.command import command
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color


class Points(visual.Points):

    __doc__ = visual.Points.__doc__

    @command("visual.Points")
    def __init__(self, positions   : Transform | Buffer,
                       sizes       : Transform | Buffer | float,
                       fill_colors : Transform | Buffer | Color,
                       line_colors : Transform | Buffer | Color,
                       line_widths : Transform | Buffer | float):

        super().__init__(positions, sizes, fill_colors, line_colors,
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
            collection = viewport._axes.scatter([],[])
            collection.set_antialiaseds(True)
            collection.set_linewidths(0)
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

        # Invert depth buffer values before sorting
        # This in place inversion is important for subsequent transforms
        positions[:,2] = 1 - positions[:,2]
        sort_indices = np.argsort(positions[:,2])
        collection.set_offsets(positions[sort_indices,:2])
        self.set_variable("screen[positions]", positions)


        fill_colors = self.eval_variable("fill_colors")
        if isinstance(fill_colors, np.ndarray) and (len(fill_colors) == len(positions)):
            collection.set_facecolors(fill_colors[sort_indices])
        else:
            collection.set_facecolors(fill_colors)

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

        sizes = self.eval_variable("sizes")
        if isinstance(sizes, np.ndarray) and (len(sizes) == len(positions)):
            collection.set_sizes(sizes[sort_indices])
        else:
            collection.set_sizes([sizes]*len(positions))

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
