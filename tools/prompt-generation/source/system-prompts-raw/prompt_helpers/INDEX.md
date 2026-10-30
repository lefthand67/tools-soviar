# System Prompts — `prompt_helpers`

Date: 2026-10-31
Source: `/home/commi/Yandex.Disk/it_learning/17_ai_engineering/prompt_helpers` (outside the workspace)
Copied: **11 files, 892 lines** — byte-identical to source.

## Why this corpus matters

The two toolkit repos' prompts are prose with YAML frontmatter. These are not.
Every `.md` here uses an explicit **delimited block format**:

```
### METADATA ###        ... ### END METADATA ###
### SYSTEM PROMPT ###   ... ### END SYSTEM PROMPT ###
### USER INPUT ###      ... ### END USER INPUT ###
```

Inside `SYSTEM PROMPT`, named blocks nest:

```
### ROLE ###
### PRINCIPLES ###
### CORE CONTEXT ###
### AUDIENCE PROTOCOL ###      <- wrapper block
    ### ANSWER TARGET ###      <- nested
    ### USER PROFILE ###       <- nested
### CONSULTING PROTOCOL ###
### INPUT PROTOCOL ###         <- wrapper block
    ### EXPECTED INPUT ###
    ### INPUT CHECK ###
    ### CORE PROCEDURES ###
### OUTPUT FORMAT ###
```

This is a third block system, distinct from `prepare_prompt.py` and
`ThreeTierCompiler` (see `../analysis_20261031_prompt_generation_engines.md`),
and it is the only one in the workspace that carries a **reusable, named block
taxonomy** — ROLE / PRINCIPLES / CORE CONTEXT / AUDIENCE PROTOCOL / CONSULTING
PROTOCOL / INPUT PROTOCOL / OUTPUT FORMAT — shared across otherwise unrelated
prompts. That taxonomy is the most directly reusable artifact for a
blocks-to-prompt engine.

The JSON files express the same idea with object keys as blocks.

## Contents

### Markdown, delimited-block format (7)

| File | Lines | Version | Domain |
|---|---|---|---|
| `ai_consultant.md` | 103 | 0.2.0 | AI Powered Systems (CV, NLP) |
| `ai_consultant_small_llms.md` | 106 | 0.1.0 | AI Powered Systems (CV, NLP), SLLM variant |
| `business_analysis.md` | 103 | 0.2.0 | AI-Powered Business Requirements Engineering |
| `prompt_consultant.md` | 108 | 0.12.0 | AI-Powered Requirement Engineering |
| `tech_analysis.md` | 75 | 0.3.0 | AI-Powered Technical Solutions Engineering |
| `translator.md` | 43 | 0.2.0 | AI-Powered Technical Translator |
| `telegram_postman.md` | 3 | — | Telegram post drafting (bare instruction, no block structure) |

Primary functions, verbatim from their metadata:

- `ai_consultant` — "Peer review and critique of architectural and software
  engineering concepts for industrial applications of AI powered systems."
- `business_analysis` — "Business Requirements Elicitation from the vague user input."
- `prompt_consultant` — "Peer review and critique of system prompts for industrial
  applications." (highest version in the set at 0.12.0 — the most iterated)
- `tech_analysis` — "Generate solutions from the business requirements."
- `translator` — "Translation of the texts already passed the review."

`ai_consultant.md` and `ai_consultant_small_llms.md` are the same role at
different targets — the pair is a natural before/after for model-size-dependent
prompt tuning.

### JSON, key-as-block format (3)

| File | Lines | Version | Top-level blocks |
|---|---|---|---|
| `mentor_simple.json` | 57 | — | `pedagogical_principles`, `teaching_style`, `feedback_approach`, `emergency_brake_rules`, `structure_data`, `mastery_gated_progression` |
| `linux_brainstorming_colleague.json` | 104 | 0.3.1 | `metadata`, `input_protocol`, `system`, `target`, `exploration_protocol`, `output_protocol`, `USER_INPUT` |
| `strategic_autonomy_architect_personal.json` | 73 | 0.1.2 | `metadata`, `system_identity`, `user_context_anchor`, `operational_instructions`, `knowledge_domains`, `72_hour_velocity_protocol`, `session_state_summary`, `output_protocol` |

These three are structurally the closest match to what `ThreeTierCompiler`
consumes (`dict` of named blocks), and `mentor_simple.json` is the cleanest
example of pure pedagogical blocks with no identity or protocol scaffolding.

`linux_brainstorming_colleague.json` carries `owner: rudakow.wadim@gmail.com` in
its metadata — copied as-is, unchanged.

### Plain text (1)

| File | Lines | Contents |
|---|---|---|
| `prompts.txt` | 117 | 5 ad-hoc utility prompts, numbered `# 1.`–`# 5.`: reformat text, markdown source list, reformat-preserving-style, detailed summary, create table |

Not a system prompt — included because it is prompt text in the same collection
and shows the short-form instruction style used alongside the long-form blocks.

## Excluded

| Path | Reason |
|---|---|
| `data/who_i_am.md` (73 lines) | Personal profile — professional summary, employer, project links. Personal context, not a system prompt. Referenced by no file in the set (verified by grep). |
| `data/my_experience.md` (89 lines) | Personal career/experience narrative. Same reasoning. |
| `data/Untitled.ipynb` (16 KB) | Untitled scratch notebook. |
| `data/.ipynb_checkpoints/*` (3 files) | Editor checkpoint artifacts — duplicates of the above. |

The two `data/*.md` files are the raw material for the `### USER PROFILE ###` and
`user_context_anchor` blocks that appear — unfilled — inside these prompts. They
were left out because they are personal data rather than prompts, and moving
them into a separate git repository is a decision worth making explicitly.
Say the word and they can be added.

## Verification

```
ALL FILES BYTE-IDENTICAL
```

Each copied file compared with `cmp -s` against its source. No file was edited,
reformatted, or stripped of its metadata fences.
