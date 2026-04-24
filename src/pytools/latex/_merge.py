import argparse
import dataclasses as dc
import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

_parser = argparse.ArgumentParser()
_parser.add_argument("--home", type=Path)
_parser.add_argument("--out", "-o", type=Path)
_parser.add_argument("--clear", action="store_true")

LATEX_INPUT = re.compile(r"(?:\s*)\\input\{(.*?)\}")
IMAGE_PATH = re.compile(r"(?:\s*)\\includegraphics\[width=(?:\d.*in|\\textwidth)\]{Images/(.*?)}")


@dc.dataclass(slots=True)
class ProgramArgs:
    home: Path
    out: Path
    clear: bool


def parse_args(args: Sequence[str] | None = None) -> ProgramArgs:
    return _parser.parse_args(
        args=args,
        namespace=ProgramArgs(Path("68890842e74e6cc03b23b3df"), Path("journal"), clear=False),
    )


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


def main(args: ProgramArgs) -> None:
    args.out.mkdir(exist_ok=True)
    maintex = args.home / "main.tex"
    joined_tex = ""
    with maintex.open("r") as fin:
        for line in fin:
            joined_tex += merge_into(args.home, line)
    final_tex = ""
    for line in joined_tex.splitlines(keepends=True):
        final_tex += fixed_image_path(line)
    with (args.out / "main.tex").open("w") as fout:
        fout.write(final_tex)
    for img in args.home.glob("Images/*.png"):
        shutil.copyfile(img, args.out / img.name)
    for img in args.home.glob("Images/*.pdf"):
        shutil.copyfile(img, args.out / img.name)
    shutil.copyfile(args.home / "ref.bib", args.out / "ref.bib")
    shutil.copyfile(args.home / "preamble.sty", args.out / "preamble.sty")
    supplement = args.out / "supplement.tex"
    with (args.home / "supplement.tex").open("r") as fin, supplement.open("w") as fout:
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

def clear_dir(args: ProgramArgs) -> None:
    for s in LATEX_TEMPFILES:
        print(s)
        for f in args.out.glob(s):
            print(f)
            f.unlink()


if __name__ == "__main__":
    args = parse_args()
    if args.clear:
        clear_dir(args)
    main(args)
