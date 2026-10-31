---
name: architectural-alignment-pre-coverage
description: Strategy for ensuring code alignment with the Architectural Source of Truth (SSoT) before performing industrial-grade test coverage.
source: auto-skill
extracted_at: '2026-06-03T12:00:00Z'
---

# Architectural Alignment Pre-Coverage

This skill defines a critical guardrail for the "Industrialization" process. It prevents the "Bottom-Up Coverage Trap," where an agent spends significant effort making legacy code testable and covered, only to discover that the code is "corrupt" relative to the current Architectural Source of Truth (SSoT).

## ⚠️ The "Bottom-Up" Coverage Trap
In a fast-evolving project, it is tempting to see a module with 60% coverage and attempt to reach 100% by:
1.  Extracting pure functions to remove I/O dependencies.
2.  Adding complex mocks to handle edge cases.
3.  Writing L1-L3 tests for every permutation of existing logic.

**The Risk:** If the architecture has shifted (e.g., from a "Generative" approach to a "Deterministic Block Assembly" approach), you are essentially polishing a "ghost"—investing effort into a codebase that is fundamentally misaligned with the current ADRs.

## 🎯 The Symmetry Mandate
Before attempting to increase coverage or industrialize a module, the agent MUST verify the **Symmetry** between the implementation and the SSoT.

### The Alignment Checklist
Ask these three questions before writing a single test:
1.  **Purpose Alignment**: Does this module's primary goal still exist in the current `Roadmap.md`?
2.  **Mechanism Alignment**: Does the implementation use the mandated patterns (e.g., "Skeptical Mastery", "Three-Tier Block System") or is it using a deprecated approach (e.g., "Guideline-based prompting")?
3.  **Data-Flow Alignment**: Does the input/output of this module match the requirements of the current `system_blueprint.md`?

## 🛠️ Alignment Procedure

### 1. Top-Down Audit
Instead of reading the code first, read the documentation:
- Review the latest relevant **ADRs**.
- Check the current **Roadmap** phase.
- Examine the **Architectural Blueprint**.

### 2. Gap Analysis
Compare the current implementation against the audit results:
- **Redundant Logic**: Identify functions that calculate values no longer used by the system.
- **Logic Mismatches**: Identify "Probabilistic/Generative" logic that should now be "Deterministic/Compiled".
- **Missing Requirements**: Identify new constraints mandated by ADRs that are absent from the code.

### 3. The Decision Matrix

| Analysis Result | Action | Strategy |
| :--- | :--- | :--- |
| **Aligned** | $\rightarrow$ Industrialize | Proceed with pure function extraction and L1-L4 coverage. |
| **Minor Drift** | $\rightarrow$ Refactor $\rightarrow$ Industrialize | Align the logic to the SSoT first, then implement coverage. |
| **Fundamentally Corrupt** | $\rightarrow$ Redesign / Delete | Do not attempt to cover. Mark as "Corrupt State" and rewrite based on the SSoT. |

## 📈 Benefits
- **Token Efficiency**: Avoids wasting context and tokens on legacy refactoring.
- **Engineering Integrity**: Ensures that 100% coverage actually means "100% of the *correct* logic is verified."
- **Reasoning Clarity**: Prevents the agent from becoming "wedded" to a specific implementation just because it has high test coverage.
