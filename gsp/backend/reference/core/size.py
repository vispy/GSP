# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command

class Size(Object):
    
    @command("core.Size")
    def __init__(self, value : float,
                       unit : str):

        """Representation of a size in given units.

        Parameters:

         value:
        
            Actual value 

         unit:
        
            Unit to be considered when interpreting the value

            Unit can be dot, point, em, inch, mm, cm or empty.
        """
        
        Object.__init__(self)
        self.value = value
        self.unit = unit

