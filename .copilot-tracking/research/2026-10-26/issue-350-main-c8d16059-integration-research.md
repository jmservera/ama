<!-- markdownlint-disable-file -->
---
title: Issue 350 main c8d16059 integration research
description: Read-only lifecycle, conflict prediction and residual evidence recorded before plan, critique and merge
ms.date: 2026-10-26
---

Written 2026-10-26 from about 07:15Z, before any plan, critique or merge in this continuation. No file had been edited when it was written.

Lifecycle (fresh fetch):

* Local HEAD `49851214922ba7f7c143ddcb435c396b2040cd89`, remote branch `a9bdae317489b873f9e1ffc58a81d32282f39cb0` (an ancestor of HEAD, so local is 4 commits ahead). Branch `test/deployed-feedback-harness-350`, tree clean, no ignored files.
* `origin/main` is `c8d16059c0c0a22c4ffba88c6b65ac068f64accc` and is **not** an ancestor. Merge base `ea5577b2`; main is one commit ahead: #455 (synthetic read-only resident feedback preview, issue 444).
* Main-only files: new issue444 `.copilot-tracking` records, `.github/rubric/scores/latest.json`, `src/api/README.md`, `src/api/pyproject.toml`, new `resident_preview` modules, checks and tests in `src/api` and `src/core`, and `src/core/README.md`.
* Branch-owned changes since the merge base: only `tools/check-demo-feedback.py`, `tools/test_check_demo_feedback.py` and issue-350 `.copilot-tracking` records. Main does not touch `tools/`. `git merge-tree` predicts a clean merge (exit 0, no conflict list).
* Disk: 6.8 GB free (22 GB in the previous continuation). That is a material reduction; no new environment or gate is started.

Residual work from the coordinator's whole-content assessment (20:34Z), recorded as data: no new High or Medium functional defect after the RecursionError and Application Administrator fixes; one Medium fixture-provenance concern RV-001 (contact and AI evidence assembled by hand) remains; historical process gaps are not retroactively closed; an owner-accepted historic process deviation does not imply technical or whole-issue pass. None of that changes the checker in this slice.

Boundaries: the checker's default `980` is a `check_baseline` value for open programme cases. The current seed has 980 total and 443 open, which are not interchangeable. A future `--expect-programme-cases` capture needs a fresh role-permitted open count. No default or fixture change, no live query and no invented verification here.

Historical evidence (original 2026-10-24 non-conformant review, 2026-10-25 alignment review, correction1 and retry reviews, the current-main readiness review) is preserved unchanged. Existing pinned receipts and editable environments are not used or modified.
