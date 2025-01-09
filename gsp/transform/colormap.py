# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.core import Buffer
from gsp.io.command import command
from gsp.transform import Transform

class Colormap(Transform):
    """
    Colormap transform allows to map a scalar to a color
    """

    @command("transform.Colormap")
    def __init__(self,
                 colormap : str = None):
        """
        Colormap transform allows to map a scalar to a color

        ```bash
        python docs/snippets/Colormap_init.py
        ```

        Parameters
        ----------
        colormap:
            Name of the colormap
        """
        Transform.__init__(self, __no_command__ = True)
        self._colormap = colormap

    @command()
    def set_colormap(self, colormap : str ):
        """
        Set the colormap

        ```bash
        python docs/snippets/Colormap_set_colormap.py
        ```

        Parameters
        ----------
        colormap:
            Name of the colormap
        """
        pass

    def copy(self):
        """
        Copy the transform
        """

        transform = Transform.copy(self)
        transform._colormap = self._colormap
        return transform


    def evaluate(self, buffers : list):
        """
        Evaluate the transform using given buffers
        """

        import matplotlib as mpl
        import matplotlib.pyplot as plt

        if self._next:
            value = self._next.evaluate(buffers)
        else:
            value = self._buffer
        cmap = plt.get_cmap(self._colormap)
        norm = mpl.colors.Normalize(vmin=value.min(), vmax=value.max())
        return cmap(norm(value))
