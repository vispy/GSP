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
    data = Data(nbytes=512, struct=[("color", 1, "u4")])
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
            list of (`name` (str), `type` (str), `count` (int)) items.

            with:

            Type        | Kind                             |
            ----------- | -------------------------------- |
             `i[1,2,4]` | signed integer (8,16, 32 bits)   |
             `u[1,2,4]` | unsigned integer (8,16, 32 bits) |
             `f[2,4,8]` | float (16, 32, 64 bits)          |
             `m`        | timedelta (64 bits)              |
             `M`        | datetime (64 bits)               |
             `U[n]`     | unicode string (n x 16 bits)     |
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
