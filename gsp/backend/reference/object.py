# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
"""
The role of the Object class is to facilitate the writing of the reference
implementation. It is *not* part of the protocol.
"""
import itertools

class OID:
    """ Object unique identifier

    The object unique identifier (that is technically a simple integer) is used
    to uniquely identify objects. When a Command is issued, objects' id are used
    inside parameters in place of the actual object. It is then the
    responsability of the receiver to resolve an id in order to find the
    corresponding object.

    !!! Note
    
        Any implementation of the protocol needs to have an equivalent system
        in order to guarantee the identification of any object.

    Attributes:

     counter (itertools.count):
    
       Unique identifier counter  (class attribute)

     id (int):
    
       Identifier unique value
    """

    # Identifier counter
    counter = itertools.count()

    # Unique identifier
    id = None
    
    def __init__(self, id = None):
        """ Creates a new identifier unless id is provided. """
                
        if id is None:
            self.id = 1 + next(OID.counter)
        else:
            self.id = int(id)

    def __eq__(self, other):
        if isinstance(other, (int,)):
            return self.id == other
        else:
            return self.id == other.id

    def __int__(self):
        return self.id

    def __hash__(self):
        return self.id

    def __repr__(self):
        return "%d" % self.id

    def to_json(self):
        return self.id

    
class Object:
    """Generic object with a unique ID

    Object is the base class that every other class must inherit in order to
    guarantee the unique identification of objects.

    Attributes:

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
    
    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        keys = list(vars(self).keys())
        keys.remove("_id")
        for key in keys:
            if getattr(self, key) != getattr(other, key):
                return False
        return True
