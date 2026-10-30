# Prompt Generation Engines — Survey

Date: 2026-10-31
Scope: `soviar-systems` working tree (sibling repos added to the workspace)

## Question

Find the engine that generates system prompts out of blocks.

## Answer

Two independent engines implement the same idea — a thin manifest that pulls in
shared JSON blocks via `_includes`, merged into one compiled system prompt —
and are **not shared code**:

| | Engine A | Engine B |
|---|---|---|
| Original location | `ai_engineering_handbook/tools/scripts/prepare_prompt.py` | `mentor_generator/core/compiler/` |
| Style | CLI, single file | Library package |
| Tiering | flat, later-wins | explicit T1/T2/T3 + runtime overrides |

No prompt-generation logic exists in `soviar-toolkit`, `soviar-toolkit-candidate`,
or `tools-soviar` itself.

---

## Engine A — `prepare_prompt.py`

Single-file CLI, 475 lines, one third-party dependency (`pyyaml`).

**Manifests:** `ai_engineering_handbook/ai_system_layers/3_prompts/consultants/*.json`
(`devops_consultant`, `ai_systems_consultant`, `handbook_consultant`,
`ai_brainstorming_colleague`)

**Blocks:** `ai_engineering_handbook/ai_system_layers/3_prompts/blocks/*.json`
(`common_principles`, `common_user_stack`, `common_consulting_context`,
`standard_output_protocol`, `heuer_tradecraft`, `wrc_sva_framework`)

**Mechanism:** `PreparePromptCLI.run()` reads the manifest, then
`_resolve_includes()` walks `_includes` depth-first, parses each include with the
handler matching its extension, `dict.update()`s the result, and finally merges
the manifest's own keys on top. Cycle detection via a `visited` set.

**Output:** YAML-like stream (default) or `--output-format plain` (string values
only). `_strip_chars()` removes `*'"\`#` but preserves `*` where `MATH_PATTERNS`
identify it as multiplication.

**Interfaces:** positional file arg, or `--stdin`; `--input-format` override
(`json|yaml|toml|markdown|text`); `--output-format`; `--verbose`.

**Tests:** `tools/tests/test_prepare_prompt.py` — 1056 lines, 117 test functions.
**Wiring:** `.pre-commit-config.yaml:156`, `.github/workflows/quality.yml:219`.

---

## Engine B — `ThreeTierCompiler`

Package of five modules (plus `__init__.py`), ~25 KB, depends on `pydantic`.

**Blocks:** `mentor_generator/templates/blocks/` (identity + protocol blocks) and
`mentor_generator/templates/domains/`

**Call sites:** `apps/cli/main.py:183` (pipeline Stage 3 "Compile"),
`apps/web/app.py:191`

**Mechanism:** `ThreeTierCompiler.compile_prompt(manifest, t3_path=None,
in_memory_overrides=None)` resolves, in order:

1. `manifest["t1"]` — universal blocks, relative to `t1_path`
2. `manifest["t2"]` — domain blocks, relative to `t2_path`
3. `manifest["t3"]` — project overrides file inside `t3_path`
4. `in_memory_overrides` — runtime steering, documented as having "the final word"

`_resolve_recursive()` merges `_includes` before the current block, so a block
overrides what it includes.

**Safety:**
- `_validate_block()` — Pydantic `IdentityBlock` / `DomainBlock` contracts, applied recursively
- `allowed_roots` + `Path.is_relative_to()` — path-traversal rejection
- `RecursionError` on circular includes
- Empty block file degrades to `{}` with a warning instead of raising

**Output:** `to_yaml_stream()` delegating to `core/compiler/yaml_stream.py`, so the
compiler and the blueprint loader cannot drift. Persisted to
`<project>/.config/system_prompt/system_prompt.txt`.

---

## Key difference: include path resolution

This is the one line that decides whether a block library is relocatable.

- **A** — `include_path = Path(include_path_str)`, i.e. **relative to the process
  CWD**. The handbook's manifests therefore only resolve when the CLI is invoked
  from the repo root; its include strings are written root-relative
  (`"ai_system_layers/3_prompts/blocks/common_user_stack.json"`).
- **B** — `include_path = (abs_path.parent / include_rel_path).resolve()`, i.e.
  **relative to the including block**. Blocks can nest and the tree can move.

## Other differences

| Dimension | A: `prepare_prompt.py` | B: `ThreeTierCompiler` |
|---|---|---|
| Interface | CLI + `--stdin` | Python API |
| Input formats | JSON, YAML, TOML, Markdown-frontmatter, text | JSON only |
| Block schema | none | Pydantic contracts |
| Path traversal guard | none | `allowed_roots` |
| Tier model | flat (list order wins) | T1 / T2 / T3 / in-memory |
| Noise stripping | `_strip_chars`, math-aware | `yaml_stream.strip_noise` |
| Plain-text mode | yes | no |
| Third-party deps | `pyyaml` | `pydantic` |

## Assessment

- **B is the stronger engine** — validated blocks, explicit precedence,
  traversal and cycle protection, relocatable includes.
- **A is the stronger CLI** — multi-format ingestion, plain-text extraction, and
  117 tests already gated in pre-commit and CI.
- A consolidation would take B's resolver + schemas and A's CLI surface and
  format handlers.

---

## What was copied here

```
source/
├── prepare_prompt/
│   └── tools/
│       ├── scripts/prepare_prompt.py      <- ai_engineering_handbook/tools/scripts/
│       └── tests/test_prepare_prompt.py   <- ai_engineering_handbook/tools/tests/
└── three_tier_compiler/
    └── core/compiler/                     <- mentor_generator/core/compiler/
        ├── __init__.py
        ├── domain_resolver.py
        ├── schemas.py
        ├── steering.py
        ├── three_tier.py
        └── yaml_stream.py
```

Original package layout was preserved deliberately: Engine A's tests import
`tools.scripts.prepare_prompt`, and Engine B's modules import
`core.compiler.schemas` / `core.compiler.yaml_stream`. Flattening either would
break imports.

`__pycache__` was excluded.

## Verification

Both engines import from their new locations:

```bash
# Engine A (needs pyyaml)
cd source/prepare_prompt
python3 -c "from tools.scripts.prepare_prompt import PreparePromptCLI; print('A OK')"

# Engine B (needs pydantic)
cd source/three_tier_compiler
python3 -c "from core.compiler.three_tier import ThreeTierCompiler; print('B OK')"
```

Result at time of copy: `A OK`, `B OK`.

## Not copied — known gaps

1. **Block libraries are absent.** Neither engine can produce a prompt without
   them. Sources: `ai_engineering_handbook/ai_system_layers/3_prompts/blocks/`,
   `mentor_generator/templates/blocks/`, `mentor_generator/templates/domains/`.
2. **Engine B's tests were not copied.** They live under
   `mentor_generator/tests/unit/core/` (`test_three_tier_compiler.py`,
   `test_controllability.py`, `test_precision_contract.py`, others) and rely on
   `mentor_generator` settings fixtures.
3. **Engine B is not self-contained.** `domain_resolver.py` and `steering.py`
   import `from apps.cli.collector import UserAnswers`, which was outside the
   copied `core/compiler` package and is not present here. `three_tier.py` and
   `yaml_stream.py` have no such external import.
4. **Engine B requires `Core` package context.** `core/` has no `__init__.py`
   upstream either — it resolves as a PEP 420 namespace package, so the working
   directory must be `source/three_tier_compiler/` for `core.compiler.*` imports.
5. **No packaging metadata** (`pyproject.toml`) was created for either engine.
