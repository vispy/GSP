# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

from . mkdocs import mkdocs
from . command import record, command
from . convert import convert, register, unregister
from . command import CID, Command, CommandQueue


# class save:
#     """
#     Context manager to save a session.
#     """

#     def __init__(self, filename, format=None):
#         import pathlib

#         self.filename = filename
#         self.format = format or pathlib.Path(filename).suffix[1:]
#         self.queue = queue()
#         return self

#     def __enter__(self):
#         from gsp.io import json

#         if self.format in ["json"]:
#             json.save(self.filename, self.queue)
#         else:
#             raise ValueError(f"Unknown format ({format})")

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
