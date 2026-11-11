---
title: Issue 1360 extension E1 plan
ms.date: 2026-11-10
task_id: 1360-extension1-1110
---

## Objective

Make a committed transfer whose post-commit reload fails with `OSError` or `ValueError` report a committed, unconfirmed outcome instead of "Nothing was recorded", while a failure before `COMMIT` keeps saying nothing was recorded. Authority: owner E1 of five (four left), inherited 135/1360 lineage, original C1 to C5 and the D2 zero history preserved.

## Decisions

* Option 1 from research: in `SqlStore.save`, translate `OSError` and `ValueError` from the single post-commit `_sync` call to `CommittedReloadError`, chained, with `_seq = -1` kept. No CLI change: its existing `CommittedReloadError` arm already gives the truthful recovery text ("may be recorded; run again, it adds nothing twice").
* No change to transfer semantics, permissions, state, consent, retry or new actions. `sqlite3.Error` handling unchanged. No catch-all and no silent default.

## Phases

* [x] Phase 1 research (merged current main, baseline green)
* [ ] Phase 2 source change: one tuple in `sqlstore.py` plus its comment
* [ ] Phase 3 regression tests (importer real-CLI case with real `SqlStore`; core sibling case) and targeted checks
* [ ] Phase 4 review once, records, local commit, handoff

## Validation

Targeted: `src/importer` discover, `src/core` `test_import_refusals` and `test_priority_order`, ruff check and format check and mypy for the touched packages, and the affected API case-journey test if it exercises `CommittedReloadError`. Tier: focused (owner DEMO targeted), because no gate, workflow, dependency, deployment, SQL service or security control changes. No full SQL, Docker or cloud gate. Hosted CI is not observed.

## Success criteria

* Durable commit plus post-commit `OSError`/`ValueError` gives exit 2 and a message that does not say "Nothing was recorded", and says the refusals may be recorded.
* Pre-commit failure still says nothing was recorded and the store holds no refusal.
* Retry adds nothing: one document entry and one `recorded_import_refusals` audit entry.
* No partial-success fabrication: the text claims no count of recorded items.
* Ledger and source files unchanged by hash.
