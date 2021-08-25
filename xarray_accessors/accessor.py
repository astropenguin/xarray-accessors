# standard library
from functools import wraps
from inspect import isclass
from types import FunctionType, MethodType
from typing import Any, Callable, ClassVar, Dict, List, Type, Union


# third-party packages
import xarray as xr


# type hints
Accessor = Type["AccessorBase"]
Function = Callable[..., Any]


# constants
RESERVED_NAMES = (
    "_accessed",
    "_accessors",
    "_functions",
)


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
        if name in cls._accessors:
            return cls._accessors[name]

        if name in cls._functions:
            return cls._functions[name]

        setattr(cls, name, type(name, (AccessorBase,), {}))
        return cls._accessors[name]

    def __setattr__(cls, name: str, value: Union[Accessor, Function]) -> None:
        """Set an accessor class or a function to the instance."""
        if name in RESERVED_NAMES:
            return super().__setattr__(name, value)

        if isclass(value) and issubclass(value, AccessorBase):
            return cls._accessors.update({name: value})

        if isinstance(value, FunctionType):
            return cls._functions.update({name: value})

        raise TypeError("Value must be either an accessor or a function.")


class AccessorBase(metaclass=AccessorMeta):
    """Base class for DataArray and Dataset accessors."""

    _accessed: Union[xr.DataArray, xr.Dataset]  #: Accessed data.
    _accessors: ClassVar[Dict[str, Accessor]]  #: Nested accessors.
    _functions: ClassVar[Dict[str, Function]]  #: Data functions.

    def __init__(self, data: Union[xr.DataArray, xr.Dataset]) -> None:
        """Initialize an instance by binding data."""
        super().__setattr__("_accessed", data)

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

    def __setattr__(self, name: str, value: Any) -> None:
        """Disallow setting a value to the instance."""
        raise AttributeError("Cannot set a value to the instance.")
