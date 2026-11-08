# Author review: issue 1231 R13 alignment

Date: 2026-11-07. Author review only, not independent assessment. Execution: Complete. Outcome: Residual work.

Compared: research, plan, changes record, merge tree and focused check results.

* RV-001 (Medium, evidence gap): no FULL tip gate on this head; required after #891 and main settle, with --stack 11fb73f45 --stack tip. Route: coordinator.
* RV-002 (Low): history is a merge, not a rebase, because the rebase needed invented intermediate resolutions. The old declared parent 181a1c1bb stays in ancestry; the squash/PR diff against 11fb73f45 is child-only. Route: coordinator decision on whether to keep the merge shape.
* RV-003 (Low, carried): directory-sync failure after link has no audit entry (R12 RV-001); store.py format finding from r10 (now passes the format check on src/api).
* RV-004 (Info): no critique was run (no source decision); independent parent and child exact-head review is still required. Simulated registries are not human approvals; hard-link EPERM injection is not a real unsupported mount.
