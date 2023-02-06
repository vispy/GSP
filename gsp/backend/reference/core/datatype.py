# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference import (Object, command)


class Datatype(Object):
    
    @command("core.Datatype")
    def __init__(self, format : str):
        """A datatype describes the structure of a chunk of
        memory. The literal description of the type is a `/` separated
        list of atomic items of the form `type[:name][:count] / … /
        type[:name][:count]` where `name` is a valid identifier, count
        is a strictly positive integer and `type` is one of:
        
        Type     | Alias | Description                            | Size    | Comment                            |
        -------- | ----- | -------------------------------------- | ------- | ---------------------------------- |
        bool     | `?`   | boolean                                |  8 bits |                                    |
        byte     | `b`   | signed integer                         |  8 bits |                                    |
        short    | `s`   | signed integer                         | 16 bits |                                    |
        int      | `i`   | signed integer                         | 32 bits |                                    |
        ubyte    | `B`   | unsigned integer                       |  8 bits |                                    |
        ushort   | `S`   | unsigned integer                       | 16 bits |                                    |
        uint     | `I`   | unsigned integer                       | 32 bits |                                    |
        half     | `e`   | half-precision floating-point number   | 16 bits |  5 bits exponent, 10 bits mantissa |
        float    | `f`   | single-precision floating-point number | 32 bits |  8 bits exponent, 23 bits mantissa |
        double   | `d`   | double-precision floating-point number | 64 bits | 11 bits exponent, 52 bits mantissa |
        datetime | `Y`   | date/time representation               | 64 bits | Offset from 1970-01-01T00:00:00    |


        Parameters:

          format:

            Literal description of the type
        
        **Note**

        - Spaces are non significant

        """
        
        Object.__init__(self)
        self.format = format

    @property
    def size(self):
        
        sizes = {"?" : 1, "b" : 1, "B" : 1,
                 "s" : 2, "S" : 2, "e" : 2,
                 "i" : 4, "I" : 4, "f" : 4,
                 "d" : 8, "Y" : 8 }
        regex = r"(?P<type>[?bsiBSIefdY]):(?P<name>[a-zA-Z0-9]*):(?P<count>[0-9]+)"
        size = 0
        for (dtype,name,count) in re.findall(regex, self.literal):
            size += sizes[dtype]*int(count)
        return size

