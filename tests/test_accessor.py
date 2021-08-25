# third-party packages
import xarray as xr


# submodule
from xarray_accessors.accessor import AccessorBase


# accessors
class Accessor(AccessorBase):
    pass


def func(dataarray: xr.DataArray) -> int:
    return 1


Accessor.func = func
Accessor.sub.subsub.func = func  # type: ignore


# test functions
def test_accessor_attrs() -> None:
    assert Accessor.func is func
    assert Accessor.sub.subsub.func is func  # type: ignore


def test_accessor_call() -> None:
    assert Accessor(xr.DataArray()).func() == 1  # type: ignore
    assert Accessor(xr.DataArray()).sub.subsub.func() == 1  # type: ignore
