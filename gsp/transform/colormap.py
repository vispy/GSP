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
                 colormap : str = None,
                 vmin : float = None,
                 vmax : float = None):
        """
        Colormap transform allows to map a scalar to a color

        ```bash
        python docs/snippets/Colormap_init.py
        ```

        Parameters
        ----------
        colormap:
            Name of the colormap

        vmin :
            Minimum value or None for dynamic minimum

        vmax :
            Maximum value or None for dynamic maximum
        """
        Transform.__init__(self, __no_command__ = True)
        self._colormap = colormap
        self._vmin = vmin
        self._vmax = vmax

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
        transform._vmin = self._vmin
        transform._vmax = self._vmax
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
        norm = mpl.colors.Normalize(vmin=self._vmin or value.min(),
                                    vmax=self._vmax or value.max())
        return cmap(norm(value))
