# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
from gsp.object import Object
from gsp.io.command import command, register

# This allows to specify an empty list as default arg
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

    ```bash
    python docs/snippets/Data_init.py
    ```

    """

    @command("core.Data")
    def __init__(self, uri : str = "",
                       nbytes : int = 0,
                       dtype : list = None):
        """
        Data represents a block of raw binary data, with an
        optional structure.

        Parameters
        ----------
        uri :
            Uniform Resource Identifier from where to fetch data.
        nbytes :
            Number of bytes in the data. This is used to create data
            ex-nihilo if no uri has been provided. If a dtype is
            provided, the nbytes is discarded in favor of the size of
            the provided structure.
        dtype :
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
                 offset : int,
                 data : bytes):

        """Update data content at given offset with new data.

        ```bash
        python docs/snippets/Data_set_data.py
        ```

        Parameters
        ----------
        offset:
            Offset in bytes where to start update
        data:
            Content to update with.
        """
        pass
