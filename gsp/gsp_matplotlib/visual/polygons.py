# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from .. import glm
from ...gsp import visual
from ...gsp.io.command import command
from ...gsp.transform import Transform
from ...gsp.core import Viewport, List, Buffer, Color, Measure, LineStyle, LineJoin

from matplotlib.collections import PolyCollection

class Polygons(visual.Polygons):

    __doc__ = visual.Polygons.__doc__

    @command("visual.Polygons")
    def __init__(self, positions    : Transform | Buffer,
                       indices      : Transform | Buffer | List | int,
                       fill_colors  : Transform | Buffer | Color,
                       line_colors  : Transform | Buffer | Color,
                       line_widths  : Transform | Buffer | float,
                       line_styles  : Transform | Buffer | LineStyle,
                       line_joins   : Transform | Buffer | LineJoin):
        
        super().__init__(positions, indices, fill_colors, line_colors,
                         line_widths, line_styles, line_joins, __no_command__ = True)


    def render(self, viewport=None, model=None, view=None, proj=None):

        super().render(viewport, model, view, proj)
        model = model if model is not None else self._model
        view = view if view is not None else self._view
        proj = proj if proj is not None else self._proj

        # Disable tracking for newly created glm.ndarray (or else,
        # this will create GSP buffers)
        tracker = glm.ndarray.tracked.__tracker_class__
        glm.ndarray.tracked.__tracker_class__ = None


        # 1. First things first, how many polygons?

        # 2. Second thing to check, can we use a single collection?

        # 3. Third do we need to initialize / re-initialize ?
        
        
        # Create the collection if necessary
        if viewport not in self._viewports:
            collection = PolyCollection([], clip_on=True, snap=False)
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

        # Project positions onto screen
        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ self._transform.T)

        # Here we consider all the case of indices shape
        indices = self.eval_variable("indices")

        # Integer means polygons of equal size, consecutive vertices
        if isinstance(indices, (int)):
            size  = indices
            count = len(positions) // size
            polygons = [positions[i*size:(i+1)*size] for i in np.arange(count)]

        # Buffer / array means path of different sizes, consecutive vertices
        elif isinstance(indices, (Buffer, np.ndarray)):
            start = 0
            end = 0
            polygons = []
            for size in indices:
                end += size
                polygons.append (positions[start:end])
                start = end

        # List / list means indirect vertices
        elif isinstance(indices, (List, list, glm.vlist)):
            polygons = []
            for index in indices:
                polygons.append (positions[index].reshape(-1,3))
                
        # We sort polygons according to the mean depth of vertices composing the path
        # (we could used instead minimum or maximum depth among all the vertices)
        depth = [-p[...,2].mean() for p in polygons]
        sort_indices = np.argsort(depth)

        self.set_variable("screen[positions]", positions.reshape(-1,3))
        self.set_variable("screen[polygons]", [np.mean(path, axis=0) for path in polygons])
        polygons = [polygons[i][...,:2] for i in sort_indices]
        collection.set_paths(polygons)

        # Fil colors
        fill_colors = self.eval_variable("fill_colors")
        if isinstance(fill_colors, np.ndarray):
            # Number of color == number of polygons
            if len(fill_colors) == len(polygons):
                collection.set_facecolors(fill_colors[sort_indices])
            # Number of colors == number of vertices
            elif len(fill_colors) == len(positions):
                raise NotImplementedError("Per vertex line color is not available")
            else:
                collection.set_facecolors(fill_colors)
        # Unique fill color
        else:
            collection.set_facecolors(fill_colors)

        # Line colors
        line_colors = self.eval_variable("line_colors")
        if isinstance(line_colors, np.ndarray):
            # Number of color == number of polygons
            if len(line_colors) == len(polygons):
                collection.set_edgecolors(line_colors[sort_indices])
            # Number of colors == number of vertices
            elif len(line_colors) == len(positions):
                raise NotImplementedError("Per vertex line color is not available")
            else:
                collection.set_edgecolors(line_colors)
        # Unique line color
        else:
            collection.set_edgecolors(line_colors)

        # Line_widths
        line_widths = self.eval_variable("line_widths")
        if isinstance(line_widths, np.ndarray):
            # Number of widths == number of polygons
            if len(line_widths) == len(polygons):
                collection.set_linewidths(line_widths[sort_indices].ravel())
            # Number of colors == number of vertices
            elif len(line_widths) == len(positions):
                raise NotImplementedError("Per vertex line widths is not available")
            else:
                collection.set_linewidths(line_widths)
        # Unique line width
        else:
            collection.set_linewidths(line_widths)

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
