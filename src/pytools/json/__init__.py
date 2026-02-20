from collections.abc import Mapping, Sequence
from types import MappingProxyType

"""
Type aliases for `json` standard library.
This assumes that the default encoder and decoder are used.
"""


__all__ = "AnyArray", "AnyObject", "AnyValue", "Array", "Object", "_Value"


def __dir__() -> tuple[str, ...]:
    return __all__


###


type _Primitive = bool | int | float | str | None
type _Value = _Primitive | Mapping[str, _Value] | Sequence[_Value]
type _AnyValue = (
    _Primitive
    # NOTE: `TypedDict` can't be included here, since it's not a sub*type* of
    # `dict[str, Any]` according to the typing docs and typeshed, even though
    # it **literally** is a subclass of `dict`...
    | Mapping[str, _AnyValue]
    | MappingProxyType[str, _AnyValue]
    | Sequence[_AnyValue]
    | tuple[_AnyValue, ...]
)


# Return types of `json.load[s]`

type Array[_VT: _Value = _Value] = Sequence[_VT]
type Object[_VT: _Value = _Value] = Mapping[str, _VT]
# ensure that `Value | Array | Object` is equivalent to `Value`
type Value = _Value | Array | Object


# Input types of `json.dumps`

type AnyArray[_AVT: _AnyValue = _AnyValue] = list[_AVT] | tuple[_AVT, ...]
type AnyObject[_AVT: _AnyValue = _AnyValue] = dict[str, _AVT]
type AnyValue = _AnyValue | AnyArray | AnyObject | Value
