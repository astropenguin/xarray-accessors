__all__ = [
    "get_nested_attr",
]


# standard library
from typing import Any, Sequence


# constants
class Missing:
    def __repr__(self):
        return "<MISSING>"


MISSING: Missing = Missing()  #: An instance for missing value.


# main features
def get_nested_attr(obj: Any, names: Sequence[str], default: Any = MISSING) -> Any:
    """Get a nested attribute from the given object.

    `get_nested_attr(x, ['y', 'z'])` is equivalent to `x.y.z`.

    Args:
        obj: Object to be evaluated.
        names: Sequence of attribute names.
        default: Default value. It is returned
            if the nested attribute does not exist.

    Returns:
        Nested attribute of an object.

    Raises:
        AttributeError: Raised if the nested attribute
            does not exist and `default` is not specified.
        ValueError: Raised if `names` is an invalid object
            (e.g., a string, an empty list or tuple).

    """
    if not isinstance(names, (list, tuple)):
        raise ValueError("Names must be a sequence of strings.")

    if len(names) == 0:
        raise ValueError("At least one name must be specified.")

    name, names = names[0], names[1:]
    nested_obj = getattr(obj, name, default)

    if nested_obj is MISSING:
        raise AttributeError(f"{obj} has no attribute '{name}'.")

    if len(names) == 0:
        return nested_obj
    else:
        return get_nested_attr(nested_obj, names, default)

