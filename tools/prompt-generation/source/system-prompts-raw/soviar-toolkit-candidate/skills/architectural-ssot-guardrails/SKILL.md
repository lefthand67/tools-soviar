---
name: architectural-ssot-guardrails
description: Methodology for maintaining architectural integrity by strictly adhering to the Source of Truth (SSoT) hierarchy.
source: auto-skill
extracted_at: '2026-05-30T23:31:02.854Z'
---

# Architectural SSoT Guardrails

In complex, agent-driven projects, "Reasoning Drift" occurs when agents rely on summary documentation rather than formal specifications. To prevent this, implement a strict **Source of Truth (SSoT) Hierarchy**.

## 1. The SSoT Hierarchy
When conflicting information is found across project files, follow this priority order:
1. **The Executable Truth (Code):** What the system actually does.
2. **The Formal Specification (ADRs):** The "Why" and "What" of the architectural decision.
3. **The Strategy (Roadmap):** The sequence and vision of implementation.
4. **The Tactical Blueprint (Plans):** The a-priori "How."
5. **The Governance Summary (e.g., AGENTS.md, README):** A mirror/summary of the above.

## 2. The "Mirror" Trap
Summary documents (like `AGENTS.md` or `README.md`) are designed for quick onboarding. They are **mirrors**, not sources. 
- **The Risk:** Mirrors can become "blurry" or outdated. If an agent treats a mirror as the SSoT, they will propagate architectural drift by modifying other files to match an outdated summary.
- **The Guardrail:** Never use a summary document to justify a structural change. Always trace the requirement back to an ADR or the Roadmap.

## 3. Validation Loop
Before executing a structural change:
1. **Identify the target change.**
2. **Search for the corresponding ADR.**
3. **Verify the Roadmap state.**
4. **Cross-reference with the Code.**
5. **Update the Summary (Mirror) LAST**, only after the change is verified against the formal SSoT.

This prevents "Hallucinated Architecture" where the agent modifies the system based on its own misunderstanding of a summary file.
