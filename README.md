# pytools

Lightweight collection of commonly used Python development utilities and small helper tools for typing, result types, parallel operations, logging, etc.

## Features

- `pytools.array` — convenient generic typing shortcuts for NumPy arrays (e.g., A1[T], shape-aware aliases) and lightweight helpers for type-safe array operations
- `pytools.init_module` — utilities and a small CLI to scaffold/populate new Python submodules with sensible default files and layout.
- `pytools.logging` — light weight feature full logger that requires less setup than stdlib
- `pytools.parallel` — simple concurrency helpers (thread/process pools, task orchestration).
- `pytools.parsing` — factory class for converting argparse to enums or other types
- `pytools.path` — Quick tools for iterating on paths
- `pytools.plotting` — Provides a typed interface for `matplotlib`
- `pytools.progress` — Simple independent progress bar
- `pytools.result` — Result/Option types (Ok/Err) for error handling and propagation without raising

### init_module

Features:
- Populate __all__ and basic docstring stubs; optional type stub/py.typed.
- CLI: see
```bash
python -m pytools.init_module -h
```

## Installation

From source only
```bash
pip install "pytools@git+https://github.com/willwiz/pytools@v1.1"
```

## License

MIT — see LICENSE file

## Support

Use the repository issue tracker for questions and bug reports.