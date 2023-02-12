# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.core import Buffer
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.transform import Transform


class Accessor(Transform):

    @command("transform.Accessor")
    def __init__(self, key : str = None):
        """
        Accessor transform allows to access a specific field in a Buffer.

        parameters:

          key:

            Name of the field to access
        """
        
        Transform.__init__(self, __no_command__ = True)
        self._key = key

    @property
    def key(self):
        """Name of the field to access"""
        
        return self._key
            
    @command()
    def set_key(self, key : str):
        """Set key

        Parameters:

          key:

            Name of the field to access
        """

        self._key = key

    def copy(self):
        transform = Transform.copy(self)
        transform.set_key(self._key)
        return transform
                    

class X(Accessor):

    @command("transform.X")
    def __init__(self):
        "X Accessor (first field)"
        Accessor.__init__(self, "x", __no_command__ = True)

class Y(Accessor):

    @command("transform.Y")
    def __init__(self):
        "Y Accessor (second field)"
        Accessor.__init__(self, "y", __no_command__ = True)

class Z(Accessor):

    @command("transform.Z")
    def __init__(self):
        "Z Accessor (third field)"
        Accessor.__init__(self, "z", __no_command__ = True)

class W(Accessor):

    @command("transform.W")
    def __init__(self):
        "W Accessor (fourth field)"
        Accessor.__init__(self, "w", __no_command__ = True)

class R(Accessor):

    @command("transform.R")
    def __init__(self):
        "R Accessor (first field)"
        Accessor.__init__(self, "r", __no_command__ = True)

class G(Accessor):

    @command("transform.G")
    def __init__(self):
        "G Accessor (second field)"
        Accessor.__init__(self, "g", __no_command__ = True)

class B(Accessor):

    @command("transform.B")
    def __init__(self):
        "B Accessor (third field)"
        Accessor.__init__(self, "b", __no_command__ = True)

class A(Accessor):

    @command("transform.A")
    def __init__(self):
        "A Accessor (fourth field)"
        Accessor.__init__(self, "a", __no_command__ = True)


