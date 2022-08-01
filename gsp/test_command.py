# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp

def test_command_cid():
    "Test if command get a unique id"

    gsp.mode("client", reset=True)
    command = gsp.Command()
    assert command.id == 1

def test_command_decorator():
    "Test if a call is properly recorded into command"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b): pass
    Test().call(1,2)
    command = gsp.Command.commands[0]
    assert command.classname == "Test"
    assert command.methodname == "call"
    assert command.parameters == {"id" : 1, "a": 1, "b":2}

def test_command_decorator_default_arg():
    "Test if default argument values are recorded"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b, c=3): pass
    Test().call(1,2)
    command = gsp.Command.commands[0]
    assert command.parameters == {"id" : 1, "a": 1, "b": 2, "c": 3}

def test_command_decorator_named_arg():
    "Test if named arguments are handled properly"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b, c=3): pass
    Test().call(c=3,b=2,a=1)
    command = gsp.Command.commands[0]
    assert command.parameters == {"id" : 1, "a": 1, "b": 2, "c": 3}

def test_command_no_record_global():
    "Test command no record (global)"
    
    gsp.mode("client", reset=True, record=False)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b): pass
    Test().call(1,2)
    assert len(gsp.Command.commands) == 0

def test_command_no_record_local():
    "Test command no record (local)"
        
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command(record=False)
        def call(self, a, b): pass
    Test().call(1,2)
    assert len(gsp.Command.commands) == 0

def test_command_record_global():
    "Test command no record (global)"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b): pass
    Test().call(1,2)
    assert len(gsp.Command.commands) == 1

def test_command_record_local():
    "Test command no record (local)"
        
    gsp.mode("client", reset=True, record=False)
    class Test(gsp.Object):
        id = 1
        @gsp.command(record=True)
        def call(self, a, b): pass
    Test().call(1,2)
    assert len(gsp.Command.commands) == 1


def test_command_yaml_dump_init():
    "Test yaml dump with creation"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command("")
        def __init__(self, a, b): pass
    Test(1,2)
    command = gsp.Command.commands[0]
    command.timestamp = 0
    assert command.yaml_dump() == (
        """- method: Test\n"""
        """  id: !CID '1'\n"""
        """  timestamp: 0\n"""
        """  parameters: {id: 1, a: 1, b: 2}\n""")

def test_command_yaml_dump_method():
    "Test yaml dump with a regular method"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command()
        def call(self, a, b): pass
    Test().call(1,2)
    command = gsp.Command.commands[0]
    command.timestamp = 0
    assert command.yaml_dump() == (
        """- method: Test/call\n"""
        """  id: !CID '1'\n"""
        """  timestamp: 0\n"""
        """  parameters: {id: 1, a: 1, b: 2}\n""")

def test_command_yaml_dump_method_rename():
    "Test yaml dump with a regular & renamed method"
    
    gsp.mode("client", reset=True, record=True)
    class Test(gsp.Object):
        id = 1
        @gsp.command("mycall")
        def call(self, a, b): pass
    Test().call(1,2)
    command = gsp.Command.commands[0]
    command.timestamp = 0
    assert command.yaml_dump() == (
        """- method: Test/mycall\n"""
        """  id: !CID '1'\n"""
        """  timestamp: 0\n"""
        """  parameters: {id: 1, a: 1, b: 2}\n""")

