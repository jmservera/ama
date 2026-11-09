---
title: Issue 86 light propagation of local parent e888a49 changes
description: Changes record for one normal merge and light checks (Refs #86)
ms.date: 2026-11-08
---

LIGHT propagation only; not FULL, not publication.

* Start `43c9f466`; records commit `fbae3cbfc83b8ee7eb779973f0b19e3f719c0b78` (first parent, sole parent `43c9f466`); one normal merge `63c169ac0b6cae951edae2c795cb0a530e5dc0e3`, tree `0b998890…`, parents `fbae3cbf…` and `e888a499…` (local fetched object, parent worktree untouched, clean). `origin/main` `f548b65f…` is in the parent. No rebase or force; PR 1243 target unchanged.
* Merge delta from first parent: 366 paths (350 additions, 16 modifications), no mode change. Auto-merged overlap: `src/core/README.md` and `src/core/.../store.py`; result keeps the child `complaints_receiver` declaration and the parent ranking-archive hunks (`stage_retained` present).
* Proofs: every non-overlap incoming path equals the parent's blob/mode; `complaints_route.py`, `resident_decisions.py`, `test_resident_decisions.py` equal the child's; rubric JSON parses and blob/mode equal the parent's; child's existing `docs/reference/log.md` lines preserved in order with parent entries added; no prior `.copilot-tracking` file removed or changed.
* Critique: one independent (Revise, 3 blocking); dispositions in `challenges/2026-11-08/issue-86-parente888-light-critique.md` (one rejected with reason, four accepted and applied before the merge).

## Light checks (scratch `/home/azureuser/.local/share/ama/gates/g86-e888-light-1108`; non-editable own-source venv; origins prove venv copies of the archive source; `.out/.err/.exit` kept)

* core `test_resident_decisions`: exit 0, 308 tests, 110 skipped.
* core `test_ranking_publication` and `_runner`: exit 0, 76 tests.
* core strict mypy: exit 0, 269 files.
* ruff check `.` and format `--check .`: exit 1 (`ruff.*`, `fmt.*`, retained): the scan included the `build/` directory created by my own pip install in the scratch archive, not repo source. Rerun on `src tests`: exit 0 both (`ruff2`, `fmt2`).
* API selected modules (`api.*`): exit 1 with 95 tests, 1 skipped, 1 error: `test_workbench_live_defaults` could not import `playwright` (real missing dependency; logged 503/ValueError traces are expected test output). After `pip install playwright==1.64.0` (no browsers), `ManifestDefaultsMatchApi` exit 0, 3 tests (`api2.*`). The Chromium class was not run.
* Not run: SQL, Chromium, FULL, scanner, images, 60,000-case benchmark, model, Azure.

Pending: fresh child-stack FULL on current main and exact head, independent exact-head assessment, hosted checks, named human approvals, real receiver acknowledgement. Original Medium findings, adverse browser outcome and 1238 remain open.
