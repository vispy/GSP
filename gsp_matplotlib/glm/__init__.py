# -----------------------------------------------------------------------------
# Numpy/GL Mathematics
# Copyright 2023 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
GLM offers a set of objects and functions for 3D geometry inspired by the OpenGL API and the GLSL language.
"""

import array
from . glm import *
from . vlist import *
from . vec234 import *
from . mat234 import *
from . ndarray.vectors import vec2_t, vec3_t, vec4_t
from . shapes import sphere, cube
from . trackball import Trackball
