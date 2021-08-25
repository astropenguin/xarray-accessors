# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, ClassVar, Dict, List, Type, Union


# third-party packages
import xarray as xr


# type hints
Accessor = Type["AccessorBase"]
Function = Callable[..., Any]


# runtime classes
class AccessorBase:
    """Base class for DataArray and Dataset accessors."""

    _accessors: ClassVar[Dict[str, Accessor]]  #: Nested accessors
    _functions: ClassVar[Dict[str, Function]]  #: Data functions

    def __init__(self, data: Union[xr.DataArray, xr.Dataset]) -> None:
        """Initialize an instance by binding data."""
        self._accessed = data

    def __dir__(self) -> List[str]:
        """Return the union namespace of accessors and functions."""
        return list(set(self._accessors) | set(self._functions))

    def __getattr__(self, name: str):
        """Return an accessor class instance or a bound function."""
        if name in self._accessors:
            return self._accessors[name](self._accessed)

        if name in self._functions:
            function = self._functions[name]

            @wraps(function)
            def method(self: AccessorBase, *args: Any, **kwargs: Any) -> Any:
                return function(self._accessed, *args, **kwargs)

            return MethodType(method, self)

        cname = type(self).__name__
        raise AttributeError(f"{cname!r} object has no attribute {name!r}")
