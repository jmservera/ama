---
title: Issue 131 extension 1 (E1) missing historical households field (research)
ms.date: 2026-11-10
task_id: 131-extension1-1110
---

## Status

Research stub created before the research-open witness event. Substantive research follows after that event.

Scope: the residual of original finding 1. A stored inventory revision with no `households` key is accepted as an explicit null (Unknown). Authority: owner answer on 2026-11-10 after 23:10, "Authorize up to five additional corrections for this existing scope", recorded in Root brief `brief-131-extension1-2311.txt`. This is E1 of a finite E1 to E5 extension. The earlier spent history and the previous proved minimum of 0 are preserved; this is not a reset, not a reinterpretation of the 2026-11-09 grant and not a perpetual allowance. No automatic E2 follows the frozen handoff.

## Disposition and scope

Research executed 2026-11-10 (UTC 23:13 onward) after the research stub, state file and `research-open` witness event (seq 2, ok). Planning Readiness: Ready.

This is E1 of the finite extension: the residual of original finding 1, not a new slice. In scope: Core `resident_decisions.py` `_inventory_history_ok`, the existing corrupt-history test in `src/core/tests/test_resident_decisions.py`. Out of scope: new fields, permissions, resident data, consent, schema, UI, API change, issues 132, 144, 1360, 1362 and any unrelated 131 work.

## Evidence

* Baseline on clean `61e95201887bfd7c6b49ce9811c277856291e65f` (owned venv `venv-131-household-inventory-1110`, mypy 2.4.0, Ruff 0.17.1, module origins resolve to this worktree's `src/core` and `src/api`, owned synthetic `ZF_DATA`): Core `test_resident_decisions.py` Ran 416 OK skipped=148; API `test_resident_api.py` Ran 21 OK skipped=1. No product failure blocks the correction. The skips include SQL-Server opt-in cases that did not run: MSSQL is not run and not claimed; the SQLite inherited store cases ran.
* Independent assessment `independent-131-inherited-repair-1402/functional/functional-findings.json`: one Medium residual. The identity-reason finding is resolved.
* Defect, read from source: `_inventory_history_ok` calls `_history_rows_ok(revision.get("households"))`. `dict.get` returns None for an absent key, and None is the valid explicit Unknown value, so a revision with no `households` key passes the shared validator. The view then raises `KeyError` only for the latest revision (so it reads Malformed only by accident of position), while the writer accepts `expected_version` and appends a valid revision, after which the view inspects only the new last revision and reports Declared or Unknown. This launders a malformed earlier revision. The supported actions always write the key, so only corrupt-store injection reaches it; `TENURE_HOLD` still holds.
* `origin/main` fetched at `6d4cd62475ba89a214055f761b8e3276ef063d44`, 24 commits ahead. It does not touch `resident_decisions.py`, `test_resident_decisions.py` or `test_resident_api.py`. It adds 73 lines to `src/core/README.md` and unrelated API tests and workspace scripts. A read-only `git merge-tree --write-tree HEAD origin/main` was clean (tree `3cda8c62`). The ordinary merge is performed inside the implementation after the marker; no rebase, reset or amend.
* Authority: Root brief `brief-131-extension1-2311.txt`; E1 of finite E1 to E5; the previous spent history and the proved minimum 0 stay as recorded; no reset and no automatic E2.

## Smallest fix

Require the `households` key to be present in every stored revision before its value is validated: `"households" in revision`. Explicit null stays valid Unknown. No other contract changes, so legitimate stale-digest history and legitimate Unknown are not rejected (contract evidence: the original design records Unknown as an explicit null and the existing Unknown tests).

## Regression plan (red on the old code, green on the new)

* Remove only `households` from an otherwise valid revision: singleton and earlier-revision-then-valid-last. Assert Malformed view, gate with malformed first and hold last, refused scope, refused writer with no durable case or audit change. JSON base and inherited SQLite store.
* Controls: explicit null revision still reads Unknown and accepts the next revision (round trip, reopen); existing stale-digest control retained.

## Limits

* No SQL Server, browser, cloud, model, provider or private data. Local evidence only: no publication, acceptance, hold release, universal C1 or C2 compliance.
