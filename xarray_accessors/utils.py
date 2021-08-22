__all__ = [
    "get_nested_attr",
    "set_nested_attr",
    "del_nested_attr",
    "has_nested_attr",
]


# standard library
from typing import Any, Sequence


# constants
class Missing:
    def __repr__(self):
        return "<MISSING>"


MISSING: Missing = Missing()


# runtime functions
def get_nested_attr(obj: Any, names: Sequence[str], default: Any = MISSING) -> Any:
    """Get a nested attribute from the given object.

    ``get_nested_attr(x, ['y', 'z'])`` is equivalent to ``x.y.z``.

    Args:
        obj: Object to be evaluated.
        names: Sequence of attribute names.
        default: Default value. It is returned
            if the nested attribute does not exist.

    Returns:
        Nested attribute of an object.

    Raises:
        AttributeError: Raised if the nested attribute
            does not exist and ``default`` is not specified.
        ValueError: Raised if ``names`` is an invalid object
            (e.g., a string, an empty list or tuple).

    """
    if len(names) == 0:
        raise ValueError("At least one name must be specified.")

    attr = getattr(obj, names[0], default)

    if attr is MISSING:
        raise AttributeError(f"{obj!r} has no attribute {names[0]!r}.")

    if len(names) == 1:
        return attr
    else:
        return get_nested_attr(attr, names[1:], default)


def set_nested_attr(obj: Any, names: Sequence[str], value: Any) -> None:
    """Set a nested attribute on the given object to the given value.

    ``set_nested_attr(x, ['y', 'z'], v)`` is equivalent to ``x.y.z = v``.

    Args:
        obj: Object to be evaluated.
        names: Sequence of attribute names.
        values: Value to be set as the nested attribute.

    Raises:
        AttributeError: Raised if the nested attribute does not exist.
        ValueError: Raised if ``names`` is an invalid object
            (e.g., a string, an empty list or tuple).

    """
    if len(names) == 0:
        raise ValueError("At least one name must be specified.")

    if len(names) == 1:
        setattr(obj, names[0], value)
    else:
        setattr(get_nested_attr(obj, names[:-1]), names[-1], value)


def del_nested_attr(obj: Any, names: Sequence[str]) -> None:
    """Remove a nested attribute from the given object.

    ``del_nested_attr(x, ['y', 'z'])`` is equivalent to ``del x.y.z``.

    Args:
        obj: Object to be evaluated.
        names: Sequence of attribute names.

    Raises:
        AttributeError: Raised if the nested attribute does not exist.
        ValueError: Raised if ``names`` is an invalid object
            (e.g., a string, an empty list or tuple).

    """
    if len(names) == 0:
        raise ValueError("At least one name must be specified.")

    if len(names) == 1:
        delattr(obj, names[0])
    else:
        delattr(get_nested_attr(obj, names[:-1]), names[-1])


def has_nested_attr(obj: Any, names: Sequence[str]) -> bool:
    """Return whether an object has a nested attribute.

    Args:
        obj: Object to be evaluated.
        names: Sequence of attribute names.

    Returns:
        ``True`` if the object has the nested attribute. ``False`` otherwise.

    Raises:
        AttributeError: Raised if the nested attribute does not exist.
        ValueError: Raised if ``names`` is an invalid object
            (e.g., a string, an empty list or tuple).

    """
    try:
        get_nested_attr(obj, names)
        return True
    except AttributeError:
        return False
