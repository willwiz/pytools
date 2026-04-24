import re
from typing import TYPE_CHECKING, Unpack

if TYPE_CHECKING:
    from pathlib import Path

    from ._parser import HighlightKwargs


HIGHTLIGHTED = re.compile(r"\\hlc\[.+?\]\{(?P<tex>.+?)\}")


def remove_highlight(tex: str) -> str:
    return HIGHTLIGHTED.sub(lambda m: m.group("tex"), tex)


def main(maintex: Path, **kwargs: Unpack[HighlightKwargs]) -> None:
    with maintex.open("r") as fin:
        content = [remove_highlight(line) for line in fin.readlines()]
    with kwargs["out"].open("w") as fout:
        fout.writelines(content)
