# Research: resident AI expiry as data (issue 624)

Disposition: executed. Planning Readiness: Ready.

## Findings

* `infra/sql/resident-assistant.sql` `resident_ai.reserve` hardcoded `@now >= '2026-11-01T00:00:00'`; it was the only SQL time bomb. `resident_ai.complete` has no time check and needs no change.
* `resident_ai.budget` had `(id, reserved_cents)`; the script is applied idempotently on every deploy and by the tests, so the migration must be guarded (`COL_LENGTH`) and the seed insert must name its columns.
* Python gates: `assistant.py` `EXPIRES` (2026-11-01 UTC) and `aoai.py` import it for five client-side checks. They are an independent earlier gate; the issue allows them to stay consistent. Reading SQL at runtime would add a DB read to paths that are deliberately offline, so the constant stays and is documented.
* Local container `ama-350-feedback-sql` is available for the opt-in SQL tests.

## Decision

Add `expires_at DATETIME2(7) NOT NULL DEFAULT '2026-11-01T00:00:00'`. Existing rows take the default (live behaviour unchanged, no data loss). No live expiry or cap is extended; Azure is not touched.
