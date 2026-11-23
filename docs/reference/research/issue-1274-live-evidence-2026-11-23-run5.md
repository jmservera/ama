---
title: Resilient verified official release downloads, workflow wiring regression (#1274)
description: New tools test pinning the Source CI actionlint bootstrap to the verified installer, with the per-criterion table for issue 1274
ms.date: 2026-11-23
---

## Scope

Synthetic demo, desktop only. CI-only issue: no Azure resource touched, no credential read. Only `tools/test_install_actionlint.py` changed (no `src/`), so the focused tier applies. Run 4 ([note](./issue-1274-live-evidence-2026-11-23-run4.md)) holds the retained job-log lines and the live actionlint checksum verification.

## Observations

* New `WorkflowWiringTests` (2 tests) assert that `src-ci.yml` runs `python3 tools/install-actionlint.py "$RUNNER_TEMP/actionlint-bin"`, that the version check string equals the installer `VERSION` (1.7.7), and that no curl or wget line in a native (non-`.lock.yml`) workflow fetches `releases/download` directly.
* `python3 -m unittest tools.test_install_actionlint`: 14 tests OK. `ruff check`, `ruff format --check` and `mypy --strict` on the two installer files: clean.
* The axe download in `src-ci.yml` is a CDN fetch with `--retry 5` and a pinned SHA-256, not a release download.

## Per-criterion table

| Criterion | Verdict |
| --- | --- |
| 1 failing endpoints | Proven for actionlint (run 4); unproven for AWF checksums.txt and #1273 (logs not retained) |
| 2 bounded fail-closed retrieval | Proven (installer tests) |
| 3 focused regressions | Proven (14 tests OK) |
| 4 real checksum verification, exact-head hosted CI | Actionlint 1.7.7 verified in run 4; AWF 0.28.23 and hosted CI on the reviewed head unproven (no push, owner-gated) |
| 5 resume route | Proven (merged #1275) |
