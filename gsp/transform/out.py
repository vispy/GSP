# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from __future__ import annotations
from ..io.command import command
from ..transform import Transform

class Out(Transform):
    """
    An out transform is a just in time (JIT) transform that allows to access
    a variable that is produced by a visual during rendering.
    """

    @command("transform.Out")
    def __init__(self, name : str = None):
        """
        Build the transform

        Parameters
        ----------
        name:
            Name of the buffer that have been produced by the visual.
            A specific key can be specified using the dot notation
            (e.g. "screen.x", "screen.yx").
        """
        Transform.__init__(self, __no_command__ = True)
        self.name = name

    def __call__(self):
        raise ValueError("Out transform cannot be composed")

    def copy(self):
        """
        Copy the transform
        """

        transform = self.__class__()
        transform.set_buffer(self._buffer)
        transform.set_base(self.base)
        transform.name = self.name
        if self._next:
            transform.set_next(self._next.copy())
        return transform


    def evaluate(self, variables : dict):
        """
        Evaluate the transform

        Parameters
        ----------
        variables :
            Dictionary of out variables produced by a visual
        """

        if "." in self.name:
            name = self.name.split(".")[0]
            key = self.name.split(".")[-1]
            for swizzle in ["xyzw", "rgba"]:
                if set(key).issubset(set(swizzle)):
                    index = [swizzle.index(c) for c in key]
                    break
        else:
            name = self.name
            index = None

        if name in variables.keys():
            variable = variables[name]
            if index is not None:
                return variable[..., index]
            else:
                return variable
        else:
            raise ValueError(f"Variable {name} not found")
