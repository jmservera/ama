---
title: Issue 202 live r2 research, 2026-11-19
---

Research disposition: executed (re-verification of the 2026-11-18 audit). Planning Readiness: Ready.

Only one criterion is unticked: old workflows removed or replaced and required checks updated.

* `mvp/` and `prototype/` have 0 tracked files; tag `v0.21.0` is on origin; no release exists.
* `mvp-ci.yml` and `mvp-validation.yml` are `disabled_manually`; `src-ci.yml` is active.
* Ruleset `mainprotect` requires no status checks; ruleset `main` is disabled; no classic protection.
* 43 live references remain (inventory in the evidence dir): `tools/rpi-checks.py` pins both files by SHA-256 and maps job names, `src-ci.yml` actionlint list and path filters, `infra/tests/test_pipeline.py`, `tools/test_src_cutover_repoint.py`, `src/core` cutover audit and tests, docs.
* Removal edits gate tooling and `src/core` code, so FULL tier applies; `rpi-checks.py --all` is barred for this worker.

Evidence: docs/reference/research/issue-202-live-20261119T1540Z-evidence/
