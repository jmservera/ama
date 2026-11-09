---
title: "#184 current-main validation plan"
ms.date: 2026-11-09
---

Prospective plan, written before merge. Scope: ordinary local merge of fetched origin/main 1f28d0913 (no rebase, no force-push), evidence of equivalence, focused impacted checks, authored review, frozen local commit. No product correction. A source conflict or failing impacted test stops the pass with exact scope and the original correction-budget eligibility (counts not reset).

## Phases

* [ ] A1 Merge `git merge --no-ff 1f28d09130c8e058a0436d468e6a22f3c4c24f47` after verifying origin/main equals it preserving the parent ancestry; expect a clean automatic merge.
* [ ] A2 Prove relevance: blob-hash comparison of the 31 reviewed non-tracking source paths (HEAD vs merged), import-closure assertion, grep.
* [ ] A3 Run impacted checks: core test_paired_equity (new main tests), test_live_doc_links, a core sensor smoke selection through the merged tree; core-wide ruff, format and mypy under pinned venv-184 (critique 3).
* [ ] A4 SQL: rerun both selectors (70 default, 10 analysis) in an owned disposable container under `flock -n /tmp/ama-rpi-heavy.lock`, recording pip freeze and image digest (critique 1-2); prior logs are kept as history, not reused. If the lock is busy, do other work and retry; never queue.
* [ ] A5 Record changes, authored review (not independent), state; update KB log only if a KB file is materially edited (none planned).
* [ ] A6 Commit locally with repo-local noreply identity and Copilot trailer; handoff file.

## Gates

* Demo-targeted tier (owner 2026-11-09): no `rpi-checks --all/--changed`, no receipt. Hosted CI after publication and the independent exact-head review stay required.
* Carried Low remains explicit and open. Original 53/48 mypy record stays.
