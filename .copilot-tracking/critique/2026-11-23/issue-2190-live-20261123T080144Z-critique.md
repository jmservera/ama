# Critique: issue 2190 late_success regression test (2026-11-23)

Executed once on the final candidate plan. Verdict: proceed.

* Risk: timing-based negative control could flake. Mitigation: the status delay (900 ms) is far above the 500 ms networkidle window and the page has no network, so networkidle resolves immediately; applied directly (use 1200 ms delay).
* Risk: the test duplicates the double-based test. Accepted: it adds the real-browser behaviour; the double test stays as the cheap order pin.
* Scope: tests only, no src or check change, no relaxation. Tier is focused, since no src code changes.
* No conflict with owner decisions; no Azure use needed.
