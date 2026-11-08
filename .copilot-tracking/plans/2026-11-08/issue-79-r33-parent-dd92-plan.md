---
title: Issue 79 r33 plan
ms.date: 2026-11-08
---

* Commit research, plan and details first. Re-fetch main and the topic; require `b284d0d3` and `dd92e0d1` or stop with exact drift evidence.
* One normal `git merge --no-ff origin/feat/ranking-publication-runner-79`; no rebase, amend, reset, stash, cherry-pick or force. Stop on any conflict.
* Verify: parents, tree equals the incoming tree plus this loop's own RPI/log files only, dd92 and main ancestry, `git diff --check`.
* Light checks on the integrated source (own non-editable pinned venv, Core/runner/API wiring, ruff, mypy), then freeze clean and run one FULL gate; verify the receipt against current main. No push, PR edit, tick, approval.

## Critique (author, one pass, not independent)

* Risk: treating tree equality or old receipts as validation. Disposition: the gate runs on the final frozen head; old receipts stay historical.
* Risk: gate-time drift (main, lock). Disposition: refresh immediately before; if a holder appears freeze and report RESOURCE BLOCKED, never queue.
* Risk: RPI evidence written after the gate would invalidate the receipt. Disposition: write and commit all records, including changes/Review, before the gate; post-gate results go in the external receipt and the final report only.
* Disposition: proceed.
