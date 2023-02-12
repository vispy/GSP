# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.core import Buffer
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.transform import Transform

class Colormap(Transform):

    @command("transform.Colormap")
    def __init__(self, colormap : str = None):
        """Colormap transform allows to map a scalar to a color

        parameters:

          colormap:

            Name of the colormap
        """
        
        
        Transform.__init__(self, __no_command__ = True)
        self._colormap = colormap

    @property
    def colormap(self):
        return self._colormap
        
    @command()
    def set_colormap(self, colormap : str = None):
        """Set the colormap

        parameters:

          colormap:

            Name of the colormap
        """
        
        self._colormap = colormap
        
    def copy(self):
        transform = Transform.copy(self)
        transform.set_colormap (self._colormap)
        return transform
        
