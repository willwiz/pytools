import dataclasses as dc
import re
import shutil
from typing import TYPE_CHECKING, Unpack

from ._parser import MergeKwargs, merge_parser, parse_merge_args

if TYPE_CHECKING:
    from pathlib import Path

LATEX_INPUT = re.compile(r"(?:\s*)\\input\{(.*?)\}")
IMAGE_PATH = re.compile(r"(?:\s*)\\includegraphics\[width=(?:\d.*in|\\textwidth)\]{Images/(.*?)}")


@dc.dataclass(slots=True)
class ProgramArgs:
    home: Path
    out: Path
    clear: bool


def insert_section(file: Path) -> str:
    with file.open("r") as f:
        return f.read()


def merge_into(home: Path, line: str) -> str:
    match LATEX_INPUT.match(line):
        case None:
            return line
        case m:
            return insert_section(home / m.group(1))


def fixed_image_path(line: str) -> str:
    match IMAGE_PATH.match(line):
        case None:
            return line
        case _:
            return line.replace(r"Images/", "")


def main(home: Path, **kwargs: Unpack[MergeKwargs]) -> None:
    output_dir = kwargs["out"]
    output_dir.mkdir(exist_ok=True)
    if kwargs.get("clear"):
        clear_dir(**kwargs)
    maintex = home / "main.tex"
    joined_tex = ""
    with maintex.open("r") as fin:
        for line in fin:
            joined_tex += merge_into(home, line)
    final_tex = ""
    for line in joined_tex.splitlines(keepends=True):
        final_tex += fixed_image_path(line)
    with (output_dir / "main.tex").open("w") as fout:
        fout.write(final_tex)
    for img in home.glob("Images/*.png"):
        shutil.copyfile(img, output_dir / img.name)
    for img in home.glob("Images/*.pdf"):
        shutil.copyfile(img, output_dir / img.name)
    shutil.copyfile(home / "ref.bib", output_dir / "ref.bib")
    shutil.copyfile(home / "preamble.sty", output_dir / "preamble.sty")
    supplement = output_dir / "supplement.tex"
    with (home / "supplement.tex").open("r") as fin, supplement.open("w") as fout:
        for line in fin:
            fout.write(fixed_image_path(line))


LATEX_TEMPFILES = [
    "*.aux",
    "*.bit",
    "*.blg",
    "*.bbl",
    "*.lof",
    "*.log",
    "*.lot",
    "*.glo",
    "*.glx",
    "*.gxg",
    "*.gxs",
    "*.idx",
    "*.ilg",
    "*.ind",
    "*.out",
    "*.url",
    "*.svn",
    "*.toc",
    "*.fls",
    "*.fdb_latexmk",
    "*.synctex.gz",
    "*.dvi",
    "*.ps",
    "*.bbl.bak",
    "*.spl",
]


def clear_dir(**kwargs: Unpack[MergeKwargs]) -> None:
    for s in LATEX_TEMPFILES:
        print(s)
        for f in kwargs["out"].glob(s):
            print(f)
            f.unlink()


def main_cli(args: list[str] | None = None) -> None:
    _args = merge_parser.parse_args(args)
    home, kwargs = parse_merge_args(**vars(_args)).unwrap()
    main(home, **kwargs)
