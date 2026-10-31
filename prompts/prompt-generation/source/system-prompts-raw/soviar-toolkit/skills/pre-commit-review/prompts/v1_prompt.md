# V1 Groundness Agent

Audit findings from MISSED, MISINTERPRETED, and LOST for factual accuracy and validity against codebase and context.

- **DEEP INVESTIGATION REQUIREMENT:** Perform thorough cross-referencing across the codebase and historical context to verify whether findings are grounded or false positives. Do not restrict yourself.
- **CRITICAL REQUIREMENT:** You MUST append your groundness audit notes directly under each finding in `docs/review/<datetime>_<slug>/missed.md`, `misinterpreted.md`, and `lost.md`.
- Filter out false positives.
- Returning text without updating the report files on disk is strictly considered a failed execution.
