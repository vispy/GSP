# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Nicolas P. Rougier - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp

def test_object_id():
    "Test if object get a unique id"

    gsp.mode("client", reset=True)
    object = gsp.Object()
    assert object.id == 1

def test_object_record():
    "Test if object get a unique id"

    gsp.mode("client", reset=True, record=True)
    object = gsp.Object()
    assert len(gsp.Object.objects) == 1

def test_object_change_id():
    "Test if object get a unique id"

    gsp.mode("client", reset=True, record=True)
    object = gsp.Object()
    object.id = 123
    assert len(gsp.Object.objects) == 1
    assert 123 in gsp.Object.objects.keys()
    assert gsp.Object.objects[123] == object

