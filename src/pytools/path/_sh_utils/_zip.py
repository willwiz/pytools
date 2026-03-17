import argparse
import tarfile
from collections.abc import Sequence
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    Literal,
    NamedTuple,
    TypedDict,
    TypeIs,
    Unpack,
    get_args,
    get_origin,
)

from pytools.logging import LogEnum, LogLevel, get_logger
from pytools.parallel import ThreadedRunner
from pytools.path import expand_as_path
from pytools.result import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import UnionType

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

zip_parser = argparse.ArgumentParser(
    description="Compress a directory into a tar.gz archive.", add_help=False
)
zip_parser.add_argument(
    "--output-dir", "-o", type=Path, default=Path.cwd(), help="The output tar.gz file path."
)
zip_parser.add_argument(
    "--exclude",
    "-x",
    type=str.upper,
    choices=get_args(Filter.__value__),
    action="append",
    help="Filters to apply when compressing.",
)
zip_parser.add_argument(
    "--log-level",
    type=str.upper,
    choices=get_args(LogLevel),
    default="INFO",
    help="Set the logging level.",
)
zip_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Perform a dry run without creating the archive.",
)
zip_parser.add_argument(
    "--thread",
    type=int,
    default=1,
    help="Number of parallel compressions to run.",
)
zip_parser.add_argument("names", type=str, nargs="+", help="The input directories to compress.")


def _is_type[T: Any](args: object, kind: type[T] | UnionType) -> TypeIs[T]:
    if get_origin(kind) == Literal:
        return args in get_args(kind)
    return isinstance(args, kind)


def _is_sequence_t[T: Any](args: object, kind: type[T] | UnionType) -> TypeIs[Sequence[T]]:
    if not isinstance(args, Sequence):
        return False
    return all(_is_type(i, kind) for i in args)


class APIKwargs(TypedDict, total=False):
    output_dir: Path
    filters: Sequence[Filter]
    log_level: LogLevel
    thread: int
    dry_run: bool


class _CmdLineArguments(NamedTuple):
    names: Sequence[str]
    kwargs: APIKwargs


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


def compress(output_file: Path, *input_dir: Path, filt: ArchiveFilter) -> None:
    with tarfile.open(output_file.with_suffix(".tar.gz"), "w:gz") as tar:
        for folder in input_dir:
            tar.add(folder, filter=filt)


def archive_core(output_dir: Path, input_dir: Path, filt: ArchiveFilter) -> str:
    archive_file = output_dir / input_dir.stem
    compress(archive_file, input_dir, filt=filt)
    return f"Archive for {input_dir} created successfully.\n"


def archive_api(*names: str | Path, **kwargs: Unpack[APIKwargs]) -> Result[None]:
    log = get_logger(level=kwargs.get("log_level"))
    output_dir = kwargs.get("output_dir", Path.cwd())
    if output_dir.is_file():
        msg = f"Output directory: {output_dir} is a file!"
    if not output_dir.is_dir():
        msg = f"Output directory: {output_dir} was not found!"
        return Err(ValueError(msg))
    filters = kwargs.get("filters", [])
    if not filters:
        log.debug("No filters specified, using default.")
    log.info("Running sessions with settings", dict(kwargs))
    filter_list = {k: FILTERS[k] for k in (filters or ["DEFAULT"])}
    item_filter = ArchiveFilter(filter_list)
    items = expand_as_path(names)
    if not items:
        msg = "No item found for compression"
        log.warn(msg)
        return Err(FileNotFoundError(msg))
    log.info("Files Found:", items)
    if kwargs.get("dry_run"):
        files = [i for i in items if i.is_file()]
        folders = [i for i in items if i.is_dir()]
        log.disp("  Filter:", filter_list, "  Archive Folders:", folders, "  Archive Files:", files)
        log.disp("Dry run enabled. No archives will be created.")
        return Ok(None)
    if threads := kwargs.get("thread"):
        with ThreadedRunner(thread=threads) as runner:
            for input_dir in items:
                runner.submit(archive_core, output_dir, input_dir, filt=item_filter)
                log.info(f"Archive for {input_dir} submitted.\n")
    else:
        for input_dir in items:
            log.info(f"Compressing {(output_dir / input_dir.stem).with_suffix('.tar.gz')}\n")
            msg = archive_core(output_dir, input_dir, filt=item_filter)
            log.info(msg)
    log.info(
        "Completed Archives:",
        [f for input_dir in items for f in output_dir.glob(f"{input_dir.stem}.tar.gz")],
    )
    return Ok(None)


API_KWARGS: Mapping[str, type | UnionType] = {
    "output_dir": Path,
    "thread": int,
    "log_level": LogLevel,
    "dry_run": bool,
}


def get_command_line_arguments(args: Sequence[str] | None = None) -> Result[_CmdLineArguments]:
    namespace = vars(zip_parser.parse_args(args))
    names = namespace.get("names")
    if not _is_sequence_t(names, str):
        return Err(ValueError("Missing `names` value"))
    kwargs = APIKwargs()
    for n, k in API_KWARGS.items():
        if _is_type(v := namespace.get(n), k):
            kwargs[n] = v
    filters = namespace.get("filters")
    if _is_sequence_t(filters, Filter.__value__):
        kwargs["filters"] = filters
    return Ok(_CmdLineArguments(names, kwargs))


def zip_cli(args: list[str] | None = None) -> None:
    names, kwargs = get_command_line_arguments(args).unwrap()
    archive_api(*names, **kwargs).unwrap()
