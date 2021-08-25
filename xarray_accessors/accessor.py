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
class AccessorMeta(type):
    """Metaclass for DataArray and Dataset accessors."""

    _accessors: Dict[str, Accessor]  #: Nested accessors.
    _functions: Dict[str, Function]  #: Data functions.

    def __init__(cls, *args: Any, **kwargs: Any) -> None:
        """Initialize a class by creating initial attributes."""
        cls._accessors = {}
        cls._functions = {}

    def __dir__(cls) -> List[str]:
        """Return the union namespace of accessors and functions."""
        return list(set(cls._accessors) | set(cls._functions))

    def __getattr__(cls, name: str) -> Union[Accessor, Function]:
        """Return an accessor class or a function."""
        if name not in cls._accessors:
            cls._accessors[name] = type(name, (AccessorBase,), {})

        if name in cls._accessors:
            return cls._accessors[name]

        if name in cls._functions:
            return cls._functions[name]

        cname = cls.__name__
        raise AttributeError(f"Type object {cname!r} has no attribute {name!r}.")


class AccessorBase(metaclass=AccessorMeta):
    """Base class for DataArray and Dataset accessors."""

    _accessors: ClassVar[Dict[str, Accessor]]  #: Nested accessors.
    _functions: ClassVar[Dict[str, Function]]  #: Data functions.

    def __init__(self, data: Union[xr.DataArray, xr.Dataset]) -> None:
        """Initialize an instance by binding data."""
        self._accessed = data

    def __dir__(self) -> List[str]:
        """Return the union namespace of accessors and functions."""
        return list(set(self._accessors) | set(self._functions))

    def __getattr__(self, name: str) -> Union["AccessorBase", MethodType]:
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
        raise AttributeError(f"{cname!r} object has no attribute {name!r}.")
