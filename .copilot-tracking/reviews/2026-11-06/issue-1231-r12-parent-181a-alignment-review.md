# Author review: issue 1231 R12 alignment with parent 181a1c1bb

Date: 2026-11-06. Author review only, not an independent assessment.

Execution: Complete for the bounded local alignment. Outcome: Residual work.

Compared: R12 research, plan, critique, changes record, the merge diff and the focused check results (63 core tests, 17 API tests, Ruff 0.17.1, mypy 268 files, diff check).

## Findings

* RV-001 (Low, residual): a directory-sync failure after the link raises OSError with no audit entry although the record is committed. A retry reports it already published. Route: owner decision or later rpi-plan.
* RV-002 (Low, carried): store.py failed `ruff format --check` at r10; not touched here. Route: distinct follow-up.
* RV-003 (Medium, evidence gap): checks are source-bound with a shared read-only environment. No installed-package run, FULL gate, SQL, browser or real unsupported-mount evidence. EPERM injection is not a real mount. Route: coordinator FULL gate.
* RV-004 (Info): previous independent review items M1 (no fsync before link) and M2 (corrupt record at final name) are addressed by the parent's logic plus the child tests. Independent re-assessment of this exact head is still required.

Unchanged limits: simulated registries are not human approvals; r4, r7, r9 and r11 receipts are historical; topology 1231 -> 79 -> 73; no publication.
