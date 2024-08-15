# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

import numpy as np
from gsp import Object
from gsp.core import Buffer
from gsp.io.command import command
from gsp.core import Viewport, Buffer
from gsp.transform import Transform


class Visual(Object):
    """
    Generic Visual
    """

    @command("visual.Visual")
    def __init__(self):
        """ Generic visual """

        Object.__init__(self) #, __no_command__ = True)

        self._in_variables = { }
        self._out_variables = { }
        self._viewports = {}
        self._model = np.eye(4)
        self._view = np.eye(4)
        self._proj = np.eye(4)
        self._transform = np.eye(4)

    def set_variable(self, name, value):
        """
        Store variable name with given value

        Parameters
        ----------
        name : string
            Name of the variable to store
        value : any
            Value of the variable to store
        """

        if name in self._in_variables.keys():
            self._in_variables[name] = value
        elif name in self._out_variables.keys():
            self._out_variables[name][...] = value
        else:
            raise IndexError(f"Unknown variable ({name})")

    def get_variable(self, name):
        """
        Retrieve variable *name* (without evaluation)

        Parameters
        ----------
        name : string
            Name of the variable to retrieve
        """

        if name in self._in_variables.keys():
            return self._in_variables[name]
        elif name in self._out_variables.keys():
            return self._out_variables[name]
        raise IndexError(f"Unknown variable ({name})")

    def eval_variable(self, name):
        """
        Evaluate and return variable *name*

        Parameters
        ----------
        name : string
            Name of the variable to evaluate
        """

        value = self.get_variable(name)
        if isinstance(value, Transform):
            value = value.evaluate(self._in_variables | self._out_variables)
        elif isinstance(value, (Buffer,np.ndarray)):
            value = np.asanyarray(value)
        return np.atleast_1d(value)

    @command()
    def render(self, viewport, model=None, view=None, proj=None):
        """
        Render the visual on viewport using the given model,
        view, proj matrices

        Parameters
        ----------
        viewport : Viewport
            Viewport where to render the visual
        model : mat4
            Model matrix to use for rendering
        view : mat4
            View matrix to use for rendering
        proj : mat4
            Projection matrix to use for rendering
        """

        # We store the model/view/proj matrices for resize events
        if model is not None:
            self._model = model
        if view is not None:
            self._view = view
        if proj is not None:
            self._proj = proj

        self._transform = self._proj @ self._view @ self._model
        self.set_variable("viewport", viewport)
