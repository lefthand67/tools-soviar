---
name: rdd-functional-requirements
description: Translates Business Requirements (BR) into mandatory system constraints (FR). Ensures technical feasibility and edge-case coverage.
---

# PROTOCOL: Functional Requirements Engineering

## [STATE: INITIALIZATION]
- **Input:** `docs/requirements/features/<slug>/br/br.md`
- **Directory Setup:** Create `docs/requirements/features/<slug>/fr/`.
- **Artifacts:** Initialize `fr.md`.

## [STATE: ANALYSIS]
- **Logic:** For each SMART Success Criterion in the BR, derive one or more "The system shall..." statements.
- **Invariant:** Every FR must be traceable to a BR.

## [STATE: DRAFTING]
- **Artifact:** `docs/requirements/features/<slug>/fr/fr.md`
- **Schema:**
  - `FR-ID`: Unique identifier.
  - `Requirement`: "The system shall [behavior] when [trigger]."
  - `Priority`: High | Medium | Low.
  - `Edge-Cases`: Failure modes and responses.
  - `Non-Functional`: Performance, security, or idempotency.
  - `Traceability`: Reference to BR-ID.

## [STATE: REVIEW_GATE]
- **Action:** Dispatch Review Subagent.
- **Context:** `[br/br.md, fr/fr.md]`
- **Review-Criteria:** Completeness, Purity (no "How"), and Testability.
- **Sign-off:** Save the verdict in `docs/requirements/features/<slug>/fr/review.md`.

## [TRANSITION]
Proceed to `rdd-technical-spec`.
