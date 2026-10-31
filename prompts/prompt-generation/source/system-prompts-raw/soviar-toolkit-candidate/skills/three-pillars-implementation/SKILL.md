---
name: three-pillars-implementation
description: Enforces the Three Pillars of Industrial-Grade Implementation: TDD First, Code-as-Docs, and Embedded Observability.
source: auto-skill
extracted_at: '2026-06-06T16:00:00.000Z'
---

# PROTOCOL: Three Pillars of Implementation

## 🎯 Purpose
To transition from "vibe-based" coding to a deterministic engineering pipeline. This skill ensures that every feature is implemented with absolute traceability, testability, and observability.

## 🏛️ Pillar 1: TDD First (Test-Driven Development)
**The Law:** No implementation code may be written until a failing test exists that proves the feature is missing.

1. **Define the Test:** Based on the `tactical_plan.md` and `FR.md`, write a test case that fails.
2. **Execute & Verify Failure:** Run the test. It MUST fail. If it passes, the test is not probing the new functionality.
3. **Minimal Implementation:** Write the absolute minimum amount of code required to make the test pass.
4. **Refactor:** Optimize the code while keeping the test green.
5. **Repeat:** Move to the next atomic step in the tactical plan.

## 🏛️ Pillar 2: Code-as-Docs (AI-Native Contracts)
**The Law:** The code must be its own documentation. Instructional guides are replaced by executable contracts.

1. **Type Safety:** Every function signature must use strict type hinting.
2. **Contract Docstrings:** Every public method must have a docstring defining:
    - **Input:** What is the expected state/type?
    - **Output:** What is the guaranteed outcome?
    - **Invariants:** What must remain true?
3. **Deterministic Identification:** Use clear, descriptive naming that reflects the business intent (as defined in the `BR.md`), not the implementation detail.
4. **Verification:** Use `soviar impl audit-docs <slug>` (when available) to verify alignment.

## 🏛️ Pillar 3: Embedded Observability
**The Law:** A feature is not "done" until its internal state is transparent to the system.

1. **Deterministic Logging:** Implement structured logs at key decision points (not just errors).
2. **Health Hooks:** Add observability hooks (metrics/probes) that allow the system to verify the feature is working in production.
3. **Traceability:** Ensure logs include the feature slug or a correlation ID to trace requests back to the `Tactical Plan`.
4. **Verification:** Use `soviar impl check-obs <slug>` (when available) to verify hooks.

## 🚀 Implementation Workflow
For every task in the `tactical_plan.md`:

1. **TDD Cycle:** Write Test $\rightarrow$ Fail $\rightarrow$ Implement $\rightarrow$ Pass.
2. **Doc Cycle:** Update Docstrings/Contracts $\rightarrow$ Verify AI-readability.
3. **Obs Cycle:** Embed Logs/Probes $\rightarrow$ Verify transparency.
4. **Sign-off:** Once all pillars are satisfied for the task, mark it as complete in the `tactical_plan.md`.

## 🛡️ Guardrails
- **No "Quick Fixes":** Any change that bypasses TDD is considered a "corrupt state" and must be reverted.
- **No "Ghost Docs":** Do not write separate `.md` guides for how the code works; update the code's contracts instead.
- **Zero-Blind-Spots:** If a piece of logic cannot be observed via logs/metrics, it is not production-ready.
