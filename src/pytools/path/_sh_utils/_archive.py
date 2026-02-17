import argparse
import dataclasses as dc
import tarfile
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, get_args

from pytools.logging import LogEnum, LogLevel, get_logger
from pytools.parallel import ThreadedRunner
from pytools.path import IterateAsPath

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

FILTER = Literal["MACOS", "GIT", "PYTHON", ".", "LOG", "DATA"]
FILTERS: Mapping[FILTER, Mapping[Literal["match", "prefix", "suffix"], Sequence[str]]] = {
    "MACOS": {"match": [".DS_Store", "__MACOSX"]},
    "GIT": {"match": [".git"]},
    "PYTHON": {"match": ["__pycache__"], "prefix": [".git", ".venv"]},
    ".": {"prefix": ["."]},
    "LOG": {"suffix": [".log"]},
    "DATA": {"suffix": [".dat"]},
}

parser = argparse.ArgumentParser(description="Compress a directory into a tar.gz archive.")
parser.add_argument(
    "--output-dir", "-o", type=Path, default=Path.cwd(), help="The output tar.gz file path."
)
parser.add_argument(
    "--exclude",
    "-x",
    type=str.upper,
    choices=get_args(FILTER),
    action="append",
    help="Filters to apply when compressing.",
)
parser.add_argument(
    "--log-level",
    type=str.upper,
    choices=get_args(LogLevel),
    default="INFO",
    help="Set the logging level.",
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Perform a dry run without creating the archive.",
)
parser.add_argument(
    "--thread",
    type=int,
    default=1,
    help="Number of parallel compressions to run.",
)
parser.add_argument("input_dir", type=str, nargs="*", help="The input directories to compress.")


@dc.dataclass
class ParsedArgs:
    output_dir: Path
    exclude: list[FILTER]
    input_dir: list[str]
    log_level: LogLevel
    thread: int
    dry_run: bool


class ArchiveFilter:
    __slot__ = ("match_list", "prefix_list", "suffix_list")
    match_list: Final[list[str]]
    prefix_list: Final[list[str]]
    suffix_list: Final[list[str]]

    def __init__(
        self, filters: Mapping[str, Mapping[Literal["match", "prefix", "suffix"], Sequence[str]]]
    ) -> None:
        self.match_list = [v for filt in filters.values() for v in filt.get("match", [])]
        self.prefix_list = [v for filt in filters.values() for v in filt.get("prefix", [])]
        self.suffix_list = [v for filt in filters.values() for v in filt.get("suffix", [])]

    def __call__(self, tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        for pattern in self.match_list:
            if pattern == Path(tarinfo.name).name:
                return None
        for pattern in self.prefix_list:
            if Path(tarinfo.name).name.startswith(pattern):
                return None
        for pattern in self.suffix_list:
            if Path(tarinfo.name).name.endswith(pattern):
                return None
        logger = get_logger()
        logger.disp(f"  Adding {tarinfo.name}", filt=LogEnum.BRIEF)
        return tarinfo


def compress(inpur_dir: Path, output_dir: Path, filt: ArchiveFilter) -> None:
    with tarfile.open(output_dir.with_suffix(".tar.gz"), "w:gz") as tar:
        tar.add(inpur_dir, arcname=inpur_dir.name, filter=filt)


def archive_main(input_dir: Path, output_dir: Path, filt: ArchiveFilter) -> str:
    archive_file = output_dir / input_dir.stem
    compress(input_dir, archive_file, filt=filt)
    return f"Archive for {input_dir} created successfully.\n"


def archive_cli(args: list[str] | None = None) -> None:
    parsed_args = parser.parse_args(args, ParsedArgs(Path(), [], [], "INFO", 1, dry_run=False))
    logger = get_logger(level=parsed_args.log_level)
    if not parsed_args.input_dir:
        parser.print_help()
        return
    if parsed_args.output_dir.is_file():
        logger.fatal(f"Output directory {parsed_args.output_dir} is a file.")
        raise SystemExit(1)
    if not parsed_args.output_dir.is_dir():
        parsed_args.output_dir.mkdir(parents=True, exist_ok=True)
    filter_list = {k: FILTERS[k] for k in parsed_args.exclude}
    file_filter = ArchiveFilter(filter_list)
    items = IterateAsPath(parsed_args.input_dir)
    logger.info("Session is being ran with settings:", dc.asdict(parsed_args))
    if parsed_args.dry_run:
        files = [i for i in items if i.is_file()]
        folders = [i for i in items if i.is_dir()]
        logger.disp(
            "  Filter:", filter_list, "  Archive Folders:", folders, "  Archive Files:", files
        )
        logger.disp("Dry run enabled. No archives will be created.")
        return
    if parsed_args.thread > 1:
        with ThreadedRunner(thread=parsed_args.thread) as runner:
            for input_dir in items:
                runner.submit(archive_main, input_dir, parsed_args.output_dir, filt=file_filter)
                logger.info(f"Archive for {input_dir} submitted.\n")
    else:
        for input_dir in items:
            logger.info(
                f"Compressing {(parsed_args.output_dir / input_dir.stem).with_suffix('.tar.gz')}\n"
            )
            msg = archive_main(input_dir, parsed_args.output_dir, filt=file_filter)
            logger.info(msg)
    logger.info(
        "Completed Archives:",
        [f for input_dir in items for f in parsed_args.output_dir.glob(f"{input_dir.stem}.tar.gz")],
    )
