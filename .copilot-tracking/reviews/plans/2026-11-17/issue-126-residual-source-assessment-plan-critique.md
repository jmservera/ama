<!-- markdownlint-disable-file -->
# Plan Critique: issue #126 residual and unassessed-check source assessment

* Date: 2026-11-17; one independent critique (rubber-duck agent, read-only); not repeated.
* Verdict: Revise
* Verified by critic: all 14 named test modules exist; HEAD/tree and PR #1812 ancestry correct; #1812 is not an ancestor of `origin/main`; tests not run by critic.

## Findings and Direct Dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Significant | Report roles are proposed; plan said accountable; unassessed role mappings are inferred. Label roles proposed/inferred, no accepted delegation. | Applied in phase details (role labelling). |
| PC-002 | Significant | A passing batch can include skips; source-tested claims must cite executed, passed tests. | Applied in phase details (test-evidence rule). |
| PC-003 | Significant | Inherited `ZF_*MSSQL` opt-ins, bytecode writes and tmp dirs. Use sanitised env, no bytecode, TMPDIR/ZF_DATA under evidence root. Note: `ZF_DATA`, `ZF_BIND`, `ZF_STATE`, `ZF_AI_GOLDEN` are inherited at launch and are cleared by `env -i`. | Applied in phase details (sanitised environment). |
| PC-004 | Minor | Separate task version, release version and EU applicability fields; do not substitute registry/PRD versions. | Applied in phase details (version fields). |
| PC-005 | Minor | Map internal tier names to requested vocabulary; observed/independently accepted listed as unavailable. | Applied in plan and phase details. |

No finding conflicts with a confirmed user decision; no significant or divergent issue requires a user decision.
