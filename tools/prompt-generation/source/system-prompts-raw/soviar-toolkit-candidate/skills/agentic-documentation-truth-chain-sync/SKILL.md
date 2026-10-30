---
name: agentic-documentation-truth-chain-sync
description: Process for synchronizing project documentation across the "Truth-Chain" to prevent cognitive dissonance and reasoning drift in AI agents.
source: auto-skill
extracted_at: '2026-06-01T10:05:00.000Z'
---

# Agentic Documentation Truth-Chain Synchronization

When working with AI agents (especially those with long-term memory or those being replaced/restarted), a discrepancy between high-level entry points (e.g., `README.md`) and detailed specifications (e.g., `ADRs`) causes **Cognitive Dissonance**. The agent may ignore new architectural mandates or hallucinate a compromise between conflicting sources.

## 1. The Truth-Chain Hierarchy

Documentation must be treated as a layered system where each level serves a specific cognitive function for the agent:

| Level | Artifact | Cognitive Function | Typical Content |
| :--- | :--- | :--- | :--- |
| **Entry Point** | `AGENTS.md` / `README.md` | **Identity & Governance** | "What is this project?", "What are the supreme laws?", "How do I start?" |
| **Strategy** | `Roadmap.md` | **Vision & Sequence** | "Why are we doing this?", "What is the current phase?", "What is the North Star?" |
| **Tactics** | `misc/plan/*.md` | **Operational Blueprint** | "How exactly is this feature implemented?", "What are the success criteria?" |
| **Mandates** | `docs/architecture/adr/*.md` | **Authoritative Law** | "What is the final decision?", "What are the constraints?", "What is forbidden?" |
| **Implementation** | Code / Docstrings | **Executable Truth** | "How does it actually work in bytes?" |

---
name: agentic-documentation-truth-chain-sync
description: Process for synchronizing project documentation across the "Truth-Chain" to prevent cognitive dissonance and reasoning drift in AI agents.
source: auto-skill
extracted_at: '2026-06-01T10:05:00.000Z'
---

# Agentic Documentation Truth-Chain Synchronization

When working with AI agents (especially those with long-term memory or those being replaced/restarted), a discrepancy between high-level entry points (e.g., `README.md`) and detailed specifications (e.g., `ADRs`) causes **Cognitive Dissonance**. The agent may ignore new architectural mandates or hallucinate a compromise between conflicting sources.

## 1. The Truth-Chain Hierarchy

Documentation must be treated as a layered system where each level serves a specific cognitive function for the agent:

| Level | Artifact | Cognitive Function | Typical Content |
| :--- | :--- | :--- | :--- |
| **Entry Point** | `AGENTS.md` / `README.md` | **Identity & Governance** | "What is this project?", "What are the supreme laws?", "How do I start?" |
| **Strategy** | `Roadmap.md` | **Vision & Sequence** | "Why are we doing this?", "What is the current phase?", "What is the North Star?" |
| **Tactics** | `misc/plan/*.md` | **Operational Blueprint** | "How exactly is this feature implemented?", "What are the success criteria?" |
| **Mandates** | `docs/architecture/adr/*.md` | **Authoritative Law** | "What is the final decision?", "What are the constraints?", "What is forbidden?" |
| **Implementation** | Code / Docstrings | **Executable Truth** | "How does it actually work in bytes?" |

## 2. The Synchronization Process (Anti-Drift)

### A. Downstream Synchronization (Decision $\rightarrow$ Code)
Whenever a strategic shift occurs (e.g., a new ADR is accepted), the agent MUST NOT stop at the ADR. It must perform a **Downstream Synchronization** across the entire chain:

1. **Codify the Decision**: Write the ADR (The Law).
2. **Update the Vision**: Reflect the decision in the `Roadmap.md` (The Strategy).
3. **Align the Entry Point**: Update `AGENTS.md` and `README.md` to reflect the new identity/architecture (The Governance).
4. **Refine the Technical Map**: Update `system_blueprint.md` or other architectural maps.
5. **Symmetrize the Code**: Update module docstrings and variable names to match the new terminology (The Implementation).

### B. Bottom-Up Verification (Code $\rightarrow$ Strategy)
To prevent **Roadmap Optimism** (where strategy docs are updated to reflect *intended* state rather than *actual* state), the agent should perform periodic **Reality Audits**:

1. **Plan Review**: Identify plans marked as "COMPLETED" or "implemented" in the roadmap.
2. **Empirical Verification**: Instead of trusting the status, use a verification loop (e.g., subagents) to cross-reference the Plan's **Success Criteria** against the actual **Implementation** (Code/Tests).
3. **Gap Analysis**: If the audit fails, identify the "Implementation Gap" (specific missing components or shallow tests).
4. **Restore Truth-Chain**: Downgrade the Roadmap status to "IN PROGRESS," keep the tactical plans active, and prioritize the missing gaps.

## 3. Identifying "Cognitive Dissonance"

Signs that the Truth-Chain is broken:
- The agent suggests a solution that contradicts a recently accepted ADR.
- The agent refers to the project by an old name or old architectural paradigm (e.g., calling an "App Platform" a "CLI Tool").
- The agent implements a feature using a deprecated pattern described in the README but forbidden in the ADRs.
- The Roadmap claims a phase is "COMPLETED," but the corresponding core logic is missing from the codebase.

## 4. Implementation Mandate: The "Symmetry Rule"
**The code is the territory, but the documentation is the map.**

If the map changes, the territory must be updated. If the territory is updated, the map must be revised. Any gap between the two is defined as **Reasoning Drift** and must be corrected immediately as a high-priority bug.


## 4. Implementation Mandate: The "Symmetry Rule"
**The code is the territory, but the documentation is the map.** 

If the map changes, the territory must be updated. If the territory is updated, the map must be revised. Any gap between the two is defined as **Reasoning Drift** and must be corrected immediately as a high-priority bug.
