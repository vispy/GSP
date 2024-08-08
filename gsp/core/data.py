# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp import Object
from gsp.io.command import command, register

@register("NoneType", "list")
def NoneType_to_list(value):
    return list()

class Data(Object):
    """
    Data represents a block of raw binary data, with an optional
    structure. This data is built using the provided uri that may
    either point to an external file, or be a data URI that encodes
    the binary data directly in the JSON file. When an uri is
    provided, data will is fetched just in time and stored locally. If
    no uri has been provided, an empty data is created ex-nihilo, just
    in time. Data can be modified and is tracked for any modification.

    ```python exec="yes"
    from gsp.io import mkdocs
    mkdocs(print,
    '''
    from gsp.core.data import Data
    data = Data(nbytes=512)
    ''')
    ```
    """

    @command("core.Data")
    def __init__(self, uri : str = "",
                       nbytes : int = 0,
                       struct : list = None):
        """
        Data represents a block of raw binary data, with an
        optional structure.

        Parameters
        ----------
        uri :
            Uniform Resource Identifier from where to fetch data.
        nbytes :
            Number of bytes in the data. This is used to create data
            ex-nihilo if no uri has been provided. If a struct is
            provided, the nbytes is discarded in favor of the size of
            the provided structure.
        struct :
            Description of the internal structure of the data as a
            list of (count, dtype) items.

            with `dtype` one of:

            Type       | Data type      | Signed                    | Bits
            ---------- | -------------- | ------------------------- | ----
            np.int8    | signed byte    | signed, two's complement  | 8
            np.uint8   | unsigned byte  | unsigned                  | 8
            np.int16   | signed short   | signed, two's complement  | 16
            np.uint16  | unsigned short | unsigned                  | 16
            np.int32   | signed int     | signed                    | 32
            np.uint32  | unsigned int   | unsigned                  | 32
            np.int64   | signed long    | signed                    | 64
            np.uint64  | unsigned long  | unsigned                  | 64
            np.float32 | float          | signed                    | 32
            np.float64 | double         | signed                    | 64
        """
        Object.__init__(self)


    @command()
    def set_data(self,
                 offset : int = 0,
                 data : bytes = None):

        """Update data content at given offset with new data.

        Parameters
        ----------
        offset:
            Offset in bytes where to start update
        data:
            Content to update with.
        """

        buffer = np.asanyarray(self).view(np.ubyte)
        buffer[offset:offset+len(data)] = np.frombuffer(data, np.ubyte)
