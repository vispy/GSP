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
       packages=["gsp",
                 "gsp.backend",
                 
                 "gsp.backend.text",
                 
                 "gsp.backend.yaml",
                 
                 "gsp.backend.json",
                 
                 "gsp.backend.reference",
                 "gsp.backend.reference.core",
                 "gsp.backend.reference.visual",
                 "gsp.backend.reference.transform",
                 
                 "gsp.backend.matplotlib",
                 "gsp.backend.matplotlib.core",
                 "gsp.backend.matplotlib.visual",
                 "gsp.backend.matplotlib.transform",
                 ] )
