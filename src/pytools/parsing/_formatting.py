import dataclasses as dc
from argparse import Namespace
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, TypeIs, cast, runtime_checkable

import numpy as np

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

SCREEN_WRAP_LIMIT = 100
TAB = "  "


def list_format(lst: Sequence[Any], *, layer: int = 0, w_limit: int = SCREEN_WRAP_LIMIT) -> str:
    items = [ppfmt(item, layer=layer + 1, w_limit=w_limit) for item in lst]
    total_len = sum(len(item) for item in items) + 2 * (len(items) - 1) + len(TAB) * (layer + 1)
    if total_len <= w_limit:
        return "[" + ", ".join(items) + "]"
    indent = TAB * layer
    head = "[\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{item}" for item in items])
    tail = f"\n{indent}]"
    return head + body + tail


def dict_format(
    dct: Mapping[str, object], *, layer: int = 0, w_limit: int = SCREEN_WRAP_LIMIT
) -> str:
    items = {k: f"{k!s}: {ppfmt(v, layer=layer + 1, w_limit=w_limit)}" for k, v in dct.items()}
    total_len = sum(len(v) for v in items.values()) + 2 * (len(items) - 1) + len(TAB) * (layer + 1)
    if total_len <= w_limit:
        return "{" + ", ".join(items.values()) + "}"
    head = "{\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{v}" for v in items.values()])
    tail = f"\n{TAB * layer}}}"
    return head + body + tail


def set_format(st: set[object], *, layer: int = 0, w_limit: int = SCREEN_WRAP_LIMIT) -> str:
    items = [ppfmt(item, layer=layer + 1, w_limit=w_limit) for item in st]
    total_len = sum(len(item) for item in items) + 2 * (len(items) - 1) + len(TAB) * (layer + 1)
    if total_len <= w_limit:
        return "{" + ", ".join(items) + "}"
    indent = TAB * layer
    head = "{\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{item}" for item in items])
    tail = f"\n{indent}}}"
    return head + body + tail


def _is_dataclass_instance(obj: object) -> TypeIs[DataclassInstance]:
    return dc.is_dataclass(obj) and not isinstance(obj, type)


def dc_format(obj: DataclassInstance, *, layer: int = 0, w_limit: int = SCREEN_WRAP_LIMIT) -> str:
    class_name = obj.__class__.__name__
    items = {
        f.name: f"{f.name}: {ppfmt(getattr(obj, f.name), layer=layer + 1, w_limit=w_limit)}"
        for f in dc.fields(obj)
    }
    total_len = (
        len(class_name)
        + sum(len(v) for v in items.values())
        + 2 * (len(items) - 1)
        + len(TAB) * (layer + 1)
    )
    indent = TAB * layer
    if total_len <= w_limit:
        return f"{class_name}({', '.join(items.values())})"
    if total_len - len(class_name) <= w_limit:
        return f"{class_name}(\n" + TAB * (layer + 1) + ", ".join(items.values()) + f"\n{indent})"
    head = f"{class_name}(\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{v}" for v in items.values()])
    tail = f"\n{indent})"
    return head + body + tail


def class_format(obj: object, *, layer: int = 0, w_limit: int = SCREEN_WRAP_LIMIT) -> str:
    class_name = obj.__class__.__name__
    items = {k: f"{k}: {ppfmt(v, layer=layer + 1, w_limit=w_limit)}" for k, v in vars(obj).items()}
    total_len = (
        len(class_name)
        + sum(len(v) for v in items.values())
        + 2 * (len(items) - 1)
        + len(TAB) * (layer + 1)
    )
    indent = TAB * layer
    if total_len <= w_limit:
        return f"{class_name}({', '.join(items.values())})"
    if total_len - len(class_name) <= w_limit:
        return f"{class_name}(\n" + TAB * (layer + 1) + ", ".join(items.values()) + f"\n{indent})"
    head = f"{class_name}(\n"
    body = ",\n".join([f"{TAB * (layer + 1)}{v}" for v in items.values()])
    tail = f"\n{indent})"
    return head + body + tail


@runtime_checkable
class HasToStr(Protocol):
    def __str__(self) -> str: ...


def ppfmt(items: object, *, layer: int = 0, w_limit: int = SCREEN_WRAP_LIMIT) -> str:
    match items:
        case str() | float() | int() | Path():
            v = repr(items) if isinstance(items, Path) else str(items)
            v = v.replace("\n", f"\n{TAB * (layer + 1)}")
        case Mapping():
            v = dict_format(cast("Mapping[str, object]", items), layer=layer, w_limit=w_limit)
        case Sequence() | np.ndarray():
            v = list_format(cast("Sequence[object]", items), layer=layer, w_limit=w_limit)
        case set():
            v = set_format(cast("set[object]", items), layer=layer, w_limit=w_limit)
        case _ if _is_dataclass_instance(items):
            v = dc_format(items, layer=layer, w_limit=w_limit)
        case Namespace():
            v = class_format(items, layer=layer, w_limit=w_limit)
        case HasToStr():
            v = str(items).replace("\n", f"\n{TAB * (layer + 1)}")
    return v
