# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

import itertools
from gsp.object import OID, Object
from . command import command
from . command import CID, Command, CommandQueue
from . convert import convert, register, unregister


def mkdocs(print, script=""):

    from gsp.io import yaml, json, ansi
    from gsp.io import CommandQueue

    CommandQueue.get_default().empty()
    Object.objects = {}
    CID.counter = itertools.count()
    OID.counter = itertools.count()
    exec(script)
    yaml_dump = yaml.dump()
    json_dump = json.dump()
    ansi_dump = ansi.dump()

    print('??? example "Example"')

    # Python script
    print('    === "PYTHON"')
    print('        ``` python linenums="1" ')
    for line in script.split("\n"):
        print("        %s" % line)
    print('        ```\n')

    # TEXT version
    print('    === "TEXT"')
    print('        ``` ansi linenums="1"')
    for line in ansi_dump.split("\n"):
        print("        %s" % line)
    print('        ```\n')

    # YAML version
    print('    === "YAML"')
    print('        ``` yaml linenums="1"')
    for line in yaml_dump.split("\n"):
        print("        %s" % line)
    print('        ```\n')

    # JSON version
    print('    === "JSON"')
    print('        ``` json linenums="1"')
    for line in json_dump.split("\n"):
        print("        %s" % line)
    print('        ```\n')
