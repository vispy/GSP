# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp import visual
from gsp.io.command import command
from gsp.transform import Transform
from gsp.core import Buffer, Color, Matrix
import matplotlib.image as mpl_img
from gsp_matplotlib import glm
from gsp_matplotlib.core.viewport import Viewport
from gsp_matplotlib.core.texture import Texture


class Image(visual.Image):
    __doc__ = visual.Image.__doc__

    @command("visual.Image")
    def __init__(
        self,
        positions: Transform | Buffer,
        texture_2d: Texture,
        image_extent: tuple = (-1, 1, -1, 1),
    ) -> None:
        """
        Initialize an Image object.

        Parameters:
            positions (Transform | Buffer): A (N, 3) array of XYZ positions in object space.
            texture_2d (Texture): A Texture object containing the image to display.
            image_extent (tuple): A tuple (left, right, bottom, top) defining the extent of the image in object space.
        """

        super().__init__(positions, texture_2d, image_extent, __no_command__=True)

        self._positions = positions
        self._texture_2d = texture_2d
        self._image_extent = image_extent

    def render(
        self,
        viewport: Viewport,
        model: Matrix | None = None,
        view: Matrix | None = None,
        proj: Matrix | None = None,
    ):
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
            axe_image = mpl_img.AxesImage(
                viewport._axes,
                data=self._texture_2d.data.reshape(self._texture_2d.shape),
            )
            self._viewports[viewport] = axe_image
            viewport._axes.add_image(axe_image)

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

        axe_image: mpl_img.AxesImage = self._viewports[viewport]
        positions4d = glm.to_vec4(self._positions) @ self._transform.T
        positions3d = glm.to_vec3(positions4d)
        # FIXME here image_extent is divided by W after rotation
        # but there is nothing to compensate for the camera z
        # - should i divide by the camera's zoom ?
        projected_extent = (
            positions3d[0, 0] + self._image_extent[0] / positions4d[0, 3],
            positions3d[0, 0] + self._image_extent[1] / positions4d[0, 3],
            positions3d[0, 1] + self._image_extent[2] / positions4d[0, 3],
            positions3d[0, 1] + self._image_extent[3] / positions4d[0, 3],
        )
        axe_image.set_extent(projected_extent)

        self.set_variable("screen[positions]", positions3d)

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
