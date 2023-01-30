# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — json backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import json
from base64 import b64encode
from gsp.backend.reference.command import Command, command

def json_default(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    elif isinstance(obj, bytes):
        return b64encode(obj).decode()
        
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def json_dump(self):

    # Convert parameters if necessary
    parameters = {}
    for key,value in self.parameters.items():
        if callable(value):
            parameters[key] = value()
        else:
            parameters[key] = value

    # Check which method has been called
    if (self.methodname is None or not len(self.methodname)):
        method = self.classname
    elif "." in self.methodname:
        method = self.methodname
    else:
        method = "%s/%s" % (self.classname, self.methodname)
        
    payload = { "jsonrpc": "2.0",
                "id" : int(self.id),
                "timestamp" : self.timestamp,
                "method" : method,
                "parameters" : parameters }
    return json.dumps(payload, default=json_default)
    
Command.dump = json_dump

def json_load(self, payload):
    self.id = payload["id"]
    try:
        self.classname, self.methodname = payload["method"].split("/")
    except ValueError:
        self.classname, self.methodname = payload["method"], None
    self.parameters = payload["parameters"]
    self.timestamp = payload["timestamp"]

Command.load = json_load

import gsp.backend.reference.core as core
import gsp.backend.reference.visual as visual
import gsp.backend.reference.transform as transform
from gsp.backend.reference import (objects, commands, process)
mode = "client"
