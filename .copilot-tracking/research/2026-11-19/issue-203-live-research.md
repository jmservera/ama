---
title: Issue 203 live research (third run)
ms.date: 2026-11-19
---

Refs #203. Synthetic demo, desktop only, resource group `ama`. Research disposition: executed. Planning Readiness: Ready.

Unticked criteria: (1) repository search for `mvp/` and `prototype/`; (5) deployed app and CI green from `src/`.

Findings from reading the repository:

* `tools/check-legacy-references.py` and `tools/test_check_legacy_references.py` already exist and encode criterion 1. The previous run (2026-11-18) recorded 20 violations; the working head `3e5371eb0` now reports 0.
* Prior criterion 5 note: running digest not provably built from `src/`, no `src-deploy.yml` runs, no push CI on `main`.
* Code candidate: none. The checker exists and passes; changing it alters gate semantics (full tier) and no defect was found. Outcome is an evidence note only.
