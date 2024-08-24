# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
from gsp.core import Buffer
from . transform import Transform
from gsp.io.command import command

class Operator(Transform):

    @command("transform.Operator")
    def __init__(self, operator : str,
                       left : Transform | Buffer | int | float = None,
                       right : Transform | Buffer | int | float = None):
        """Arithmetic operator to compose two transforms

        Parameters
        ----------
        operator :
            Operator description, one of: `+` (addition),
            `-` (subtraction), `/` (division), `*` (multiplication),
        left :
            Left operand (transform or buffer)
        right :
            Right operand (transform or buffer)
        """

        Transform.__init__(self, __no_command__ = True)
        self._operator = operator
        self._next = None
        self._left = None
        self._right = None

        if isinstance(left, Transform):
            self._left = left.copy()
        else:
            self._left = left

        if isinstance(right, Transform):
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

    @command()
    def set_operator(self,
                     operator : str):
        """Set operator

        Parameters
        ----------
        operator:
            Operator
        """

        self._operator = operator

    @command()
    def set_left(self,
                 left : Transform | Buffer | float | int):
        """Set left operand

        Parameters
        ----------
        left:
            Left operand (transform or buffer)
        """

        self._left = left

    @command()
    def set_right(self,
                  right : Transform | Buffer | float | int):
        """
        Set right operand

        Parameters
        ----------
        right:
            Righ operand (transform or buffer)
        """

        self._right = right

    def copy(self):
        """
        Shallow copy
        """

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

    def evaluate(self, variables):

        if isinstance(self._left, Transform):
            left = self._left.evaluate(variables)
        else:
            left = self._left

        if isinstance(self._right, Transform):
            right = self._right.evaluate(variables)
        else:
            right = self._right

        return left, right

    def __repr__(self):

        if self._base:
            s = f"{self.__class__.__name__} (id={self.id}[base={self.base.id}], "
        else:
            s = f"{self.__class__.__name__} (id={self.id}, "

        s += "(left=%s, right=%s)" % (repr(self._left), repr(self._right))

        return s

class Add(Operator):

    @command("transform.Add")
    def __init__(self, left : Transform | Buffer | float | int = None,
                       right : Transform | Buffer | float | int = None):
        """
        Arithmetic addition of left and right
        """

        Operator.__init__(self, "+", left, right,
                          __no_command__ = True)

    def evaluate(self, variables):
        left, right = Operator.evaluate(self, variables)
        return left + right

class Sub(Operator):

    @command("transform.Sub")
    def __init__(self, left : Transform | Buffer | float | int = None,
                       right : Transform | Buffer | float | int = None):
        """
        Arithmetic subtraction of left and right
        """

        Operator.__init__(self, "-", left, right, __no_command__ = True)

    def evaluate(self, variables):
        left, right = Operator.evaluate(self, variables)
        return left - right

class Mul(Operator):

    @command("transform.Mul")
    def __init__(self, left : Transform | Buffer | float | int = None,
                       right : Transform | Buffer | float | int = None):
        """
        Arithmetic multiplication of left and right
        """
        Operator.__init__(self, "*", left, right,
                          __no_command__ = True)

    def evaluate(self, variables):
        left, right = Operator.evaluate(self, variables)
        return left * right

class Div(Operator):

    @command("transform.Div")
    def __init__(self,left : Transform | Buffer | float | int = None,
                      right : Transform | Buffer | float | int = None):
        """
        Arithmetic division of left and right
        """

        Operator.__init__(self, "/", left, right,
                          __no_command__ = True)

    def evaluate(self, variables):
        left, right = Operator.evaluate(self, variables)
        return left / right
