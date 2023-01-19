# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — yaml backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import yaml
import gsp.backend.reference.core as core
import gsp.backend.reference.visual as visual
import gsp.backend.reference.transform as transform

from gsp.backend.reference.object import OID as _OID
from gsp.backend.reference.command import CID as _CID
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import Command, command
from gsp.backend.reference import (mode, objects, commands, process)


class OID(yaml.YAMLObject, _OID):

    # YAML tag (class attribute)
    yaml_tag = "!OID"

    # YAML loader (class method)
    yaml_loader = yaml.SafeLoader
    
    def __init__(self, id : int = None):
        _object._OID.__init__(self, id)

    @classmethod
    def to_yaml(cls, representer, node):
        """ Convert OID to a YAML node """
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.id}'.format(node))

    @classmethod
    def from_yaml(cls, loader, node):
        """ Convert a YAML node to OID. """
        return cls(node.value)


class CID(yaml.YAMLObject, _CID):

    # YAML tag (class attribute)
    yaml_tag = "!CID"

    # YAML loader (class method)
    yaml_loader = yaml.SafeLoader

    def __init__(self, id : int = None):
        _CID.__init__(self, id)
        
    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.id}'.format(node))

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(node.value)


def yaml_load(self, command):
    command = yaml.safe_load(data)[0]
    self.id = command["id"]
    try:
        self.classname, self.methodname = command["method"].split("/")
    except ValueError:
        self.classname, self.methodname = command["method"], None
    self.parameters = command["parameters"]
    self.timestamp = command["timestamp"]

Command.load = yaml_load
    

def yaml_dump(self):
    if self.methodname:
        method = "%s/%s" % (self.classname, self.methodname)
    else:
        method = self.classname
    data = [ { "method" : method,
               "id" : self.id,
               "timestamp" : self.timestamp,
               "parameters" : self.parameters } ]
    return yaml.dump(data, default_flow_style=None, sort_keys=False)

Command.dump = yaml_dump

