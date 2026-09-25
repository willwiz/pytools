import dataclasses as dc
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, TypeIs, cast

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

SCREEN_WRAP_LIMIT = 100
TAB = "  "


def list_format(lst: Sequence[Any], *, layer: int = 0, wrap_limit: int = SCREEN_WRAP_LIMIT) -> str:
    items = [ppfmt(item, layer=layer + 1) for item in lst]
    total_len = sum(len(item) for item in items) + 2 * (len(items) - 1) + 2 * (layer + 1)
    indent = TAB * layer
    head = "[\n"
    if total_len <= wrap_limit:
        return "[" + ", ".join(items) + "]"
    if total_len <= wrap_limit - 2:
        return "[\n" + ", ".join(items) + "\n]"
    body = ",\n".join([f"{TAB * (layer + 1)}{item}" for item in items])
    tail = f"\n{indent}]"
    return head + body + tail


def dict_format(
    dct: Mapping[str, object], *, layer: int = 0, wrap_limit: int = SCREEN_WRAP_LIMIT
) -> str:
    items = {k: f"{k!s}: {ppfmt(v, layer=layer + 1)}" for k, v in dct.items()}
    total_len = sum(len(v) for v in items.values()) + 2 * (len(items) - 1) + 2 * (layer + 1)
    if total_len <= wrap_limit:
        return "{" + ", ".join(items.values()) + "}"
    if total_len <= wrap_limit - 2:
        return "{\n" + ", ".join(items.values()) + "\n}"
    head = "{\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{v}" for v in items.values()])
    tail = f"\n{TAB * layer}}}"
    return head + body + tail


def set_format(st: set[object], *, layer: int = 0, wrap_limit: int = SCREEN_WRAP_LIMIT) -> str:
    items = [ppfmt(item, layer=layer + 1) for item in st]
    total_len = sum(len(item) for item in items) + 2 * (len(items) - 1) + 2 * (layer + 1)
    indent = TAB * layer
    head = "{\n"
    if total_len <= wrap_limit:
        return "{" + ", ".join(items) + "}"
    if total_len <= wrap_limit - 2:
        return "{\n" + ", ".join(items) + "\n}"
    body = ",\n".join([f"{TAB * (layer + 1)}{item}" for item in items])
    tail = f"\n{indent}}}"
    return head + body + tail


def _is_dataclass_instance(obj: object) -> TypeIs[DataclassInstance]:
    return dc.is_dataclass(obj) and not isinstance(obj, type)


def dc_format(
    obj: DataclassInstance, *, layer: int = 0, wrap_limit: int = SCREEN_WRAP_LIMIT
) -> str:
    class_name = obj.__class__.__name__
    items = {
        f.name: f"{f.name}: {ppfmt(getattr(obj, f.name), layer=layer + 1)}" for f in dc.fields(obj)
    }
    total_len = (
        len(class_name)
        + 2
        + sum(len(v) for v in items.values())
        + 2 * (len(items) - 1)
        + 2 * (layer + 1)
    )
    if total_len <= wrap_limit:
        return f"{class_name}({', '.join(items.values())})"
    if total_len <= wrap_limit - len(class_name) - 2:
        return f"{class_name}(\n" + ", ".join(items.values()) + "\n)"
    head = f"{class_name}(\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{v}" for v in items.values()])
    tail = f"\n{TAB * layer})"
    return head + body + tail


def ppfmt(items: object, *, layer: int = 0, wrap_limit: int = SCREEN_WRAP_LIMIT) -> str:
    match items:
        case str() | float() | int():
            return str(items)
        case Mapping():
            return dict_format(
                cast("Mapping[str, object]", items), layer=layer, wrap_limit=wrap_limit
            )
        case Sequence():
            return list_format(cast("Sequence[object]", items), layer=layer, wrap_limit=wrap_limit)
        case set():
            return set_format(cast("set[object]", items), layer=layer, wrap_limit=wrap_limit)
        case _ if _is_dataclass_instance(items):
            return dc_format(items, layer=layer, wrap_limit=wrap_limit)
        # case Iterable():
        #     return list_format(items, layer=layer)
        case _:
            return str(items)
