# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command

class Buffer(Object):
    
    @command("core.Buffer")
    def __init__(self, count : int,
                       dtype : str,
                       data  : bytes):

        """Uni-dimensional buffer with `count` elements of type
        `dtype` with content equal to `data`.
        
        Parameters:

         count:
        
            Number of elements

         dtype:
        
            Element datatype

         data:
        
            Content of the buffer


        !!! Note

            A datatype describes the structure of a chunk of memory. The
            literal description of the type is a `/` separated list of
            atomic items of the form `type[:name][:count] / … /
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

        """
        
        Object.__init__(self)
        self._count = count
        self._dtype = dtype
        self._data = data

    @command()
    def set_data(self, offset: int,
                       data : bytes):

        """Update buffer content at given offset with new data.
        
        Parameters:

         offset:
        
            Offset in bytes where to start update

         data:
        
            Content to update with.
        """
        self._data = data


