# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — yaml backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import yaml
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import Command, Converter

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

    # Convert parameters if necessary
    parameters = {}
    for key,value in self.parameters.items():
        if isinstance(value, Converter):
            parameters[key] = value()
            if isinstance(parameters[key], Object):
                parameters[key] = parameters[key].id
        else:
            parameters[key] = value
            
    # Check which method has been called
    if (self.methodname is None or not len(self.methodname)):
        method = self.classname
    elif "." in self.methodname:
        method = self.methodname
    else:
        method = "%s/%s" % (self.classname, self.methodname)
    
    data = [ { "method" : method,
               "id" : self.id,
               "timestamp" : self.timestamp,
               "parameters" : parameters } ]
    print(yaml.dump(data, default_flow_style=None, sort_keys=False))

Command.dump = yaml_dump

import gsp.backend.reference.core as core
import gsp.backend.reference.visual as visual
import gsp.backend.reference.transform as transform
from gsp.backend.reference import (objects, commands, process)

import gsp
gsp.mode = "client"
gsp.core = core
gsp.visual = visual
gsp.tranform = transform
