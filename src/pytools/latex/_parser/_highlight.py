import argparse
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ValidationError

from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._types import HighlightKwargs

hl_parser = argparse.ArgumentParser(add_help=False)
hl_parser.add_argument("file", type=Path)
hl_parser.add_argument("--prefix", "-p", type=Path, required=True)


class ProgramArgs(BaseModel):
    file: Path
    prefix: Path


def parse_highlight_args(ns: Mapping[str, Any]) -> Result[tuple[Path, HighlightKwargs]]:
    try:
        args = ProgramArgs(**ns)
    except ValidationError as e:
        return Err(e)
    kwargs: HighlightKwargs = {"out": args.prefix}
    return Ok((args.file, kwargs))
