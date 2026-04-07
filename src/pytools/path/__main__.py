import argparse

from ._sh_utils import gzip_cli, gzip_parser

parser = argparse.ArgumentParser(description="Compress a directory into a tar.gz archive.")
subparsers = parser.add_subparsers(dest="command")
subparsers.add_parser(
    "gzip", help="Compress a directory into a tar.gz archive.", parents=[gzip_parser]
)


def main_cli(args: list[str] | None = None) -> None:
    main_args = parser.parse_args(args)
    match main_args.command:
        case "gzip":
            gzip_cli(args)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main_cli()
