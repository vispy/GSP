# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause

import itertools
import inspect, linecache
from gsp.object import OID, Object
from gsp.io import yaml, json, ansi
from gsp.io.command import CID, Command, CommandQueue


# def mkdocs(print, script=""):

#     from gsp.io import yaml, json, ansi
#     from gsp.io import CommandQueue

#     CommandQueue.get_default().empty()
#     Object.objects = {}
#     CID.counter = itertools.count()
#     OID.counter = itertools.count()
#     exec(script)
#     yaml_dump = yaml.dump()
#     json_dump = json.dump()
#     ansi_dump = ansi.dump()

#     print('??? example "Example"')

#     # Python script
#     print('    === "PYTHON"')
#     print('        ``` python linenums="1" ')
#     for line in script.split("\n"):
#         print("        %s" % line)
#     print('        ```\n')

#     # TEXT version
#     print('    === "TEXT"')
#     print('        ``` ansi linenums="1"')
#     for line in ansi_dump.split("\n"):
#         print("        %s" % line)
#     print('        ```\n')

#     # YAML version
#     print('    === "YAML"')
#     print('        ``` yaml linenums="1"')
#     for line in yaml_dump.split("\n"):
#         print("        %s" % line)
#     print('        ```\n')

#     # JSON version
#     print('    === "JSON"')
#     print('        ``` json linenums="1"')
#     for line in json_dump.split("\n"):
#         print("        %s" % line)
#     print('        ```\n')

class mkdocs():

    def __init__(self, title="Example",
                       formats = ["ansi", "yaml", "json"]):
        self.title = title
        self.formats = formats

    def __enter__(self):
        CommandQueue.get_default().empty()
        Object.objects = {}
        CID.counter = itertools.count()
        OID.counter = itertools.count()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # See https://stackoverflow.com/questions/36815410/
        #  -> is-there-any-way-to-get-source-code-inside-context-manager-as-string
        cf = inspect.currentframe().f_back
        filename = cf.f_code.co_filename
        line = cf.f_lineno
        lines = []
        indent = 0
        i = 1
        while True:
            next_line = linecache.getline(filename, line + i)
            next_line_indent = len(next_line) - len(next_line.lstrip())
            if indent == 0:
                indent = next_line_indent
            elif (next_line_indent < indent and len(next_line.strip()) > 0) or next_line == "":
                break
            if next_line == "\n": # preserve newlines
                lines.append(next_line)
            else:
                lines.append(next_line[indent:])
            i += 1
        self.code = lines
        self.dump()

    def dump(self):

        print(f'??? example "{self.title}"')

        # Python script
        print('    === "PYTHON"')
        print('        ``` python linenums="1" ')
        for line in self.code:
            print("        %s" % line, end="")
        print('        ```\n')

        # Text (ansi) version
        if "ansi" in self.formats:
            ansi_dump = ansi.dump()
            print('    === "TEXT"')
            print('        ``` ansi linenums="1"')
            for line in ansi_dump.split("\n"):
                print("        %s" % line)
            print('        ```\n')

        # YAML version
        if "yaml" in self.formats:
            yaml_dump = yaml.dump()
            print('    === "YAML"')
            print('        ``` yaml linenums="1"')
            for line in yaml_dump.split("\n"):
                print("        %s" % line)
            print('        ```\n')

        # JSON version
        if "json" in self.formats:
            json_dump = json.dump()
            print('    === "JSON"')
            print('        ``` json linenums="1"')
            for line in json_dump.split("\n"):
                print("        %s" % line)
            print('        ```\n')
