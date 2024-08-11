# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from __future__ import annotations
from gsp.io.command import command
from gsp.transform import Transform

class Depth(Transform):
    """
    A depth transform is a JIT transform whose output is
    computed when a visual is rendered. For a visual with n
    vertices, the output is a Buffer of n floats containing the
    depth coordinate of each vertices.
    """

    @command("transform.Depth")
    def __init__(self, buffer : str = "positions"):
        """
        Build the transform

        Parameters
        ----------
        buffer :
            Name of the buffer from which to extract depth information.
            This buffer must have been built by a visual.
        """
        Transform.__init__(self,
                           __no_command__ = True)
        self._buffer = buffer

    def __call__(self):
        raise ValueError("Depth transform cannot be composed")

    def evaluate(self, buffers : dict):
        """
        Evaluate the transform

        Parameters
        ----------
        buffers :
            Dictionary of buffers
        """

        if "depth" in buffers.keys():
            if self._buffer in buffers["depth"].keys():
                return buffers["depth"][self._buffer]
            else:
                raise ValueError(f"Depth buffer for {self._buffer} not found")
        else:
            raise ValueError("Depth buffer not found")
