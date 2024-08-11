# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.io.command import command
from gsp.transform import Transform

class Screen(Transform):

    @command("transform.Screen")
    def __init__(self, buffer : str = "positions"):
        """
        Screen transform is a JIT transform that return screen
        coordinates (including depth)

        Parameters
        ----------
        buffer :
            Name of the buffer from which to extract screen information.
            This buffer must have been built by a visual.
        """

        Transform.__init__(self,  __no_command__ = True)
        self._buffer = buffer

    def __call__(self):
        raise ValueError("Depth transform cannot be composed")

    def evaluate(self, buffers):
        """
        Evaluate the transform

        Parameters
        ----------
        buffers :
            Dictionary of buffers
        """

        if "screen" in buffers.keys():
            if self._buffer in buffers["screen"].keys():
                return buffers["screen"][self._buffer]
            else:
                raise ValueError(f"Screen buffer for {self._buffer} not found")
        else:
            raise ValueError("Screen buffer not found")

class ScreenX(Screen):
    """
    ScreenX transform is a JIT transform that return x screen coordinates.
    """

    @command("transform.ScreenX")
    def __init__(self, buffer : str = "positions"):
        Screen.__init__(self, buffer, __no_command__ = True)

    def evaluate(self, buffers):
        return super().evaluate(buffers)[..., 0]

class ScreenY(Screen):
    """
    ScreenY transform is a JIT transform that return y screen coordinates.
    """

    @command("transform.ScreenY")
    def __init__(self, buffer : str = "positions"):
        Screen.__init__(self, buffer, __no_command__ = True)

    def evaluate(self, buffers=None):
        return super().evaluate(buffers)[..., 1]

class ScreenZ(Screen):
    """
    ScreenZ transform is a JIT transform that return z (depth)
    screen coordinates.
    """

    @command("transform.ScreenZ")
    def __init__(self, buffer : str = "positions"):
        Screen.__init__(self, buffer, __no_command__ = True)

    def evaluate(self, buffers):
        return super().evaluate(buffers)[..., 2]
