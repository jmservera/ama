---
title: Issue 1360 extension E1 research, committed transfer follow-up failure wrongly reported as Nothing recorded
ms.date: 2026-11-10
task_id: 1360-extension1-1110
---

## Disposition and scope

Research executed 2026-11-10 (UTC) after witness launch (seq 1). Planning Readiness: Ready. Disposition: executed, consuming the original diagnostic record `0c77f18fa5b7de4c0a73e58255ccfbe45a75058c` and the D2 dated authority audit rather than repeating them.

Authority: owner approval 2026-11-10 after 23:10, "Authorize up to five additional corrections for this existing scope". A new finite extension E1 to E5 applies to the inherited issue 135 and 1360 lineage. The original C1 to C5 stay spent and the D2 zero-authority history is preserved: no reset and no reinterpretation of 2026-11-09. This task is E1 only. E1 used, four left. No automatic next cycle.

Scope: only the committed-exception transfer follow-up failure that reports "Nothing was recorded" after the write was durable. No change to transfer semantics, permissions, state, consent or new actions. No broad exception refactor. No fix for unrelated exceptions, export, privacy or auditing.

## Inputs consumed

* Original diagnostic (read-only, not an independent review): Approach 1 reproduced the defect with real SQLite and the real CLI. A post-commit `_sync` raising `OSError` or `ValueError` gave exit 2 and "Nothing was recorded" although the refusal document, the audit entry and the `meta seq` increase had committed. A fresh reopen showed them retained. Retry exited 0 with `added=0 already_present=1` and audit count 1. Controls N1 (no injection, exit 0) and N2 (conflict, rollback wording, injection did not fire) stayed distinct. No data loss was demonstrated.
* D2 audit: C1 to C5 were all consumed and issue number 1360 grants nothing. The extension arrives only from the owner approval above.
* Baseline: `src/importer` 79 tests OK and `src/core` `test_import_refusals` plus `test_priority_order` 163 tests OK (72 skipped, existing) on the merged head, in own venv `/tmp/zf-1360-e1`. Module origins resolve under the worktree.

## Base identity

Branch `test/demo-transfer-outcome-diagnostic-1360-1110`. Fetched `origin/main` `6d4cd62475ba89a214055f761b8e3276ef063d44` and merged it ordinarily (no rebase, no conflict) as `307ba870a`, before the new chain. Main changed `sqlstore.py` since the diagnostic base `fe59ef56`, so the findings below were re-read at the merged head.

## Static findings at the merged head

* `sqlstore.py` `SqlStore.save`: after `COMMIT` and the in-memory snapshot updates, a store that is behind (`cur != self._seq`) calls `self._sync()`. Only `except RuntimeError` is translated to `CommittedReloadError` (class docstring: the write committed but the reload did not settle; `committed = True`). `OSError` and `ValueError` from that post-commit reload escape untranslated.
* `_persist_import_refusals` re-raises `CommittedReloadError` untouched, so the CLI already prints the truthful "saved ... may be recorded ... run again, it adds nothing twice" for it. For any other error it discards and re-raises, and the CLI generic `(OSError, ValueError)` arm says "Nothing was recorded".
* The same `ValueError` and `OSError` types are also legitimately raised before commit (normalisation, `MAX_REFUSALS`, store open and write failures). The CLI cannot tell the two apart from the type alone, so a wording-only change to the generic arm would either keep the false claim or weaken the true pre-commit message. The only exact distinction is the one the store knows: whether `COMMIT` already returned.
* Other consumers of `CommittedReloadError` (API server priority, resident and journey routes, `sensor_review_draft`) already treat it as a committed outcome. Widening the single post-commit translation makes them truthful for the same failure and changes no pre-commit path.

## Options

1. Core, one arm: translate `OSError` and `ValueError` from the post-commit `_sync` to `CommittedReloadError` in `save` (chain with `from error`, keep `_seq = -1`). Exact distinction, no CLI change, no new action. Recommended.
2. CLI wording only for the generic arm: cannot be exact; rejected as above.
3. Pre/post classification in the importer by re-reading `meta seq`: adds a read that can itself fail and races other writers; rejected.

`sqlite3.Error` from the same reload stays on the existing driver arm ("not known whether ... run again"), which is already truthful and out of scope.

## Candidate hunks (owned, minimal)

* `src/core/src/zava_forward/core/sqlstore.py` `save`: the single post-commit `except` tuple.
* `src/importer/tests/test_import_exceptions.py` `TransferFailureTests`: real SQLite, real `SqlStore`, actual CLI regression with the injection only at the post-commit `_sync`, plus the pre-commit control, retry idempotence and unchanged audit count.
* `src/core/tests/test_priority_order.py` is the existing nearby test for `RuntimeError`; one sibling test for `OSError` and `ValueError` may sit beside it only if the importer test is not enough.

## Overlap and integration dependency

Open sibling scopes: 1419 (server CSV only), 132 (staff intake), 131 (household inventory) and 80 (checker). None edits `SqlStore.save` post-commit translation. There is no currently active 135 author. The shared integration dependency is `sqlstore.py` itself, which main already changed; merge order is Root's. No hunk here touches the other scopes.

## Planning readiness

Ready. Unknown and not claimed: any hosted CI result, any independent review, any behaviour beyond the SQLite store (the MSSQL store was not exercised).
