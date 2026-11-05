---
title: Research for #188 current-main preparation
ms.date: 2026-11-05
---

* Research disposition: executed (read-only git inspection, no network). Planning Readiness: Ready.
* Inputs read: #188 state and artifacts of live-sim-ingest, live-sim-roundtrip and live-sim-handover (originals and adverse outcomes unchanged), case study original and addendum, KB index and memory, component guides, retention policy.
* Pins: child head 834e2becfba6fe1135e0e18ccd08f4faa43fc880, tree 9c3a4c9847a06fcc52987cda991e43789de09e95; fetched origin/main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f; parent feat/live-simulator-integration-184 ead177ef90d24666557708ea344848a1be43bdf8 (also the merge base). PR 1203 public head c9a14573d is older than the local source; its published contexts do not validate this head.
* Main delta: 6 commits, 55 files. Code: `src/api/.../web/style.css` (one nav rule), `tools/rpi-checks.py` and `tools/test_rpi_checks.py`, `tools/backlog-sync.py` and test, `.github/workflows/src-ci.yml`, `src/README.md`, rubric score; plus tracking records. No sensor, consumer, handover, ingestion, SQL or consent file changed.
* Overlap: none between the main delta and the child's changed files. `git merge-tree` predicts a clean ordinary merge.
* Distinction kept: weather live-sim rows are not indoor measurements. The unsupported-handover refusal, lossless `retained_envelopes` and indoor `observed_series` exclusion are the behaviors to re-prove after the merge.
* Environment finding: installed zava-forward distributions resolve to the other checkout /home/azureuser/source/ama, not this worktree, so checks need explicit worktree source paths (not mvp) and an import-path proof.
* Unknown: nothing run against SQL Server or Azure. Weather-to-weather scope question is already pending; not re-asked. C2 continuity remains unproven.
