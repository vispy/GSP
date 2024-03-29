# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""Graphic Server Protocol 

This is the reference implementation of the Graphic Server Protocol (GSP) that
It allows to issue commands, parse them and build corresponding objects.
"""

from . canvas import Canvas
from . viewport import Viewport
from . buffer import Buffer
from . color import Color
from . size import Size
