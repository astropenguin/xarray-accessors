import xarray_accessors


def test_author():
    assert xarray_accessors.__author__ == "Akio Taniguchi"


def test_version():
    assert xarray_accessors.__version__ == "0.1.0"
