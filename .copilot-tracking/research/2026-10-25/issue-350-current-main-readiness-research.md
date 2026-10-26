<!-- markdownlint-disable-file -->
---
title: Issue 350 current-main readiness research
description: Read-only lifecycle, RV-201 and current-main evidence recorded before any plan, critique, merge or edit
ms.date: 2026-10-25
---

Written 2026-10-25 from about 19:48Z, before the plan, critique and merge of this continuation. No merge or other file edit had been made when it was written. Nothing here replaces or redoes an original review.

Lifecycle (fresh `git fetch`):

* Local and remote branch `test/deployed-feedback-harness-350` are both `a9bdae317489b873f9e1ffc58a81d32282f39cb0`. The remote is an ancestor of HEAD (checked with `merge-base --is-ancestor`). Tree clean, no ignored files. PR 436 is open, draft and mergeable.
* `origin/main` is `ea5577b2ed0e051161a83813daa63d86e4613c7a` and is **not** an ancestor of HEAD. Merge base is `36996d70`; main is 4 commits ahead (#456, #448, #457, #458).
* Main-only changes (three-dot diff): rubric score files, `infra/README.md`, `src/api/README.md`, `src/core/README.md`, `src/core/pyproject.toml`, `factory.py`, new `seed_merge.py`, `sqlstore.py`, `test_mssqlstore.py`, `test_seed_merge.py`, and docs. Main does not touch `tools/check-demo-feedback.py`, its tests, `server.py`, `projection.py`, `identity.py` or auth, so no textual conflict with the branch checker work is expected. The branch's checker tests import runtime schemas, so a post-merge re-run is the actual compatibility test.
* Disk: 22 GB free (92 percent used). A complete gate was about 40 minutes and uses several GB of Docker images and venvs; it is not run here.

RV-201 evidence: `.copilot-tracking/reviews/logs/2026-10-25/issue-350-checker-correction1-retry-review.md` records outcome non-conformant with one non-blocking finding. PC-201 in the retry critique claimed artifacts were committed while untracked; the wording was corrected to future tense with an in-file disclosure, and that correction was not independently re-verified. The committed critique file already carries the corrected wording (commit a9bdae31).

RV-201 disposition: no owner decision blocks bounded integration. RV-201 is non-blocking, its correction is already recorded, and the only open item is independent re-verification, which the single scoped assessment of this continuation can perform against the committed file. Whether the retry review is accepted overall remains a coordinator or owner decision; this work records no acceptance and does not relabel the original outcome. If the assessment disagrees with the correction, the finding stays open and is routed.

Retained contract (from earlier phases, unchanged): the checker handles a deep-nesting `RecursionError` as BLOCKED, and validates the Application Administrator `/api/me` with empty counts and staff separately. `admin_account` stays not-run and overall never passes. No staff-database login prerequisite exists after PR449.

Unrelated drift to route, not change: `src/api/README.md` lines 2257 and 2282 still mention `ZF_AUTH_EMAIL_FALLBACK`, which main did not fix.
