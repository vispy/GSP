# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 VisPy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------

def use(name):
    class global_import:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            import inspect
            inner = inspect.currentframe()
            outer = inspect.getouterframes(inner)
            collector = inspect.getargvalues(outer[1][0]).locals
            globals().update(collector)
    
    if name == "text":
        with global_import():
            from gsp.backend.text import (core, visual, transform)
    elif name == "yaml":
        with global_import():
            from gsp.backend.yaml import (core, visual, transform)
    elif name == "json":
        with global_import():
            from gsp.backend.json import (core, visual, transform)
    elif name == "matplotlib":
        with global_import():
            from gsp.backend.matplotlib import (core, visual, transform)
    elif name == "terminal":
        with global_import():
            import matplotlib as mpl; mpl.use("module://imgcat")
            from gsp.backend.matplotlib import (core, visual, transform)
    elif name == "datoviz":
        with global_import():
            from gsp.backend.datoviz import (core, visual, transform)
