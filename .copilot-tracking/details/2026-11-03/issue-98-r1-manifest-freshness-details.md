<!-- markdownlint-disable-file -->
# Details: issue-98-r1-manifest-freshness

## P01 core

* `_freshness(store, case, draft, digests)` returns one entry per saved diagnostic: `index`, `input_version`, `status` (Current or Stale), `reasons`, `stale_fields` and a re-run `action`.
* Stale reasons: manifest `input_version` differs from the draft version; a newer registered schema version exists; a bound source (id, version, hash, kind) is no longer current. Source staleness lists only the fields bound to that source, so unrelated fields and decisions are untouched.
* Reuses `_current` and the per-report digest cache; snapshots and history are never altered. Availability preflight in `_report` already guarantees sources are readable, and an unavailable draft keeps the existing Unavailable entry.

## P02 evidence

* Two tests in `src/core/tests/test_form_review.py` (JSON and SQL stores): source change, input change, schema change, preserved snapshots.
* README paragraph in `src/core/README.md`; log entry in `docs/reference/log.md`.

## Human boundaries

No approval, resident consent or Finance decision is created or implied. Manual path: the reviewer re-runs `diagnose`. No AI involved.
