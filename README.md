# tools-soviar

## Testing conventions

Uppercase names are placeholders. Replace `AREA`, `UNIT`, and `MODULE` with the real names of the code under test.

### Commands

```bash
# install dependencies
uv sync

# every test in the repo — list each area explicitly
uv run pytest tools -q

# one unit
uv run pytest AREA/UNIT/tests -q

# one test
uv run pytest AREA/UNIT/tests/test_MODULE.py::TestThing -q

# coverage for one unit
uv run pytest AREA/UNIT/tests --cov=AREA.UNIT.MODULE --cov-report=term-missing -q
```

`tools` is the only area today. When you add an area, append it to the all-tests command.

### Layout

Each testable unit is a package that owns its tests:

```
AREA/
└── UNIT/
    ├── __init__.py          # re-exports the public names
    ├── MODULE.py
    └── tests/
        └── test_MODULE.py
```

A unit named `widget` under `tools` therefore reads `tools/widget/`, with tests in `tools/widget/tests/`.

### Rules

- Name directories and files with underscores. Hyphens are not valid in import paths.
- Import by dotted path from the repo root: `from AREA.UNIT import public_name`.
- Re-export every public name from `UNIT/__init__.py`; tests import the package, not the module file.
- Do not create `AREA/__init__.py` or `UNIT/tests/__init__.py`. `AREA` is an implicit namespace package and the tests directory needs no marker.
- Keep `pythonpath = ["."]` in `pyproject.toml`. Add no per-unit paths, and add no `conftest.py` to repair imports.
- Keep `addopts = ["--import-mode=importlib"]` in `pyproject.toml`. Without it, two units with same-named test files fail collection with `import file mismatch`.
- Tests live in the unit they test. Never centralize them in a repo-wide `tests/`.
- Name tests `test_<behaviour>`; use a class only when cases share state.
- A new unit ships with its tests in the same commit.
- Always pass the path to test. Do not run bare `pytest`.
