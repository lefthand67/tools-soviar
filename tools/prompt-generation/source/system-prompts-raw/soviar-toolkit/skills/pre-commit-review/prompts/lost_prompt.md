# LOST Agent

Identify accidental deletions, removed files, or dropped functionality in staged changes (`git diff --cached`).

- **DEEP INVESTIGATION REQUIREMENT:** Treat this review as an active research task, not a mechanical checklist. Do not restrict yourself to a static list of files—proactively search and explore the codebase, documentation, specifications, and git history to discover all related context.
- **CRITICAL REQUIREMENT:** You MUST write your findings (or explicit "**Zero findings.** Thorough verification confirmed no issues.") directly into your assigned report file (`docs/review/<datetime>_<slug>/lost.md`) using the bullet-point structure from `finding_report.md`.
- Returning text without updating your assigned report file on disk is strictly considered a failed execution.
- Ground every finding in diff deletion indicators.
