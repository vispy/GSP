# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
The role of the Object class is to facilitate the writing of the reference
implementation. It is *not* part of the protocol.
"""
import itertools

class OID(int):
    """
    Object unique identifier

    The object unique identifier (that is technically a simple integer) is used
    to uniquely identify objects. When a Command is issued, objects' id are used
    inside parameters in place of the actual object. It is then the
    responsability of the receiver to resolve an id in order to find the
    corresponding object.
    """

    # Identifier counter
    counter = itertools.count()

    def __new__(cls, oid=None):
        """
        Creates a new identifier unless oid is provided
        """

        if oid is None:
            oid = 1 + next(OID.counter)
        else:
            oid = int(oid)
        return super(OID, cls).__new__(cls, oid)



class Object:
    """Generic object with a unique ID

    Object is the base class that every other class must inherit in order to
    guarantee the unique identification of objects.

    Attributes
    ----------

    record (bool):

      Flag indicating whether to record object creation (class attribute)

    objects (dict):

      Dictionary of objects that have been created and recorded.

    id (OID):

      Object unique identifier
    """

    # Flag indicating if object creations are recorded
    record = True

    # Dictionnaty of created objects based on their id
    objects = {}

    def __init__(self):
        self._id = OID()
        if Object.record:
            Object.objects[self.id] = self

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newid):
        if self._id in Object.objects.keys():
            del Object.objects[self._id]
            Object.objects[newid] = self
        self._id = newid

    def __hash__(self):
        return self._id

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        keys = list(vars(self).keys())
        keys.remove("_id")
        for key in keys:
            if getattr(self, key) != getattr(other, key):
                return False
        return True
