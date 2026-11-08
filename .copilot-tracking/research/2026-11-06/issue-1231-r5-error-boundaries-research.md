---
title: Issue 1231 research r5 (unsupported hard link and committed-cleanup error boundaries)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 13:56Z, before any rebase, test run, source edit or test edit in this continuation. Same original session b353a2c9, lineage R1, R2, R3/R4 (FULL gate on `b7f6186`). All earlier records and raw evidence (`/tmp/1231-ranking-archive-r1-1106/`, `/mnt/ama-gates/*1231-r[1-4]*`) are preserved unchanged. The R4 FULL receipt is historical for `b7f6186` and is invalid for any rebased or corrected head.

## Identity and pins

* Branch `fix/ranking-archive-concurrent-writer-metadata`, head `b7f6186dc1c7357f255c7d54da30b501ea5ba111`, tree `41c2ea733564059f92a232a2a539f0c5fb2989dd`, ignored-inclusive status empty at intake.
* Corrected parent #79 `feat/ranking-publication-runner-79` is local only at `43080ab42a96fada36b9d0bc523dfa16fe0c3cd5`, tree `e806cf3486ec00921ea090fa23ee1e33351f8606`. The child's merge base is the old parent `397419724e68b24bce879512a24c7df430177f87`. The parent delta is nine files (r12 RPI records, `src/core/README.md`, `ranking_publication_runner.py`, its test module) and fixes two inherited runner findings (archive enumeration and capacity probe errors, duplicate case ids).
* Parent targets #73 `ead177ef90d24666557708ea344848a1be43bdf8`; the eventual child PR targets the #79 parent, never main. `origin/main` is `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (provenance only; no fetch needed).
* Research disposition `executed`; Planning Readiness `Ready`.

## Findings in scope (own-child, Medium, from the exact-head functional assessment of b7f)

Source: coordinator session file `review-1231-b7f-whole-functional-r64/functional-findings.json`, findings 3 and 4. Findings 1 and 2 are parent-owned and already fixed by the corrected parent; they are out of scope.

1. Unsupported hard link. `ranking_publication.publish` lets the `os.link` `OSError` escape by design (owner decision: require atomic hard links and fail closed). The runner converts it to `publish_failed`. `Store.publish_ranking_snapshot` (`store.py` 250-263) catches only `PublicationError`. `server.py` ~1153 calls it inside the POST `try`, whose handlers map `PermissionError` to 403 and re-raise a bare `OSError` (ENOTSUP) as an unhandled exception. A manager hitting EPERM therefore sees an authorization failure.
2. Cleanup after commit. After a successful `os.link` the final record exists, but `finally: os.unlink(stage)` can raise `OSError`, which replaces the return value. The runner reports `publish_failed` with no path or date; the Store never audits the publication.

## Prior art read

* `server.py` POST handler ladder: `QualityOutcomeError` returns 503 with `"outcome": "committed"`; `DocumentStoreError` returns 502 with a fixed clean message; generic `Exception` returns 503 only on selected paths. The `ConflictError`, `GateError`, `PermissionError`, `ValueError` mappings are the existing conventions. `PermissionError` must stay 403 for real role checks.
* `documents.DocumentStoreError` ("storage back end failed, report a clean error, write no metadata") shows the existing domain-exception-per-store-failure pattern. It is document specific and its 502 text is fixed, so reuse would mislead. A dedicated small exception is the closest analogue.
* Store logging uses `logging.getLogger(__name__)` for operator diagnostics, with fixed client messages (`store.py` 664, 732).
* Runner `_refusal(code, message, next_action)` records and the `warnings` list printed to stderr are the existing runner diagnostic convention (`stale source` warning uses it).
* Helper return shape `{path, written, published_on}` is asserted by equality in existing tests, so any new key must be absent on the ordinary path.
* No other caller of `ranking_publication.publish` exists in `src` besides Store and runner (grep).

## Design questions and answers

* Where is the narrow boundary? Store, around only the `publish` call. Keep helper semantic (fail closed, `OSError` propagates). Store translates `OSError` to a new `ranking_publication.ArchiveStorageError` (not a `PermissionError`, not a `ValueError`), with an actionable message naming the error class and errno symbol, never the path. The server maps that class to 503 before the generic handlers. No change to global `PermissionError` handling or to the role check.
* Is translating all `OSError` too broad? The caught span is a single call whose only I/O is the archive; an `EACCES` on an unwritable archive is also a storage condition, not authorization. `PublicationError` keeps its 400 mapping. No broad `except Exception`.
* Cleanup after commit: the helper must separate commit state from cleanup. When `os.link` succeeded and `os.unlink(stage)` fails, return the truthful committed result plus `stage_retained` (the stage file base name only). The stage is retained for deliberate recovery; the hidden name is already ignored by archive enumeration (`ranking-` prefix). When the link did not commit, behaviour is unchanged (the unlink error propagates as before, including the `FileExistsError` loser path, which reports no commit by this caller).
* Runner: add a `stage_not_removed` warning (code, message, next action) and `stage_retained` field, status `published`, `written` true, with the usual path and date. No success-shaped result for an uncommitted write.
* Store: audit `ranking_snapshot_published`, then log a warning and return the normal body plus a plain-language `warning` without any path.
* Hard-link support itself is unchanged and still only EPERM/ENOTSUP-injected in tests; no real unsupported-mount evidence exists. No deployment or mount approval is implied.

## Risks and unknowns

* Rebase conflicts are possible in `src/core/README.md` and `test_ranking_publication_runner.py` (both sides edited). Resolve by keeping both intents; stop with exact paths if intent is irreconcilable.
* Light tool versions in the read-only `/tmp/zf79venv` are unpinned relative to the project pins; I will record actual versions and not claim pinned or isolated environments.
* FULL, independent whole-feature review and publication remain pending and are not part of this stage.
