---
title: Demo release checklist for issue 202 (2026-11-22)
ms.date: 2026-11-22
---
Checklist for the owner. Unticked items are owner or later-step actions; nothing here has been performed beyond reading.

* [x] Archive tag `v0.21.0` exists locally and points at the last commit containing `mvp/` (`65a514ed`, 2026-10-27).
* [ ] Push the tag: `git push origin refs/tags/v0.21.0:refs/tags/v0.21.0` (recorded in `docs/reference/log.md`; not run, nothing is pushed in this task).
* [x] `mvp/` and `prototype/` are absent from the tree (`git ls-files` shows 0 tracked files).
* [x] Deployed revisions `ca-cutover-test-demo-api--0000053` and `ca-resident-demo--0000025` are Healthy at 100 percent traffic.
* [x] Release notes drafted: [issue-202-release-notes-demo-2026-11-22.md](./issue-202-release-notes-demo-2026-11-22.md).
* [ ] Owner decision: publish a GitHub release with the tag, or not.
* [ ] Owner decision: keep, rename or delete `mvp-ci.yml` and `mvp-validation.yml` in a FULL-tier change (they edit pinned-hash gate tooling, `src-ci` path filters and tests).
* [ ] Owner: update branch protection after cut-over; the active `mainprotect` ruleset lists no required status checks, so none needs repointing today.
* [ ] After merge of this change, tick the proven criteria in issue #202 and decide closure.
