# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
import pytest
from gsp import transform

def test_transform_add():
    """ Check if add works properly """

    t1, t2 = transform.Transform(), transform.Transform()
    t3 = t1 + t2
    assert(t3.left.base.id == t1.id)
    assert(t3.right.base.id == t2.id)

def test_transform_sub():
    """ Check if sub works properly """

    t1, t2 = transform.Transform(), transform.Transform()
    t3 = t1 - t2
    assert(t3.left.base.id == t1.id)
    assert(t3.right.base.id == t2.id)

def test_transform_mul():
    """ Check if mul works properly """

    t1, t2 = transform.Transform(), transform.Transform()
    t3 = t1 * t2
    assert(t3.left.base.id == t1.id)
    assert(t3.right.base.id == t2.id)

def test_transform_div():
    """ Check if div works properly """

    t1, t2 = transform.Transform(), transform.Transform()
    t3 = t1 / t2
    assert(t3.left.base.id == t1.id)
    assert(t3.right.base.id == t2.id)

def test_transform_call():

    t1, t2 = transform.Transform(), transform.Transform()
    t3 = t1(t2)
    assert(t3.base.id == t1.id)
    assert(t3.next.base.id == t2.base.id)

def test_transform_accessor():

    assert(transform.X())
    assert(transform.Y())
    assert(transform.Z())
    assert(transform.W())

    assert(transform.R())
    assert(transform.G())
    assert(transform.B())
    assert(transform.A())

def test_transform_measure():

    assert(transform.Pixel())
    assert(transform.Point())
    assert(transform.Inch())
    assert(transform.Millimeter())
    assert(transform.Centimeter())
    assert(transform.Meter())
    assert(transform.Kilometer())
