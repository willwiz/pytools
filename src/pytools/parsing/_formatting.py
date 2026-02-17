from collections.abc import Mapping, Sequence
from typing import Any, cast

SCREEN_WRAP_LIMIT = 100
TAB = "  "


def list_format(lst: Sequence[Any], *, layer: int = 0) -> str:
    items = [ppfmt(item, layer=layer + 1) for item in lst]
    total_len = sum(len(item) for item in items) + 2 * (len(items) - 1) + 2 * (layer + 1)
    indent = TAB * layer
    head = "[\n"
    if total_len <= SCREEN_WRAP_LIMIT:
        return "[" + ", ".join(items) + "]"
    body = ",\n".join(f"{TAB * (layer + 1)}{item}" for item in items)
    tail = f"\n{indent}]"
    return head + body + tail


def dict_format(dct: Mapping[str, object], *, layer: int = 0) -> str:
    items = {k: f"{k!s}: {ppfmt(v, layer=layer + 1)}" for k, v in dct.items()}
    total_len = sum(len(v) for v in items.values()) + 2 * (len(items) - 1) + 2 * (layer + 1)
    if total_len <= SCREEN_WRAP_LIMIT:
        return "{" + ", ".join(items.values()) + "}"
    head = "{\n"
    body = ",\n".join(f"{TAB * (layer + 1)}{v}" for v in items.values())
    tail = f"\n{TAB * layer}}}"
    return head + body + tail


def ppfmt(items: object, *, layer: int = 0) -> str:
    match items:
        case str() | float() | int():
            return str(items)
        case Mapping():
            return dict_format(cast("Mapping[str, object]", items), layer=layer)
        case Sequence():
            return list_format(cast("Sequence[object]", items), layer=layer)
        # case Iterable():
        #     return list_format(items, layer=layer)
        case _:
            return str(items)
