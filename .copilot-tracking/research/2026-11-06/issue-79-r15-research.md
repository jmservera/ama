---
title: Issue 79 research, continuation r15 (independent d654 review corrections)
ms.date: 2026-11-06
---

Task `issue-79-r15-d654-review-corrections`, parent `issue-79-r13-alignment`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Starting head `d654634fcbe5c82a362e9a3d948d09d0c2993d6d`, tree `7bf7a4af3f494d03c16d3af92fe7e9fa4cc6badb`, ignored-clean. The r14 FULL receipt (`/mnt/ama-gates/g79-r14-1106/receipt.json`) is historical for that head only.
* Independent review of d654 returned REQUEST CHANGES: `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-79-d654/functional-findings.json`. It is preserved unchanged and is not regraded here.
* `ranking_publication.publish` (read at this head):
  * checks `os.path.exists(path)` and then returns `published_on` from whatever JSON sits at the final name, with no validation (HIGH 2);
  * writes the shared `<path>.tmp` with no fsync of file or directory, then `os.replace` (HIGH 1, MEDIUM check-then-write race).
* `verify` already holds the validation rules: parse, snapshot hash, name equals content, valid date.
* Runner (`ranking_publication_runner.publish` path) already routes `PublicationError` and `OSError` to `publish_failed`, and its `exists` shortcut only skips the capacity probe. No runner change is needed.
* `Store.publish_ranking_snapshot` turns `PublicationError` into `ValueError` and audits `ranking_snapshot_already_published` for any `written` False, so a corrupt file would be audited as already published. It does not record the policy sign-off state. `Store.ranking_publication_status` calls `verify` and `overdue` (a second `verify`) without `OSError` handling.
* `run_key` is computed in the runner (`policy_hash`, `as_of`, window `today`) and only reported. Same-window duplicate publication is made idempotent by the snapshot-hash file name, not by `run_key`.

## Design (existing patterns)

* Unique temp name in the archive folder via `tempfile.mkstemp` (name starts with `.`, so `_names` ignores it), write, flush, fsync, publish with `os.link(tmp, final)`: first writer wins and `FileExistsError` is the loser signal; the loser validates the winner and returns `written` False. fsync the directory after the link. Remove own temp in `finally`.
* A shared `_existing(path, snap)` check: file opens and parses, `snapshot` equals the supplied snapshot, hash matches, name matches, `published_on` is a valid date; any failure raises `PublicationError` and never overwrites.
* Store: audit detail and response gain `policy_signed` (from `ranking.is_signed`); status catches `OSError` into a structured problem and computes `overdue` from the single result.

## Limits and unknowns

* `os.link` needs a filesystem with hard links; an `OSError` there already surfaces through the runner as `publish_failed` and through the store as an error, never as success.
* Policy-owner signoff, Legal retention, scheduled publication, hosted CI and a fresh FULL and independent review of the corrected head stay unproven. Light checks only; the shared heavy lock is held by #81 and is not touched.
