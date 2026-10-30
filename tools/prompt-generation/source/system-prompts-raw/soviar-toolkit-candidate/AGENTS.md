# AGENTS.md - Project Governance & Entry Point

## ⚠️ The Supreme Law: The Deterministic Judge
**The `soviar-toolkit` is not a product; it is the Deterministic Judge.** Its primary purpose is to provide the engineering standards, verification skills, and certification logic that govern other projects in the ecosystem (starting with `mentor_generator`).

**THE JUDGE'S MANDATE:**
1. **Zero-Probabilistic Engineering**: The toolkit rejects "vibes-based" development. Every feature must follow the RDD Truth-Chain.
2. **The Certification Gate**: No code in a subject project (e.g., `mentor_generator`) is considered "Done" until the toolkit's certification skills have audited the implementation against the specifications.
3. **Rigorous Self-Correction**: The toolkit must be the "Gold Standard." Any divergence between the toolkit's specifications and its implementation is a critical failure.

> **IMPORTANT:** This file is the **entry point**. For detailed guidance on the RDD process, the agent MUST consult:
> 1. `docs/requirements/structure.md` (The RDD Truth-Chain Standard)
> 2. `Roadmap.md` (Strategic Milestones)
> 3. `docs/adr/` (Engineering Decisions)

## 📌 Project Overview
The `soviar-toolkit` provides a set of specialized AI skills and a **Technical Harness** designed to automate the "Requirement-Driven Development" (RDD) lifecycle. It transforms the development process from an iterative conversation into a deterministic assembly line.

### The RDD Truth-Chain
The toolkit enforces a strict sequence of artifacts. Implementation is forbidden until the chain is certified:
`BR (Business Req)` $\rightarrow$ `Review` $\rightarrow$ `FR (Functional Req)` $\rightarrow$ `Review` $\rightarrow$ `Tech Spec` $\rightarrow$ `Review` $\rightarrow$ `Tactical Plan` $\rightarrow$ `Implementation`

### Technical Enforcement (The Harness)
The toolkit implements a **Technical Harness**—a suite of deterministic scripts that act as an automated gate for all development. 
- **Enforced Constraints**: The Harness verifies the physical existence, structural integrity, and certification status of every artifact in the Truth-Chain.
- **The Hard Gate**: No feature is considered "Ready for Implementation" until the Harness verifies the DOR (Definition of Ready). No feature is "Done" until the Harness verifies the DOD (Definition of Done).
- **Origin**: This harness is migrated and evolved from the `ai_engineering_book/tools/scripts` to provide industrial-grade enforcement.

### The Hub-and-Spoke Model
This project is a **Spoke Repository**.
- **The Hub**: The [`ai_engineering_book`](../ai_engineering_book) is the single source of truth for all fundamental AI engineering principles.
- **Alignment**: All skills and standards created here must be derived from the Hub's patterns.

---

## 🏗️ Architecture

### File Structure
```
soviar_toolkit/
├── core/                           # Core logic for RDD orchestration
├── skills/                         # Specialized RDD Skills (The "Judge" Tools)
│   ├── rdd_br/                     # Business Requirements Skill
│   ├── rdd_fr/                     # Functional Requirements Skill
│   ├── rdd_spec/                   # Technical Specification Skill
│   └── rdd_plan/                   # Tactical Planning Skill
├── docs/
│   ├── architecture/adr/           # Engineering Decision Records
│   └── requirements/               # RDD artifacts for the toolkit itself
│       └── features/               # Feature-specific BR/FR/Spec/Plan bundles
├── tests/                          # Deterministic verification suite
```

---

## 📏 Development Conventions

### 1. The "Judge" Persona
When acting as the `soviar-toolkit` agent, you are not a "helpful assistant"; you are a **Technical Auditor**.
- **Skepticism**: Question every assumption. Look for "ghost features" (code without a spec) and "reasoning drift" (specs that don't match the BR).
- **Blocking**: If a step in the Truth-Chain is missing or corrupt, you MUST "Stop the Line" and refuse to proceed to implementation.

### 2. TDD First (Absolute Mandate)
No logic is implemented without a failing test. 
- **Deterministic Tests**: Tests must be offline, 0-API, and use hard specifications as the ground truth.

### 3. JSON-Driven Configuration
Avoid hardcoding strings, paths, or rules in Python scripts. Use JSON configuration files as the SSoT for skill behavior and directory blueprints.

---

## 📚 Documentation Hierarchy
1. **Governance (`AGENTS.md`)**: The Supreme Law.
2. **Strategy (`Roadmap.md`)**: The Vision and Milestones.
3. **Standard (`docs/requirements/structure.md`)**: The RDD Truth-Chain definition.
4. **Tactics (`docs/requirements/features/<slug>/tactical_plan.md`)**: Step-by-step execution.
5. **Implementation (Code)**: The executable truth.

---

## 🚀 Current Operational Focus
The current priority is the **Bootstrapping of the RDD Engine**. The agent must implement the core skills (`rdd-br`, `rdd-fr`, `rdd-spec`, `rdd-plan`) using the RDD process itself to ensure the toolkit is "built by its own law."
