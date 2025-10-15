# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp import visual
from gsp.io.command import command
import gsp_matplotlib.core as mpl_core
import gsp_matplotlib.glm as glm


class Volume(visual.Volume):
    """
    3D Volume visual representation.
    """

    __doc__ = visual.Volume.__doc__

    @command("visual.Volume")
    def __init__(
        self,
        texture_3d: mpl_core.Texture,
        bounds_3d: tuple = ((-1, 1), (-1, 1), (-1, 1)),
        point_size: float = 10.0,
        downsample_ratio: float = 1.0,
        alpha_factor: float = 1.0,
        jitter_position_factor: float = 0.0,
        remove_invisible_points_enabled: bool = True,
    ):
        """
        Initialize a 3D volume.

        Args:
            texture_3d (mpl_core.Texture): The 3D texture to use for the volume.
            bounds_3d (tuple[tuple[float, float], tuple[float, float], tuple[float, float]]): The 3D bounds of the volume.
            point_size (float): The size of the points in the volume.
            downsample_ratio (float): The ratio to downsample the volume. percent of original number of point to keep
            alpha_factor (float): The factor to apply to the alpha channel of each point color.
            jitter_position_factor (float): The factor to apply to the jittering of positions. It helps to reduce moire patterns.
            remove_invisible_points_enabled (bool): Whether to remove invisible points aka points with alpha = 0.
        """
        volume_depth = texture_3d.shape[0]
        volume_height = texture_3d.shape[1]
        volume_width = texture_3d.shape[2]

        ############
        # Sanity checks for __init__ arguments
        #

        # sanity check - bounds_3d shape MUST be (3, 2)
        assert np.shape(bounds_3d) == (3, 2)

        # sanity check - volume shape
        assert volume_depth > 0
        assert volume_height > 0
        assert volume_width > 0

        #############
        # Convert volume_data in a grid for `positions` and `fill_colors`
        #

        # Create a grid of normalized coordinates directly in meshgrid
        x_min, x_max = bounds_3d[0]
        y_min, y_max = bounds_3d[1]
        z_min, z_max = bounds_3d[2]
        coordinate_z, coordinate_y, coordinate_x = np.meshgrid(
            np.linspace(z_min, z_max, volume_depth),
            np.linspace(y_min, y_max, volume_height),
            np.linspace(x_min, x_max, volume_width),
            indexing="ij",  # ensures (z,y,x) ordering
        )

        # Stack into (N, 3) array of positions
        positions = np.stack([coordinate_x.ravel(), coordinate_y.ravel(), coordinate_z.ravel()], axis=-1).reshape(-1, 3)
        fill_colors = texture_3d.data.reshape(-1, 4)  # rgba per point

        ############
        # Downsample the positions and fill_colors
        #

        point_to_keep = int(downsample_ratio * len(positions))
        indices = np.random.choice(len(positions), size=point_to_keep, replace=False)
        positions = positions[indices]
        fill_colors = fill_colors[indices]

        ############
        # optimisation: remove all positions and fill_colors where alpha is 0. it would be invisible anyways
        #

        if remove_invisible_points_enabled:
            positions = positions[fill_colors[..., 3] > 0]
            fill_colors = fill_colors[fill_colors[..., 3] > 0]

        ############
        # multiply alpha (the forth dimension) of fill_colors
        #

        fill_colors[..., 3] *= alpha_factor

        ############
        # Fake way to remove moire patterns
        #

        if jitter_position_factor != 1:
            positions += jitter_position_factor * np.random.normal(0, 1, positions.shape)

        ############
        # Initialize the parent class
        #

        super().__init__(
            positions=positions,
            sizes=point_size,
            fill_colors=fill_colors,
            __no_command__=True,
        )

    def render(self, viewport=None, model=None, view=None, proj=None):
        """
        Render the volume in the given viewport.
        Heavily inspired by `visual.points`
        """

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
            collection = viewport._axes.scatter([], [])
            collection.set_antialiaseds(True)
            collection.set_linewidths(0)
            self._viewports[viewport] = collection
            viewport._axes.add_collection(collection, autolim=False)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            canvas = viewport._canvas._figure.canvas
            canvas.mpl_connect("resize_event", lambda event: self.render(viewport))

        # If render has been called without model/view/proj, we don't
        # render Such call is only used to declare that this visual is
        # to be rendered on that viewport.
        if self._transform is None:
            # Restore tracking
            glm.ndarray.tracked.__tracker_class__ = tracker
            return

        collection = self._viewports[viewport]
        positions = self.eval_variable("positions")
        positions = positions.reshape(-1, 3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ self._transform.T)

        # Invert depth buffer values before sorting
        # This in place inversion is important for subsequent transforms
        positions[:, 2] = 1 - positions[:, 2]
        sort_indices = np.argsort(positions[:, 2])
        collection.set_offsets(positions[sort_indices, :2])
        self.set_variable("screen[positions]", positions)

        fill_colors = self.eval_variable("fill_colors")
        if isinstance(fill_colors, np.ndarray) and (len(fill_colors) == len(positions)):
            collection.set_facecolors(fill_colors[sort_indices])
        else:
            collection.set_facecolors(fill_colors)

        sizes = self.eval_variable("sizes")
        if isinstance(sizes, np.ndarray) and (len(sizes) == len(positions)):
            collection.set_sizes(sizes[sort_indices])
        else:
            collection.set_sizes([sizes] * len(positions))

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
