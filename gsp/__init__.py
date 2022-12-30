# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""Graphic Server Protocol 

This is the reference implementation of the Graphic Server Protocol (GSP) that
It allows to issue commands, parse them and build corresponding objects.
"""
import itertools
from gsp.core.object import Object, OID
from gsp.core.command import Command, command, CID


def mode(mode="server", reset=True, record=None, output=None):
    "Set protocol in specified mode (server or client)."

    if reset:
        Object.objects = {}
        OID.counter = itertools.count()
        Command.commands = []
        CID.counter = itertools.count()
            
    if mode == "client":
        Command.record = record if record is not None else True
        Command.output = output if output is not None else True
        Object.record = True
    else:
        Command.record = record if record is not None else False
        Command.output = output if output is not None else False
        Object.record = False

def objects():
    """ Dictionnary of objects that have been created. """
    
    return Object.objects

def commands():
    """ List of commands that have been issued. """
    
    return Command.commands

def process(command, globals=None, locals=None):
    """ Process a given command. """
    
    Command.execute(command, globals, locals)

