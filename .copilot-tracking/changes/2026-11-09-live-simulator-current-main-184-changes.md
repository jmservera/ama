---
title: "#184 current-main validation changes"
ms.date: 2026-11-09
---

Implementation record for the plan and details of the same slug. No product source, test or setup was edited in this pass; the only repository change besides these records is the ordinary merge commit.

## Identity

* Start HEAD e0bb2bc0a06d9b7bf3b431bdd54d80c5670986bf, tree a6349582852b9583d182c76508a09cd287fd3ea0.
* Merge commit 60707c555a654a8d97830ef68b8122d585cf948e, tree 3b8567e0ae2c271b1716b824d118f1bd5b73052a (equals the predicted `merge-tree` tree), parents e0bb2bc0a and fetched origin/main 1f28d09130c8e058a0436d468e6a22f3c4c24f47 (re-verified immediately before merge). Ordinary `git merge --no-ff`; no rebase, no force, no conflict; reviewed IoT source and owner ancestry preserved.
* Records were written before the merge; the commit that follows adds them (frozen head is stated in the handoff).

## Equivalence proof (logs in /home/azureuser/logs-184-cm)

* 28 of 31 parent-changed non-tracking paths have identical blob ids at e0bb2bc0a and at the merged head; the three differences are docs/reference/README.md, docs/reference/log.md and src/core/README.md (main text merged alongside the parent's additions).
* Source/infra/tool/workflow delta e0bb2bc0a to merged head: src/core/README.md, src/core/src/zava_forward/core/paired_equity.py, src/core/tests/test_paired_equity.py only (src-delta.txt). No infra, tools, dependency manifest, workflow or Dockerfile change.
* Importing every parent-changed IoT module and `sensor_sql_check`: paired_equity not loaded (import-closure.txt). Grep finds paired_equity only in its test and README.

## Checks at merged head (demo-targeted tier; no rpi-checks --all/--changed, no receipt)

| Check | Result |
| --- | --- |
| core test_paired_equity (new main tests) | 23 OK, exit 0 |
| core test_live_doc_links (scans changed README) | 2 OK, exit 0 |
| core ruff check, ruff format --check, mypy (273 files) | pass, exit 0 |
| core sensor* (earlier run, 192; PYTHONPATH not needed) | 192 OK, 11 offline opt-in skips |
| core device 48, live 22, resident_sensors 10, historical_backfill 10 | OK, exit 0 |
| api live* 66 (2 skips need owned SQL), iot* 49, sensor* 103 (PYTHONPATH=../core/tests:../agents/tests) | OK, exit 0 |
| api mypy --no-incremental --cache-dir=/dev/null, ruff check | 0 errors in 199 files, pass |
| tools test_rpi_checks | 102 OK |
| Owned disposable SQL default selector (nonqueued `flock -n`, first attempt not busy) | 70 tests OK, zero skips, exit 0 |
| Owned disposable SQL analysis selector | 10 tests OK, zero skips, "accepted", exit 0 |

* An initial api run without PYTHONPATH failed to import fixture modules (harness path, not code); rerun with the documented path passed. Recorded, not hidden.
* SQL was rerun, not reused (critique 1, 2): image sha256:cf8f0ab2ebe6...1718, pip freeze hash 51c6a4d9e8e0..., tools ruff 0.17.1 / mypy 2.4.0, playwright 1.64.0, container removed, no other session resources touched. SQL meta and logs: sql-default.{meta,log}, sql-analysis.{meta,log}.
* Not rerun, unchanged inputs by blob id: infra unit tests and offline Bicep build/lint (no infra, tool or Bicep blob changed; evidence at e0bb2bc0a stays historical for those). Browser: no web change. Hosted CI and independent exact-head review pending.

## Carried items

* Low (exact-grant live_receiver.main, rejected data-quality under receiver grants, replay coverage): OPEN, unchanged; `test_live_receiver_sql.py` unchanged. This pass does not claim it closed.
* Original 53 errors in 48 files mypy record retained; explained by missing declared playwright, fixed in isolated venv, not waived.
* F1 flake (send-rate test): passed here (iot* 49 OK); a separate flake draft remains a follow-up.
* Correction counts unchanged; no correction made.
