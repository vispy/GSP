# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from __future__ import annotations # Solve circular references with typing

import numpy as np
from gsp import Object
from . data import Data
from gsp.io.command import command, register


class Buffer(Object):

    """
    Buffer represents a structured view on some Data or
    Buffer. Buffer can be a partial or whole view on the underlying
    source.


    ```python exec="yes"
    from gsp.io import mkdocs
    mkdocs(print,
    '''
    from gsp.core.buffer import Buffer
    buffer = Buffer(128, [("color", 4, "u1")])
    ''')
    ```
    """

    @command("core.Buffer")
    def __init__(self, count : int,
                       dtype : list):
        """
        Create a new Buffer.

        Parameters
        ----------
        count :
            Number of item
        dtype : str
            Type of the item
        """
        Object.__init__(self)

    @command()
    def set_data(self, offset : int,
                       data : bytes):

        """Update buffer content at given offset with new data.

        ```python exec="yes"
        from gsp.io import mkdocs
        mkdocs(print,
        '''
        import numpy as np
        from gsp.core.buffer import Buffer
        buffer = Buffer(2, ["f4"])
        buffer.set_data(0, bytes(2*np.float32(0).nbytes))
        ''')
        ```

        Parameters
        ----------
        offset :
            Offset in bytes where to start update
        data :
            Content to update with.
        """
        pass
