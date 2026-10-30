# System Prompts — Raw Corpus

Date: 2026-10-31
Sources: `soviar-toolkit`, `soviar-toolkit-candidate`, `prompt_helpers`
Copied: **45 files** — byte-identical to source.

| Subtree | Files | Lines | Format |
|---|---|---|---|
| `soviar-toolkit/`, `soviar-toolkit-candidate/` | 34 | 3,594 | prose + YAML frontmatter |
| `prompt_helpers/` | 11 | 892 | delimited `### BLOCK ###` fences; JSON key-as-block |

The `prompt_helpers` subtree is documented separately in
`prompt_helpers/INDEX.md` — it uses a **third block system** (nested
`### ROLE ###` / `### PRINCIPLES ###` / `### OUTPUT FORMAT ###` fences) that is
the only reusable named-block taxonomy found in the workspace. Read it alongside
`../analysis_20261031_prompt_generation_engines.md`.

The tiers below apply to the two toolkit repos only.

## Why these files and not others

The two repos contain no file that is *named* a system prompt except five files
under `skills/pre-commit-review/prompts/`. Everything else that reaches a model
does so as a skill body, a command body, or agent context. Since the purpose of
this corpus is raw material for prompt generation, the boundary used here is
**"text authored to be read by the model as instruction"**, split into four tiers
so the corpus can be narrowed without re-collecting it.

## Tier A — Dedicated system prompts (5 files, 42 lines)

Referenced verbatim as subagent system prompts by
`soviar-toolkit/skills/pre-commit-review/SKILL.md` ("Read
`skills/pre-commit-review/prompts/<x>_prompt.md`").

| File | Lines |
|---|---|
| `soviar-toolkit/skills/pre-commit-review/prompts/missed_prompt.md` | 9 |
| `soviar-toolkit/skills/pre-commit-review/prompts/misinterpreted_prompt.md` | 9 |
| `soviar-toolkit/skills/pre-commit-review/prompts/lost_prompt.md` | 8 |
| `soviar-toolkit/skills/pre-commit-review/prompts/v1_prompt.md` | 8 |
| `soviar-toolkit/skills/pre-commit-review/prompts/v2_prompt.md` | 8 |

These are the only artifacts in either repo whose sole purpose is to be a prompt.
Each defines one review agent (MISSED, MISINTERPRETED, LOST, V1 Groundness,
V2 Senior Decision) with a role statement, investigation mandate, and a
write-back contract.

## Tier B — Skill instruction prompts (21 files, 2,222 lines)

`SKILL.md` bodies are loaded into the model's context when the skill is invoked,
so they are prompt text with frontmatter attached, not documentation.

### `soviar-toolkit` (7)

| File | Lines |
|---|---|
| `skills/pre-commit-review/SKILL.md` | 41 |
| `qwen/skills/openspec-apply-change/SKILL.md` | 205 |
| `qwen/skills/openspec-archive-change/SKILL.md` | 221 |
| `qwen/skills/openspec-explore/SKILL.md` | 354 |
| `qwen/skills/openspec-propose/SKILL.md` | 174 |
| `qwen/skills/openspec-sync-specs/SKILL.md` | 290 |
| `qwen/skills/openspec-update-change/SKILL.md` | 109 |

### `soviar-toolkit-candidate` (14)

| File | Lines |
|---|---|
| `skills/adversarial-testing-pyramid/SKILL.md` | 144 |
| `skills/agentic-documentation-truth-chain-sync/SKILL.md` | 83 |
| `skills/agentic-observability-and-deterministic-debugging/SKILL.md` | 75 |
| `skills/architectural-alignment-pre-coverage/SKILL.md` | 54 |
| `skills/architectural-ssot-guardrails/SKILL.md` | 33 |
| `skills/deterministic-llm-mocking-strategy/SKILL.md` | 90 |
| `skills/rdd-alignment-audit/SKILL.md` | 64 |
| `skills/rdd-business-requirements/SKILL.md` | 39 |
| `skills/rdd-functional-requirements/SKILL.md` | 34 |
| `skills/rdd-orchestrator/SKILL.md` | 31 |
| `skills/rdd-tactical-planning/SKILL.md` | 36 |
| `skills/rdd-technical-spec/SKILL.md` | 46 |
| `skills/runtime-infrastructure-toggle/SKILL.md` | 47 |
| `skills/three-pillars-implementation/SKILL.md` | 52 |

Two of these carry an explicit role assignment in the body rather than only
procedure — `rdd-orchestrator` ("You are the Project Manager for the
Requirement-Driven Development process") and `rdd-technical-spec` ("You are
managing a Single Shared JSON State"). Those are the closest to Tier A in kind.

## Tier C — Command prompts (6 files, 1,241 lines)

`/opsx-*` slash commands. The command body is the prompt the model executes.

| File | Lines |
|---|---|
| `soviar-toolkit/qwen/commands/opsx-apply.md` | 197 |
| `soviar-toolkit/qwen/commands/opsx-archive.md` | 260 |
| `soviar-toolkit/qwen/commands/opsx-explore.md` | 235 |
| `soviar-toolkit/qwen/commands/opsx-propose.md` | 166 |
| `soviar-toolkit/qwen/commands/opsx-sync.md` | 282 |
| `soviar-toolkit/qwen/commands/opsx-update.md` | 101 |

## Tier D — Agent context (2 files, 89 lines)

Standing project instructions prepended to a session — system-prompt-shaped, but
project-scoped rather than role-scoped.

| File | Lines |
|---|---|
| `soviar-toolkit/AGENTS.md` | 7 |
| `soviar-toolkit-candidate/AGENTS.md` | 82 |

`soviar-toolkit-candidate/AGENTS.md` contains an explicit identity assignment:
"When acting as the `soviar-toolkit` agent, you are not a 'helpful assistant';
you are a **Technical Auditor**."

---

## Path remap

`soviar-toolkit/.qwen/` was copied as `soviar-toolkit/qwen/`. Reason:
`tools-soviar/.gitignore` contains a bare `.qwen/` pattern (intended to exclude
local Qwen Code session settings), which matches a directory of that name at any
depth — a literal `.qwen/` here would have been silently untracked.

No other path was changed. File contents were not read-modified or reformatted.

## Excluded

| Path | Reason |
|---|---|
| `soviar-toolkit/docs/plan/plan_20261003_194935_pre_commit_review.md` | Design plan that *describes* the prompts; not a prompt |
| `soviar-toolkit/skills/pre-commit-review/templates/*.md` | Output report templates, not model instructions |
| `soviar-toolkit/openspec/specs/**, openspec/config.yaml` | Specs and tool config |
| `soviar-toolkit-candidate/docs/**` | ADRs, requirements, standards, feature bundles |
| `soviar-toolkit-candidate/skills/rdd-technical-spec/schemas.json` | Pipeline state schema, not a prompt |
| `soviar-toolkit-candidate/config/*.json` | Toolkit configuration |
| `src/**`, `tests/**`, `pyproject.toml`, `uv.lock`, `LICENSE`, `.gitignore` | Code and packaging |

## Verification

Every copied file was compared to its source with `cmp -s`, mapping
`qwen/` back to `.qwen/` for the remapped subtree:

```
ALL 34 FILES BYTE-IDENTICAL
```

No file was edited after copy.
