import re
from typing import TYPE_CHECKING, Unpack

from ._parser import HighlightKwargs

if TYPE_CHECKING:
    from pathlib import Path


HIGHTLIGHTED = re.compile(r"\\hlc[.+]{(?P<tex>.*)}")


def insert_section(file: Path) -> str:
    with file.open("r") as f:
        return f.read()


def main(maintex: Path, **_kwargs: Unpack[HighlightKwargs]) -> None:
    with maintex.open("r") as fin:
        for line in fin:
            match HIGHTLIGHTED.match(line):
                case None:
                    pass
                case m:
                    print(HIGHTLIGHTED.sub(line, m.group("tex")))
