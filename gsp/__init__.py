# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 VisPy Development team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp
from . log import log

mode = None
core = None
visual = None
transform = None

def use(backend):
    global mode

    mode = backend
    if backend == "client/text":
        from gsp.backend.text import (core, visual, transform)
    elif backend == "client/yaml":
        from gsp.backend.yaml import (core, visual, transform)
    elif backend == "client/json":
        from gsp.backend.json import (core, visual, transform)
    elif backend == "matplotlib":
        from gsp.backend.matplotlib import (core, visual, transform)
    elif backend == "datoviz":
        from gsp.backend.datoviz import (core, visual, transform)
    else:
        raise ValueError(f"Unknown backend ({backend})")

    import inspect

    gsp.core = core
    inspect.stack()[1][0].f_globals["core"] = core

    gsp.tranform = transform
    inspect.stack()[1][0].f_globals["transform"] = transform

    gsp.visual = visual
    inspect.stack()[1][0].f_globals["visual"] = visual
    
    


