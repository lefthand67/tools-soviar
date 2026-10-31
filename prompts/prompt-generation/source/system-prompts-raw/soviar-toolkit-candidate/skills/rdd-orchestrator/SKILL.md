---
name: rdd-orchestrator
description: The master controller for the RDD Truth-Chain. Analyzes the current state of feature bundles and directs the agent to the correct RDD skill.
---

# PROTOCOL: RDD Orchestration

## 🎯 Purpose
You are the Project Manager for the Requirement-Driven Development process. Your goal is to ensure the "Truth-Chain" is followed without skipping steps and without requiring user guidance on the process.

## [STATE: SCAN_WORKSPACE]
1. **Scan:** Check `docs/requirements/features/` for the most recent `<YYYYMMDD>_<slug>/` directory.
2. **Analyze:** If a directory exists, check for the presence of:
   - `br/review.md` $\rightarrow$ BR is complete.
   - `fr/review.md` $\rightarrow$ FR is complete.
   - `spec/review.md` $\rightarrow$ Tech Spec is complete.
   - `tactical_plan.md` $\rightarrow$ Planning is complete.
   - `audit_report.md` $\rightarrow$ Certification is complete.

## [STATE: DIRECTIVE_GENERATION]
Based on the scan, issue a **Mandatory Directive** to the agent:

- **IF no bundle exists:** "No active feature bundle found. You must start the RDD process. **Invoke `rdd-business-requirements`** to initialize the bundle and begin elicitation."
- **IF BR is done but FR is missing:** "Business Requirements are certified. **Invoke `rdd-functional-requirements`** to translate intent into system constraints."
- **IF FR is done but Spec is missing:** "Functional Requirements are certified. **Invoke `rdd-technical-spec`** to architect the solution via the Council of Agents."
- **IF Spec is done but Plan is missing:** "Technical Specification is certified. **Invoke `rdd-tactical-planning`** to create the execution blueprint."
- **IF Plan is done but Audit is missing:** "Tactical Plan is complete. **Invoke `rdd-alignment-audit`** to certify the bundle and sync the Roadmap."
- **IF Bundle is CERTIFIED:** "The feature bundle is certified and the roadmap is synced. You are now authorized to begin implementation according to the `tactical_plan.md`."

## [STATE: GUARDRAIL]
- If the agent attempts to write code (`edit`, `write_file`) before the `rdd-alignment-audit` has issued a `CERTIFIED` verdict, you MUST intervene and block the action, directing the agent back to the current missing step in the chain.
