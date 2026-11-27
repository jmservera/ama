# Issue 1837 research (run b), 2026-11-27

Refs #1837. Synthetic demo, desktop only. Base `a5b36579c2`.

## Status

Main already carries the fix (`web/nomination-routes.js` posts JSON with `X-ZF-CSRF`). The earlier 2026-11-27 run added a failure-path test and recorded the axe criterion as "not re-run".

## Angle for this run

Re-run, on the current head, the three browser journeys with axe plus the affected unit tests, so the "axe, zero unexpected skips" criterion has a fresh record instead of an inherited one. Live writes stay withheld: they add irreversible records to the shared demo.

Planning readiness: Ready.
