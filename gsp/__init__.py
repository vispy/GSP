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

def use(name):
    global mode
    
    if name == "text":
        mode = "client/text"
        from gsp.backend.text import (core, visual, transform)
    elif name == "yaml":
        mode = "client/yaml"
        from gsp.backend.yaml import (core, visual, transform)
    elif name == "json":
        mode = "client/json"
        from gsp.backend.json import (core, visual, transform)
    elif name == "matplotlib":
        mode = "matplotlib"
        from gsp.backend.matplotlib import (core, visual, transform)
    elif name == "matplotlib/iterm":
        mode = "matplotlib/iterm"
        import matplotlib as mpl; mpl.use("module://imgcat")
        from gsp.backend.matplotlib import (core, visual, transform)
    elif name == "datoviz":
        mode = "datoviz"
        from gsp.backend.datoviz import (core, visual, transform)
    else:
        raise ValueError(f"Unknown backend ({name})")

    import inspect

    gsp.core = core
    inspect.stack()[1][0].f_globals["core"] = core

    gsp.tranform = transform
    inspect.stack()[1][0].f_globals["transform"] = transform

    gsp.visual = visual
    inspect.stack()[1][0].f_globals["visual"] = visual
    
    


