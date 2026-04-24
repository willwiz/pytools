import argparse
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ValidationError

from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Mapping

    from pytools.latex._parser._types import MergeKwargs

merge_parser = argparse.ArgumentParser(add_help=False)
merge_parser.add_argument("proj", type=Path)
merge_parser.add_argument("--out", "-o", type=Path, required=True)
merge_parser.add_argument("--clear", action="store_true")


class ProgramArgs(BaseModel):
    proj: Path
    out: Path
    clear: bool = False


def parse_merge_args(ns: Mapping[str, Any]) -> Result[tuple[Path, MergeKwargs]]:
    try:
        args = ProgramArgs(**ns)
    except ValidationError as e:
        return Err(e)
    kwargs: MergeKwargs = {"out": args.out, "clear": args.clear}
    return Ok((args.proj, kwargs))
