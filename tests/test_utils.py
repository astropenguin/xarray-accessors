# third-party dependencies
from pytest import raises


# submodules
from xarray_accessors.utils import (
    del_nested_attr,
    get_nested_attr,
    has_nested_attr,
    set_nested_attr,
)


# test datasets
class Data:
    pass


data = Data()
data.a = Data()  # type: ignore
data.a.b = Data()  # type: ignore
data.a.b.c = "data"  # type: ignore


# test functions
def test_del_nested_attr() -> None:
    names = ("a", "b", "e")
    data.a.b.e = "data"  # type: ignore
    del_nested_attr(data, names)

    with raises(AttributeError):
        data.a.b.e  # type: ignore


def test_get_nested_attr() -> None:
    names = ("a", "b", "c")
    expected = data.a.b.c  # type: ignore
    assert get_nested_attr(data, names) == expected


def test_has_nested_attr() -> None:
    names = ("a", "b", "c")
    assert has_nested_attr(data, names)


def test_set_nested_attr() -> None:
    names = ("a", "b", "d")
    expected = "data"
    set_nested_attr(data, names, expected)
    assert data.a.b.d == expected  # type: ignore
