import argparse
import dataclasses as dc
from pathlib import Path

_parser = argparse.ArgumentParser("init", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
_parser.add_argument("--folder", "-f", type=str, help="Folder in which to initialize the module.")


@dc.dataclass(slots=True)
class _ParsedArguments:
    folder: str | None


def parse_args(args: list[str] | None = None) -> _ParsedArguments:
    return _parser.parse_args(args=args, namespace=_ParsedArguments(None))


def main(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "__init__.py").touch()
    (folder / "__main__.py").touch()
    (folder / "types.py").touch()
    (folder / "api.py").touch()
    (folder / "_argparse.py").touch()


if __name__ == "__main__":
    args = parse_args()
    main(Path(args.folder or "."))
