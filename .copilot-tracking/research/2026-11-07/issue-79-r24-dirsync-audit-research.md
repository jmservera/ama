---
title: Issue 79 research, r24 directory-sync audit correction
ms.date: 2026-11-07
---

Task `issue-79-r24-dirsync-audit`, parent `issue-79-r23-merge-score-23b`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: `feat/ranking-publication-runner-79`, head `b8ad4a0e607fca85cef198f6428cd41c758b04b0`, tree `8c9b7aa994446f91ab330b3bc1c9042a1f0b0c47`, ignored-clean; `origin/main` `23b26a7f3a4693cd20dcf0447303d97491096cb3` is an ancestor. Preserve ref `preserve/issue-79-pre-dirsync-audit`. Child 1231 is not touched.
* Independent functional assessment 01457fc4 (`functional-findings-completion.json`): Medium Contract. After the final `os.link` succeeds, `_fsync_dir` failure raises out of `ranking_publication.publish` before `Store.publish_ranking_snapshot` audits. The final record stays (existing behaviour), but no audit event exists; the API shows an unhandled error.
* Code: `publish` in `src/core/src/zava_forward/core/ranking_publication.py` links then calls `_fsync_dir`; the `finally` only unlinks the stage. `Store.publish_ranking_snapshot` in `store.py` catches only `PublicationError` (mapped to `ValueError`), then audits. The API route `/api/ranking/publish` in `server.py` has no handler for an OSError, so it falls to the generic 500 path. The runner catches `(PublicationError, OSError)` and refuses.
* Prior art for committed-but-unconfirmed outcomes: `IncidentCommittedError`, `GovernanceCommittedError`, `AppointmentCommittedError`, `ResidentCommittedError` return HTTP 409 with `outcome: "committed"` and a path-free message; persistence logging uses `logging.getLogger(__name__).exception(...)`.
* The suggested fix (distinct committed-but-unconfirmed outcome, audit, error) is supported. Rollback is not: removing the final name after a failed sync would break no-replacement and first-writer-wins guarantees.
* Retry note: a retry finds the final name and returns `written: false` without a directory sync, so it cannot confirm durability. Recorded as a residual, not changed here.

## Conclusions

* Add a typed `OSError` subclass carrying path and date; keep it an `OSError` so the runner and any `OSError` caller keep refusing. Store audits an explicit unconfirmed event, logs and re-raises; the API returns 409 `outcome: committed_unconfirmed` with a fixed, path-free message.
* Unknowns: whether the filesystem really persisted the name; the child's `ArchiveStorageError`/503 translation is reconciled by the coordinator.
