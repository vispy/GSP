# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.core.buffer import Buffer

class BufferView(Object):

    @command("core.BufferView")
    def __init__(self, buffer : Buffer,
                       key : str):

        """A BufferView is apartial view of an existing buffer
        indexed by one or several key(s).
        
        Parameters:

         buffer:
        
            Buffer to take view from

         key:
        
            Name of the field to be accessed.
        """
        
        Object.__init__(self)
        self.buffer = buffer
        self.key = key
