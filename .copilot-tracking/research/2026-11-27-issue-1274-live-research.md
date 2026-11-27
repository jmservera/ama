---
title: Issue 1274 live research (2026-11-27)
---

## Disposition

Executed. Prior notes (2026-11-18 to 2026-11-23) cover endpoints, 504 recovery, truncation by size, wrong checksum, exhaustion and workflow wiring. New angle: transport exceptions that are not OSError.

## Reproduced defect

`tools/install-actionlint.py` `fetch()` catches `urllib.error.HTTPError`, `OSError` and `InstallError`. `http.client.IncompleteRead` (a body cut short in transfer, the same class of fault as the observed 504 flakiness) and `http.client.BadStatusLine` derive from `HTTPException`, not `OSError`. Repro: an opener whose `read` raises `IncompleteRead` escapes `fetch()` unretried, so the second official source is never tried (script `/tmp/repro1274.py`, output `ESCAPED: IncompleteRead`).

## Planning readiness

Ready.
