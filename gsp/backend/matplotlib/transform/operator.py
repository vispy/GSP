# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP) — matplotlib backend
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from gsp.backend.matplotlib.core import Buffer
from gsp.backend.matplotlib.transform import Transform

class Operator(Transform):

    def __init__(self, operator, left = None, right = None):
        Transform.__init__(self)
        self._operator = operator
        self._next = None
        self._left = None
        self._right = None
        
        if isinstance(left, Transform):
            #if left.bound:
            #    raise ValueError("Left transform is bound to a buffer")
            self._left = left.copy()
        else:
            self._left = left

        if isinstance(right, Transform):
            #if right.bound:
            #    raise ValueError("Right transform is bound to a buffer")
            self._right = right.copy()
        else:
            self._right = right
            
    @property
    def operator(self):
        return self._operator

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def set_operator(self, operator : str):
        self._operator = operator

    def set_left(self, left = None):
        self._left = left

    def set_right(self, right = None):
        self._right = right
        
    def copy(self):
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

    def evaluate(self, buffers=None):

        if isinstance(self._left, Transform):
            left = self._left.evaluate(buffers)
        elif self._left.bound:
            left = self._left
        else:
            raise ValueError("Left operand is not bound")
            
        if isinstance(self._right, Transform):
            right = self._right.evaluate(buffers)
        elif self._right.bound:
            right = self._right
        else:
            raise ValueError("Right operand is not bound")

        return left, right


class Add(Operator):
    def __init__(self, left = None, right = None):
        Operator.__init__(self, "+", left, right)

    def evaluate(self, buffers=None):
        left, right = Operator.evaluate(self, buffers)
        return left + right
        
class Sub(Operator):
    def __init__(self, left = None, right = None):
        Operator.__init__(self, "-", left, right)

    def evaluate(self, buffers=None):
        left, right = Operator.evaluate(self, buffers)
        return left - right

class Mul(Operator):
    def __init__(self, left = None, right = None):
        Operator.__init__(self, "*", left, right)

    def evaluate(self, buffers=None):
        left, right = Operator.evaluate(self, buffers)
        return left * right

class Div(Operator):
    def __init__(self, left = None, right = None):
        Operator.__init__(self, "/", left, right)

    def evaluate(self, buffers=None):
        left, right = Operator.evaluate(self, buffers)
        return left / right
