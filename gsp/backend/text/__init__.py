# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — json backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp
from gsp.backend.reference.command import Command, Converter, command

def text_dump(self):

    id = self.parameters["id"]

    # Call pending conversions
    # for key,value in self.parameters.items():
    #    if isinstance(value, Converter):
    #        value()

    if (self.methodname is None or
        not len(self.methodname) or
        "." in self.methodname):
        print("#%03d: Creation of %s(id=%d)" % (self.id, self.classname, id))
    else:
        print("#%03d: %s(id=%d) → %s(…)" % (
            self.id, self.classname, id, self.methodname))
    for key,value in self.parameters.items():
        if isinstance(value, Converter):
            print("      | %s: %s (%s)" % (key, type(value.value).__name__, value.converter.__name__))
        else:
            print("      | %s: %s" % (key, type(value).__name__))
        
    
Command.dump = text_dump

import gsp.backend.reference.core as core
import gsp.backend.reference.visual as visual
import gsp.backend.reference.transform as transform
from gsp.backend.reference import (mode, objects, commands, process)

gsp.mode = "client"
gsp.core = core
gsp.visual = visual
gsp.tranform = transform
