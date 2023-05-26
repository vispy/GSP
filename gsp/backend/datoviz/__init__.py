# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""Graphic Server Protocol Datoviz implementation.
"""

from . app import default_app
from . canvas import Canvas
from . viewport import Viewport
from . datatype import Datatype
from . buffer import Buffer
from . pixels import Pixels


def run():
    default_app().run()
