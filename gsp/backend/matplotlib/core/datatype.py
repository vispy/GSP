# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np

class Datatype:
    
    # Convenience method, not part of the protocol
    @classmethod
    def from_numpy(cls, dtype):
        """Convert a numpy type into a string representation"""

        literal = ""
        dtype = str(dtype)
        if dtype.startswith("["):
            for item in eval(dtype):
                if len(item) == 2:
                    iname, itype = item
                    isize = 1
                else:
                    iname, itype, isize = item
                    isize = np.prod(isize)
                iname = iname.strip()
                itype = itype.strip()
                literal += "%s:%s:%d/" % (itype,iname,isize)
        elif dtype.startswith("("):
            itype, isize = eval(dtype)
            isize = np.prod(isize)
            literal += "%s::%d/" % (itype,isize)
        else:
            literal += "%s/" % (dtype)
        return Datatype(literal[:-1])

    # Convenience method, not part of the protocol
    @classmethod
    def to_numpy(cls, literal):
        dtype = []
        literal = literal.replace(" ", "")
        for item in literal.split("/"):
            if not len(item): continue
            item = item.split(":")
            if len(item) == 3:
                itype, iname, isize = item
                if not len(iname):
                    dtype.append((itype, (int(isize),)))
                else:
                    dtype.append((iname, itype, (int(isize),)))
            elif len(item) == 2:
                itype, iname = item
                dtype.append((iname, itype, (1,)))
            elif len(item) == 1:
                itype = item[0]
                dtype.append((itype, (1,)))
        if len(dtype) == 1:
            dtype = dtype[0]
            if len(dtype) == 3: 
                return dtype[1:]
            else:
                return dtype
        else:
            return dtype
    
    def __init__(self, literal):
        self.literal = literal
        self.dtype = Datatype.to_numpy(literal)
