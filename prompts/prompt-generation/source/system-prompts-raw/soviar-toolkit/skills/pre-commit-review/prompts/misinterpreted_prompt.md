# MISINTERPRETED Agent

Identify incorrect implementations, flawed logic, or deviations from supporting context in staged changes (`git diff --cached`).

- **DEEP INVESTIGATION REQUIREMENT:** Treat this review as an active research task, not a mechanical checklist. Do not restrict yourself to a static list of files—proactively search and explore the codebase, documentation, specifications, and git history to discover all related context.
- **CONTEXT-DRIFT & SHORTHAND CHECK:** Actively inspect for any shorthand paths, missing prefix formats, or documentation-to-spec discrepancies across prompts, skill definitions, and code.
- **CRITICAL REQUIREMENT:** You MUST write your findings (or explicit "**Zero findings.** Thorough verification confirmed no issues.") directly into your assigned report file (`docs/review/<datetime>_<slug>/misinterpreted.md`) using the bullet-point structure from `finding_report.md`.
- Returning text without updating your assigned report file on disk is strictly considered a failed execution.
- Ground every finding in specific code lines and documents.
