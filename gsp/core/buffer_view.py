# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.core.object import Object
from gsp.core.command import command
from gsp.core.buffer import Buffer

class BufferView(Object):

    @command("")
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
