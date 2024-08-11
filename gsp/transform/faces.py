# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.io.command import command
from gsp.transform import Transform

class Faces(Transform):
    """
    Faces transform is a JIT transform that return the faces
    buffer when it exists.
    """

    @command("transform.Faces")
    def __init__(self):

        Transform.__init__(self, __no_command__ = True)

    def __call__(self):
        raise ValueError("Faces transform cannot be composed")

    def evaluate(self, buffers=None):
        """
        Evaluate the transform

        Parameters
        ----------
        buffers :
            Dictionary of buffers
        """

        if "faces" in buffers.keys():
            return buffers["faces"]
        else:
            raise ValueError("Faces buffer not found")
