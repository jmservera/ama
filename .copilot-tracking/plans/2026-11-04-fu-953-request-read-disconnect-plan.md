# Plan: issue 953 request-read disconnect logging

Research: [research](../research/2026-11-04/fu-953-request-read-disconnect-research.md). Details: [details](../details/2026-11-04-fu-953-request-read-disconnect-details.md).

* [x] Phase 1: classify a ConnectionError raised while the request is read (parse or body) as a client disconnect logged at WARNING, no 500 attempt.
* [x] Phase 2: regression test for the parse-phase disconnect; rely on the existing backend test for 500 plus ERROR.
* [x] Phase 3: focused tests, ruff, mypy; log entry.

Critique (single pass, self-run): keep the existing `client-disconnect exc=<name>` log substring so the #924 test still matches; log only class, method, path and phase (no message, no secrets). Applied.
