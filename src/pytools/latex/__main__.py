import argparse

from ._hl import main as hl_main
from ._merge import main as merge_main
from ._parser import hl_parser, merge_parser, parse_highlight_args, parse_merge_args

parser = argparse.ArgumentParser("main")
subparsers = parser.add_subparsers(dest="command")
subparsers.add_parser(
    "merge", help="Merge a LaTeX project into a single file.", parents=[merge_parser]
)
subparsers.add_parser("remove_hl", help="Remove highlights from a LaTeX file.", parents=[hl_parser])


def main_cli(args: list[str] | None = None) -> None:
    main_args = parser.parse_args(args)
    match main_args.command:
        case "merge":
            home, kwargs = parse_merge_args(**vars(main_args)).unwrap()
            merge_main(home, **kwargs)
        case "remove_hl":
            file, kwargs = parse_highlight_args(**vars(main_args)).unwrap()
            hl_main(file, **kwargs)
        case _:
            parser.print_help()
