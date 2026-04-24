import argparse

from ._merge import main as merge_main
from ._parser import merge_parser, parse_merge_args

parser = argparse.ArgumentParser("main")
subparsers = parser.add_subparsers(dest="command")
subparsers.add_parser(
    "merge", help="Merge a LaTeX project into a single file.", parents=[merge_parser]
)


def main_cli(args: list[str] | None = None) -> None:
    main_args = parser.parse_args(args)
    match main_args.command:
        case "merge":
            home, kwargs = parse_merge_args(**vars(main_args)).unwrap()
            merge_main(home, **kwargs)
        case _:
            parser.print_help()
