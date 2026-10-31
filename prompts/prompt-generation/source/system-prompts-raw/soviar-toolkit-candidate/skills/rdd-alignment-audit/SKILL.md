---
name: rdd-alignment-audit
description: Final certification of the Feature Bundle. Verifies alignment with RDD principles and synchronizes the project Roadmap.
---

# PROTOCOL: RDD Alignment Audit & Roadmap Sync

## 📏 REFERENCE STANDARD: Feature Bundle Structure
The auditor MUST verify the target directory against this exact hierarchy. Any deviation is a structural failure.

```
<slug>/
├── br/
│   ├── br.md               # Final approved Business Requirements
│   ├── elicitation.md       # Raw clarification questions and user answers
│   └── review.md           # Subagent review logs and approval sign-off
├── fr/
│   ├── fr.md               # Final approved Functional Requirements
│   └── review.md           # Subagent review logs and approval sign-off
├── spec/
│   ├── technical_spec.md    # Final approved Technical Specification
│   ├── council_minutes.json # Raw shared state from the Council of Agents
│   ├── council_report.md    # Rendered Markdown report from council_minutes.json
│   └── review.md           # Final architectural review sign-off
├── tactical_plan.md         # The final execution blueprint (derived from Spec)
└── artifacts/              # Optional: Diagrams, research, and raw logs
```

## [STATE: INITIALIZATION]
- **Target:** `docs/requirements/features/<slug>/`
- **Action:** Scan the feature directory and list all existing files/folders.

## [STATE: STRUCTURAL_VERIFICATION]
- **Logic:** Perform a 1:1 comparison between the actual directory state and the **Reference Standard** above.
- **Checklist:**
  - [ ] All mandatory files are present in their correct sub-folders.
  - [ ] No mandatory files are missing.
  - [ ] Filenames match the standard exactly.
- **Outcome:** Identify any missing or misplaced artifacts.

## [STATE: TRUTH_CHAIN_AUDIT]
- **Logic:** Trace a random sample of requirements from the `tactical_plan.md` $\rightarrow$ `technical_spec.md` $\rightarrow$ `fr.md` $\rightarrow$ `br.md`.
- **Constraint:** No "orphaned" tasks (tasks in the plan with no parent FR) and no "forgotten" requirements (FRs with no implementation task).
- **Outcome:** Report any "Reasoning Drift" or gaps in the chain.

## [STATE: FINAL_CERTIFICATION]
- **Verdict:** 
  - `CERTIFIED`: Bundle is complete, aligned, and structurally sound.
  - `NON_COMPLIANT`: Specific gaps identified.
- **Action:** Create `docs/requirements/features/<slug>/audit_report.md`.
- **Sign-off:** If `CERTIFIED`, the feature is officially ready for implementation.

## [STATE: ROADMAP_SYNC]
- **Trigger:** Only execute if verdict is `CERTIFIED`.
- **Action:** Update `Roadmap.md`.
- **Logic:** 
  1. Search for the feature `<slug>` in the roadmap.
  2. Update its status to `[CERTIFIED]` or `[READY FOR IMPLEMENTATION]`.
  3. Ensure it is slotted into the correct Phase/Milestone.
  4. Add a link to the Feature Bundle: `([Bundle](docs/requirements/features/<slug>))`.
- **Goal:** Ensure the Roadmap is a live reflection of the certified pipeline.

## [ERROR_HANDLING]
- **Non-Compliance:** The agent MUST NOT start coding until the `rdd-alignment-audit` returns a `CERTIFIED` verdict AND the Roadmap is synced.
