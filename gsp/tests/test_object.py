# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2022 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import gsp

def test_object_id():
    "Test if object get a unique id"

    gsp.mode("client", reset=True)
    object = gsp.core.Object()
    assert object.id == 1

def test_object_record():
    "Test if object get a unique id"

    gsp.mode("client", reset=True, record=True)
    object = gsp.core.Object()
    assert len(gsp.core.Object.objects) == 1

def test_object_change_id():
    "Test if object get a unique id"

    gsp.mode("client", reset=True, record=True)
    object = gsp.core.Object()
    object.id = 123
    assert len(gsp.core.Object.objects) == 1
    assert 123 in gsp.core.Object.objects.keys()
    assert gsp.core.Object.objects[123] == object

