---
title: Issue 531 residual scope re-verification
ms.date: 2026-11-02
---

* Research disposition: executed (read-only repository and issue review).
* Planning Readiness: Ready.
* Evidence: PRs #538, #604, #628, #685, #725 are merged on main (071e132a8). Acceptance criteria 1 to 6 are ticked in the issue. The only unmet criterion is 7, live verification on the employee site.
* Criterion 7 needs an operator-signed-in Chromium attached by `checks/employee_live_acceptance.py` with `ZF_EXPECTED_TID` and `ZF_EXPECTED_OID`. No agent session can sign in interactively. The owner forbade a new live Azure tick, so it stays owner-run.
* Local main drift check: startup shell (`workspace-shell.js`), per-panel feedback, outcome-wording briefing review, sources and unverified labelling are present in `src/api/src/zava_forward/api/web/`.
* Environment note: pip-installed zava-forward distributions resolve to another worktree (issue-184), so validation used explicit `PYTHONPATH` to this worktree.
