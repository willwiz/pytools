import argparse
import shutil as sh
import tarfile
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeAliasType,
    TypedDict,
    Unpack,
    get_args,
)

from pydantic import BaseModel, ValidationError

from pytools.logging import LogLevel, get_logger
from pytools.parallel import ThreadedRunner
from pytools.path import expand_as_path
from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


type Filter = Literal["MACOS", "GIT", "PYTHON", "HIDDEN", "LOG", "DATA", "DEFAULT"]


FILTERS: Mapping[Filter, Mapping[Literal["match", "prefix", "suffix"], Sequence[str]]] = {
    "MACOS": {"match": [".DS_Store", "__MACOSX"]},
    "GIT": {"match": [".git"]},
    "PYTHON": {"match": ["__pycache__"], "prefix": [".git", ".venv"]},
    "HIDDEN": {"prefix": ["."]},
    "LOG": {"suffix": [".log"]},
    "DATA": {"suffix": [".dat", ".D"]},
    "DEFAULT": {"prefix": ["."], "match": ["__MACOSX", "__pycache__"], "suffix": [".D", ".log"]},
}

API_KWARGS: Mapping[str, type[Any] | TypeAliasType] = {
    "output_dir": Path,
    "thread": int,
    "log_level": LogLevel,
    "dry_run": bool,
    "dir_only": bool,
}


x_parser = argparse.ArgumentParser("x", add_help=False)
x_parser.add_argument(
    "--output-dir", "-o", type=Path, default=Path.cwd(), help="The output tar.gz file path."
)
x_parser.add_argument(
    "--log-level",
    type=str.upper,
    choices=get_args(LogLevel.__value__),
    default="INFO",
    help="Set the logging level.",
)
x_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Perform a dry run without creating the archive.",
)
x_parser.add_argument(
    "--thread",
    type=int,
    help="Number of parallel compressions to run.",
)
x_parser.add_argument("--dir-only", action="store_true", help="Only compress directories.")
x_parser.add_argument("names", type=str, nargs="+", help="The input directories to compress.")


class XtractionModel(BaseModel):
    output_dir: Path
    log_level: LogLevel
    dry_run: bool
    thread: int | None
    dir_only: bool
    names: list[Path]


class XArgs(TypedDict, total=True):
    names: list[Path]


class XKwargs(TypedDict, total=False):
    output_dir: Path
    log_level: LogLevel
    dry_run: bool
    thread: int | None
    dir_only: bool


def compose_program_args(archives: Mapping[Path, Path]) -> list[object]:
    files = {v for v in archives.values() if v.is_file()}
    folders = {v for v in archives.values() if v.is_dir()}
    return [
        "  Archive Folders:",
        folders,
        "  Archive Files:",
        files,
    ]


def extract_core(output_dir: Path, input_item: Path) -> str:
    if input_item.suffixes == [".tar", ".gz"]:
        with tarfile.open(input_item, "r:gz") as tar:
            tar.extractall(output_dir, filter="data")
        return f"Tar Gzip Archive {input_item} extracted successfully.\n"
    if input_item.suffix == ".zip":
        msg = "Zip file extraction is not implemented yet."
        raise NotImplementedError(msg)
    sh.copy2(input_item, output_dir / input_item.name)
    return f"Input {input_item} is a file, copied ...\n"


def extract_api(files: Sequence[Path], **kwargs: Unpack[XKwargs]) -> Result[None]:
    log = get_logger(level=kwargs.get("log_level"))
    log.info(">>> Running sessions with settings:", dict(kwargs))
    output_dir = kwargs.get("output_dir", Path.cwd())
    if output_dir.is_file():
        msg = f"Output directory: {output_dir} is a file!"
    if not output_dir.is_dir():
        msg = f"Output directory: {output_dir} was not found!"
        return Err(ValueError(msg))
    items = expand_as_path(files)
    items = [i for i in items if not i.name.endswith(".tar.gz")]
    if kwargs.get("dir_only"):
        items = [i for i in items if i.is_dir()]
    if not items:
        msg = "No item found for compression"
        log.warn(msg)
        return Err(FileNotFoundError(msg))
    archives = {output_dir / i.with_suffix(".tar.gz"): i for i in items}
    log.info(*compose_program_args(archives))
    if kwargs.get("dry_run"):
        log.info(">>> Dry run complete. No archives were created.")
        return Ok(None)
    if threads := kwargs.get("thread"):
        with ThreadedRunner(thread=threads) as runner:
            for input_item in items:
                runner.submit(extract_core, output_dir, input_item)
                log.info(f"Archive for {input_item} submitted.\n")
    else:
        for input_item in items:
            log.info(f"Extracting {input_item}")
            log.info(extract_core(output_dir, input_item))
    log.info(
        "Completed Archives:",
        [k for k in archives if k.is_file()],
    )
    return Ok(None)


def parse_x_args(args: Sequence[str] | None = None) -> Result[tuple[XArgs, XKwargs]]:
    try:
        parsed_args = XtractionModel(**vars(x_parser.parse_args(args)))
    except ValidationError as e:
        return Err(e)
    _args = XArgs(names=parsed_args.names)
    _kwargs = XKwargs(
        output_dir=parsed_args.output_dir,
        log_level=parsed_args.log_level,
        dry_run=parsed_args.dry_run,
        thread=parsed_args.thread,
        dir_only=parsed_args.dir_only,
    )
    return Ok((_args, _kwargs))


def x_cli(args: list[str] | None = None) -> None:
    files, kwargs = parse_x_args(args).unwrap()
    extract_api(files["names"], **kwargs)
