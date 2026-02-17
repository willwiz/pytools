import argparse
import dataclasses as dc
from typing import Literal

from ._sh_utils import archive_cli

parser = argparse.ArgumentParser(description="Compress a directory into a tar.gz archive.")
subparsers = parser.add_subparsers(dest="command", required=False)
subparsers.add_parser("archive", help="Compress a directory into a tar.gz archive.")


@dc.dataclass(slots=True)
class MainArguments:
    command: Literal["archive"] | None
    _unrecognized_args: list[str]


def main_cli(args: list[str] | None = None) -> None:
    main_args, extras = parser.parse_known_args(args, namespace=MainArguments(None, []))
    match main_args.command:
        case "archive":
            archive_cli(extras)
        case None:
            parser.print_help()


if __name__ == "__main__":
    main_cli()
