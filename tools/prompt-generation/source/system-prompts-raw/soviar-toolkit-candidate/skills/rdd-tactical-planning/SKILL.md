---
name: rdd-tactical-planning
description: Translates the Technical Specification into an executable, step-by-step tactical plan.
---

# PROTOCOL: Tactical Planning Engineering

## [STATE: INITIALIZATION]
- **Input:** `docs/requirements/features/<slug>/spec/technical_spec.md`
- **Pre-condition:** Tech Spec must be approved (see `spec/review.md`).
- **Artifact:** Initialize `docs/requirements/features/<slug>/tactical_plan.md`.

## [STATE: DECOMPOSITION]
- **Logic:** Break the technical design into atomic, verifiable tasks.
- **Invariant:** Every task must be a "small win" that can be verified by a specific command.
- **Schema:**
  - `Step-ID`: (e.g., T-01).
  - `Action`: "Implement [function] in [file] to achieve [FR-ID]."
  - `Verification`: The exact command to run (e.g., `pytest tests/unit/core/test_x.py`).
  - `Dependency`: Which previous steps must be completed first.

## [STATE: DRAFTING]
- **Action:** Write the final `tactical_plan.md`.
- **Format:**
  1. **Goal:** High-level summary of the implementation.
  2. **Checklist:** The decomposed steps in sequential order.
  3. **Final Verification:** The E2E test command to certify the feature.

## [STATE: REVIEW_GATE]
- **Action:** Dispatch Review Subagent.
- **Context:** `[spec/technical_spec.md, tactical_plan.md]`
- **Review-Criteria:** Is the plan a perfect mapping of the spec? Are the verification commands accurate?
- **Sign-off:** Save verdict in `docs/requirements/features/<slug>/tactical_plan_review.md`.

## [TRANSITION]
Proceed to `rdd-alignment-audit` for final bundle certification.
