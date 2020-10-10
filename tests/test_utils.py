# dependencies
from pytest import raises
from xarray_accessors.utils import (
    get_nested_attr,
    set_nested_attr,
    del_nested_attr,
    has_nested_attr,
)


# test datasets
class Data:
    pass


data = Data()
data.a = Data()
data.a.b = Data()
data.a.b.c = "data"


# test functions
def test_get_nested_attr():
    names = ("a", "b", "c")
    expected = data.a.b.c
    assert get_nested_attr(data, names) == expected


def test_set_nested_attr():
    names = ("a", "b", "d")
    expected = "data"
    set_nested_attr(data, names, expected)
    assert data.a.b.d == expected


def test_del_nested_attr():
    names = ("a", "b", "e")
    data.a.b.e = "data"
    del_nested_attr(data, names)

    with raises(AttributeError):
        data.a.b.e


def test_has_nested_attr():
    names = ("a", "b", "c")
    assert has_nested_attr(data, names)
