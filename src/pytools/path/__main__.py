import argparse

from ._sh_utils import zip_cli, zip_parser

parser = argparse.ArgumentParser(description="Compress a directory into a tar.gz archive.")
subparsers = parser.add_subparsers(dest="command")
subparsers.add_parser(
    "zip", help="Compress a directory into a tar.gz archive.", parents=[zip_parser]
)


def main_cli(args: list[str] | None = None) -> None:
    main_args = parser.parse_args(args)
    match main_args.command:
        case "zip":
            zip_cli(args)
        case None:
            parser.print_help()


if __name__ == "__main__":
    main_cli()
