<!-- markdownlint-disable-file -->
# Review: Epic 165 IoT, cohort and scenario join parity (2026-11-14)

Execution: executed once. Outcome: conformant with caveats. Boundary: the new test file only.

## Findings

* No blocking findings. Test-only; no production code changed; plan, details and changes agree.
* Caveat: no committed stock-to-case link exists, so the manifest's unpadded fixture case ids (`ZF-4`) and generated ids (`ZF-00004`) are asserted disjoint, not joined. Property-register ids (`SYN-PROP-*`) are likewise a separate namespace; the test claims no EPC or PAS 2035 compliance.
* Caveat: the installed editable `zava_forward.core` points at another checkout, so tests need `PYTHONPATH=src:tests`.
* Independent exact-head review, human approval and hosted CI remain outstanding; unchecked.

## Follow-ups

1. Add a committed stock-to-case link, then upgrade the disjointness assertion to a join.
2. Fix the dev environment so editable installs resolve to the active worktree.
