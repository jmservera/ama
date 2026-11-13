---
title: 435 unified post-1542 rebase plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1: rebase onto `2489d839e` (keep both append-only log entries; inventory TSV conflict resolved by regeneration) and cherry-pick `e5e37ffb4`.
* [ ] Phase 2: scratch venv `/tmp/venv-435u-2013` with pip, `pip install -e src/core`, regenerate the inventory TSV, check mode.
* [ ] Phase 3: run `test_cutover_audit.py` (expect 9 OK) and the #441 C9 verifier; record freshness false only for intentional `docs/` edits.
* [ ] Phase 4: remove only `/tmp/venv-435u-2013`.
* [ ] Phase 5: create the state file after the rebase, commit with refs and trailers using the privacy-safe noreply email, record `commit-complete`, leave tree clean. No push, no GitHub edits.

Tiering: focused (documentation and generated TSV only).

## Critique (rubber-duck, executed once; verdict Revise, applied directly)

* Require every non-freshness verifier check true and inspect lint execution errors; the verifier exits nonzero on expected freshness false.
* Record both the committed `docs src` diff and the dirty-file list as the freshness cause.
* Run the verifier on the final tested tree; the report names that head. State file records `commit-complete` inside the single commit so the tree stays clean.
* Confirm `/tmp/venv-435u-2013` does not exist before creation; delete only that path.
