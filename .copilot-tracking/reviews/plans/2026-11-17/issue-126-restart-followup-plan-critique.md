<!-- markdownlint-disable-file -->
# Plan Critique: issue #126 restart follow-up

* Date: 2026-11-17; one independent critique (rubber-duck agent, read-only, no tests run); not repeated.
* Verdict: Revise
* Verified by critic: six modules exist under `src/core/tests/`; the same-named orchestrator `test_source_monitor` is a different module; the documented command shape is compatible; the MN-3.2 vs GOVERN-AUDIT-02 distinction is supported when framed as missing retirement-detection test evidence alongside absent human review.

## Findings and Direct Dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Significant | "No SQL" in the brief conflicts with local SQLite cases inside the six modules (for example `test_source_monitor.py:260`). Asked for clarification. | Resolved without re-asking: the brief excludes heavy SQL (SQL Server opt-ins, no `ZF_*MSSQL*`); stdlib SQLite and JSON local doubles are part of the named modules and run. Results are labelled "local SQLite double, not SQL Server evidence"; skipped SQL Server classes are unproven, not pass. Applied in details P03-T02. |
| PC-002 | Significant | Verifier scheduled before the section it must verify; hashing the table and embedding the verifier-output hash inside the same table is circular. | Applied: order becomes add the table section first, then run the verifier, then record script/output/table hashes only in the external evidence and the changes record (not inside the hashed table); the table section cites the verifier by external path and script SHA-256 only. |
| PC-003 | Significant | Table uses `core/` and `agents/` aliases; direct `git rev-parse <commit>:<path>` fails. | Applied: the verifier resolves `core/` to `src/core/src/zava_forward/core/` and `agents/` to `src/agents/src/zava_forward/agents/` (mapping stated at table line 43) before path, line and blob checks. |
| PC-004 | Minor | The original inline verifier was never retained, so a new helper cannot be the exact original. | Applied: the helper is labelled a reconstructed verifier; its counts are distinguished from the parent's historical inline counts (69/44/38/27) and are not represented as the original run. |

## Compatible advice not conflicting with confirmed decisions

All four applied or resolved directly; no significant or divergent issue needed a user decision.
