# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

import numpy as np
from gsp import glm
from gsp import visual
from gsp.io.command import command
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color

class Pixels(visual.Pixels):

    __doc__ = (visual.Pixels.__doc__ +
    """
    !!! Notes "Notes on matplotlib implementation"

        Even with antialias off, marker coverage leaks on neighbouring
        pixels if the position is not an exact divider of viewport
        size (in pixels). Vertices coordinates could be rounded at
        time of rendering but it is easier to set a very small size
        whose coverage is more or less guaranteed to be one
        pixel. However, this size seems to be wrong on Windows,
        depending on the screen size.
    """)

    @command("visual.Pixels")
    def __init__(self, positions : Transform | Buffer,
                       colors : Transform | Buffer | Color):
        super().__init__(positions, colors, __no_command__ = True)


    def render(self, viewport, model=None, view=None, proj=None):

        super().render(viewport, model, view, proj)

        # Disable tracking for newly created glm.ndarray (or else,
        # this will create GSP buffers)
        tracker = glm.ndarray.tracked.__tracker_class__
        glm.ndarray.tracked.__tracker_class__ = None

        # Create the collection if necessary
        if viewport not in self._viewports:
            size = 0.25*(72/viewport._canvas._dpi)**2
            collection = viewport._axes.scatter( [],[], size)
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
        # positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ self._transform.T)
        sort_indices = np.argsort(positions[:,2])
        collection.set_offsets(positions[sort_indices,:2])

        self.set_variable("screen[positions]", positions)

        colors = self.eval_variable("colors")
        if colors is not None:
            if isinstance(colors, np.ndarray) and len(colors) == len(positions):
                collection.set_facecolors(colors[sort_indices])
            else:
                collection.set_facecolors(colors)


        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
