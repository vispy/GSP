# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

from distutils.core import setup

setup( name='GSP',
       version="alpha",
       description="Graphic Server Protocol",
       author="Nicolas P. Rougier",
       author_email="nicolas.rougier@inria.fr",
       packages=["gsp", "gsp.core"] )
