# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — reference implementation
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from __future__ import annotations
from typing import Union
from gsp.backend.reference.core import Buffer
from gsp.backend.reference.object import Object
from gsp.backend.reference.command import command
from gsp.backend.reference.transform import Transform


class Operator(Transform):

    @command("transform.Operator")
    def __init__(self, operator : str,
                       left : Union[Transform,Buffer] = None,
                       right : Union[Transform,Buffer] = None):
        """Arithmetic operator to compose two transforms

        Parameters:

          operator:

            Operator description, one of: `+` (addition),
            `-` (subtraction), `/` (division), `*` (mutliplication),
        
          left:

            Left operand (transform or buffer)

          right:

            Right operand (transform or buffer)
        """

        Transform.__init__(self, __no_command__ = True)
        self._operator = operator
        self._left = None
        self._right = None
        
        if isinstance(left, Transform):
            if left.bound:
                raise ValueError("Left transform is bound to a buffer")
            self._left = left.copy()
        elif isinstance(left, Buffer):
            self._left = left

        if isinstance(right, Transform):
            if right.bound:
                raise ValueError("Right transform is bound to a buffer")
            self._right = right.copy()
        elif isinstance(right, Buffer):
            self._right = right
            
    @property
    def operator(self):
        """Operator"""
        
        return self._operator

    @property
    def left(self):
        """Left operand"""
        
        return self._left

    @property
    def right(self):
        """Right operand"""
        
        return self._right
            
    @command()
    def set_operator(self, operator : str):
        """Set operator

        Parameters:

          operator:

            Operator
        """

        self._operator = operator

    @command()
    def set_left(self, left : Union[Transform,Buffer] = None):
        """Set left operand

        Parameters:

          left:

            Left operand (transform or buffer)
        """

        self._left = left

    @command()
    def set_right(self, right : Union[Transform,Buffer] = None):
        """
        Set left operand

        Parameters:

          right:

            Righ operand (transform or buffer)
        """
        
        self._right = right

        
    def copy(self):
        """Shallow copy"""
        
        transform = super().copy()
        transform.set_operator(self._operator)
        
        if isinstance(self._left, Transform):
            transform.set_left(self._left.copy())
        else:
            transform.set_left(self._left)

        if isinstance(self._right, Transform):
            transform.set_right(self._right.copy())
        else:
            transform.set_left(self._left)
            
        return transform
    
    
class Add(Operator):

    @command("transform.Add")
    def __init__(self, left = None, right = None):
        "Arithmetic addition of left and right"
        
        Operator.__init__(self, "+", left, right, __no_command__ = True)
        
class Sub(Operator):

    @command("transform.Sub")
    def __init__(self, left = None, right = None):
        "Arithmetic subtraction of left and right"

        Operator.__init__(self, "-", left, right, __no_command__ = True)

class Mul(Operator):

    @command("transform.Mul")
    def __init__(self, left = None, right = None):
        "Arithmetic multiplication of left and right"
                
        Operator.__init__(self, "*", left, right, __no_command__ = True)

class Div(Operator):

    @command("transform.Div")
    def __init__(self, left = None, right = None):
        "Arithmetic division of left and right"

        Operator.__init__(self, "/", left, right, __no_command__ = True)


    
    # def __repr__(self):
    #     if self._base:
    #         s = f"{self.__class__.__name__} (id={self.id}[base={self.base.id}])"
    #     else:
    #         s = f"{self.__class__.__name__} (id={self.id})"
            
    #     if self._next:
    #         s += "(%s)" % repr(self._next)
    #     elif self._buffer:
    #         s += "(%s)" % repr(self._buffer)
    #     return s
