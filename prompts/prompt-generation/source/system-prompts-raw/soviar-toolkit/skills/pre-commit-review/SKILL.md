---
name: pre-commit-review
description: Use before committing code or changes to review staged changes and supporting context.
---

# Pre-Commit Review

Automates a rigorous, multi-angle subagent-driven review of staged changes and supporting context before committing.

## Execution Workflow

1. **Pre-Flight Checks**
   - Check `git diff --cached`. If empty, inspect unstaged changes and prompt for atomic staging.
   - Check diff volume; warn on huge monolithic commits and require explicit confirmation.

2. **File Initialization**
   - Determine timestamp and slug (format: `docs/review/<datetime>_<slug>/`, e.g. `docs/review/20261003_194935_pre_commit_review/`).
   - Create review directory `docs/review/<datetime>_<slug>/`.
   - Initialize session report files via Bash:
     `cp skills/pre-commit-review/templates/finding_report.md docs/review/<datetime>_<slug>/{missed,misinterpreted,lost}.md`
     `cp skills/pre-commit-review/templates/final_report.md docs/review/<datetime>_<slug>/final_report.md`

3. **Sequential Pipeline (Blocking & Retry-Resilient & Trace-Enforced & Research-Driven)**
   - **Deep Context Research**: Subagents are explicitly instructed to perform active, unrestricted research across the entire codebase, documentation, specifications, and git history to discover all related context. Reviews are treated as deep investigations rather than mechanical checklist checks.
   - **Step-by-step sequential execution**: Each agent MUST completely finish and write its findings (or explicit "Zero findings" trace) directly into its assigned report file (`docs/review/<datetime>_<slug>/missed.md`, `misinterpreted.md`, `lost.md`) before the next agent starts.
   - **Orchestrator Trace Verification**: After each subagent finishes, the orchestrator MUST verify that the report file has been modified from the raw template and contains the agent's trace. If the file remains an unmodified template, it is treated as a failed subagent execution and automatically retried.
   - **MISSED:** Read `skills/pre-commit-review/prompts/missed_prompt.md`, perform deep context research across the repository and staged diff (`git diff --cached`), and verify that findings/trace are written to `docs/review/<datetime>_<slug>/missed.md`.
   - **MISINTERPRETED:** Read `skills/pre-commit-review/prompts/misinterpreted_prompt.md`, investigate logic errors and deviations against full repository context, and verify that findings/trace are written to `docs/review/<datetime>_<slug>/misinterpreted.md`.
   - **LOST:** Read `skills/pre-commit-review/prompts/lost_prompt.md`, investigate accidental deletions or missing components across git history and repository, and verify that findings/trace are written to `docs/review/<datetime>_<slug>/lost.md`.
   - **V1 Groundness:** Read `skills/pre-commit-review/prompts/v1_prompt.md`, audit findings from all three reports against codebase and context, appending groundness audit notes under each finding in the respective files.
   - **V2 Senior Decision:** Read `skills/pre-commit-review/prompts/v2_prompt.md`, synthesize validated findings with architectural awareness, determine dispositions (Apply/Drop), and verify that `docs/review/<datetime>_<slug>/final_report.md` is fully populated.

4. **Reporting**
   - Present the final V2 decision report and findings to the user.







