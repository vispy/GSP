# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from typing import Union
from typeguard import typechecked
from gsp import command


"""
"""

class Datatype(Object):
    
    # Convenience method, not part of the protocol
    @classmethod
    def from_numpy(cls, dtype):
        """Convert a numpy type into a string representation"""

        datatype = ""
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
                datatype += "%s:%s:%d;" % (itype,iname,isize)
        elif dtype.startswith("("):
            itype, isize = eval(dtype)
            isize = np.prod(isize)
            datatype += "%s::%d;" % (itype,isize)
        else:
            datatype += "%s;" % (dtype)
        return datatype

    # Convenience method, not part of the protocol
    @classmethod
    def to_numpy(cls, datatype):
        dtype = []
        datatype = datatype.replace(" ", "")
        for item in datatype.split(";"):
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
    
    @typechecked
    @command("")
    def __init__(self, type : str):
        """Dataype describes the structure of a chunk of memory.
        
        === "Python"

            ```Pycon
            >>> vec2 = Datatype("f:x / f:y")  # 8 bytes total
            >>> Command.commands[-1].to_json()
            ```

        === "JSON-RPC"

            ```json
            { 
                "jsonrpc": "2.0",
                "id": 1,
                "timestamp": 0,
                "method": "Datatype",
	        "params": {
                    "type" : f:x / f:y,
                }
	    }
            ```

        **Protocol**{: .protocol}
        
        | Request type | # Parameters | Asynchronous     | Error handling   |
        | ------------ | ------------ | ---------------- | ---------------- |
        | `CREATE`     | 1            | :material-check: | :material-check: |

        Parameters:
        
          type:
    
            Description of the type (as a `/` separated list of atomic items)
            **→** `type` must fit datatype description.

        
        The description of the type is a `/` separated list of atomic items of
        the form `alias:[name]:[count] / … / alias:[name]:[count]` where `name`
        is a valid identifier, count is a strictly positive integer and `alias`
        is one of:
        
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


        A type can be matched against a Posix regular expression (multiline):

        ```python
        '''(?:(?P<type>[?bsiBSIefdY])
             :(?P<name>[[:alpha:]]*)
             :(?P<count>[[:digit:]]+))+
           (\s*\/\s*)?'''
        ```
        
        or a Python regular expression (multiline):

        ```python
        '''((?P<type>[?bsiBSIefdY])
           :(?P<name>[\w\d]*)
           :(?P<count>\d+))+
           (\s*/\s*)?'''
        ```

        **Errors**{: .errors}

          - `INVALID_REQUEST` : Request is malformed
          - `INVALID_METHOD`  : Method does not exist or is not available.
          - `INVALID_PARAMS`  : A parameter is missing or has an illegal value

        **Future**{: .future}

        No dicussion at the moment.

        **Examples**{.examples}

        ```python
        vec2 = Datatype("f:x / f:y")             #   8 bytes total
        vec3 = Datatype("f:x / f:y / f:z")       #  12 bytes total
        rgba = Datatype("f:R / f:G / f:B / f:A") #  16 bytes total
        RGBA = Datatype("B:R / B:G / B:B / B:A") #   4 bytes total
        mat4 = Datatype("f::16")                 # 512 bytes total
        ```

        """
        
        # ((?:(?P<type>[?bsiBSIefdY]):(?P<name>[[:alpha:]]*):(?P<count>[[:digit:]]+))+)(\s*\/\s*)?
        # "((?:[\?bsiBSIefdY][124]:[[:alpha:]]+:[[:digit:]])+);?"


        Object.__init__(self)
        self.type = type

    def __repr__(self):
        """String representation of the type."""
        
        return f"Type [id={self.id}]: {self.type}"
