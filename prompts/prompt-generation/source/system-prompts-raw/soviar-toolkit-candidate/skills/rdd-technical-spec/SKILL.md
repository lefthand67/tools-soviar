---
name: rdd-technical-spec
description: Architects the technical implementation of Functional Requirements (FR) using a Council of Agents to enrich a single, shared architectural state.
---

# PROTOCOL: Technical Specification Council (State-Mutation Model)

## ⚠️ THE GOLDEN RULE: SINGLE STATE HAND-OFF
This process operates as a **Sequential Enrichment Pipeline**. You are managing a **Single Shared JSON State** located at `docs/requirements/features/<slug>/spec/council_minutes.json`.
- **NO Parallelism:** Agents must work sequentially.
- **State Mutation:** Each subagent receives the current JSON state, populates its assigned fields, and returns the updated state.

## [STATE: INITIALIZATION]
- **Input:** `docs/requirements/features/<slug>/fr/fr.md`
- **Directory Setup:** Create `docs/requirements/features/<slug>/spec/`.
- **Action:** Load FR and relevant ADRs. Initialize `council_minutes.json` as an empty list.

## [STATE: PROPOSAL_GENERATION] (Mutation 1)
- **Agent:** The Ideator (Optimist).
- **Mutation:** Populate ONLY the `proposal` field of 3-5 `solution_object` instances.
- **Handoff:** Main agent saves JSON to `docs/requirements/features/<slug>/spec/council_minutes.json`.

## [STATE: CRITICAL_ENRICHMENT] (Mutation 2)
- **Agent:** The Skeptic (Adversary).
- **Mutation:** Populate the `critique` field for every solution in the shared state.
- **Handoff:** Main agent updates the JSON state.

## [STATE: INTEGRATION_ENRICHMENT] (Mutation 3)
- **Agent:** The Integrator (Realist).
- **Mutation:** Populate the `integration` field for every solution in the shared state.
- **Handoff:** Main agent updates the JSON state.

## [STATE: FINAL_SENSING_AND_VERDICT]
- **Action:** Analyze the fully enriched `council_minutes.json`.
- **Decision:** Filter by compliance, compare integration cost, and select the winning solution.
- **Artifacts:** 
  1. Generate `docs/requirements/features/<slug>/spec/technical_spec.md`.
  2. Execute `python .qwen/skills/rdd-technical-spec/render_council_report.py` to generate `docs/requirements/features/<slug>/spec/council_report.md`.

## [STATE: REVIEW_GATE]
- **Action:** Dispatch independent Review Subagent.
- **Context:** `[fr/fr.md, spec/technical_spec.md]`
- **Sign-off:** Save verdict in `docs/requirements/features/<slug>/spec/review.md`.

## [TRANSITION]
Proceed to `rdd-tactical-planning`.
