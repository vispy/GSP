# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""Graphic Server Protocol / Matplotlib backend

This is the matplotlib implementation of the Graphic Server Protocol
(GSP) that It allows to issue commands, parse them and build
corresponding objects.
"""

from . canvas import Canvas
from . buffer import Buffer
from . viewport import Viewport
from . datatype import Datatype



