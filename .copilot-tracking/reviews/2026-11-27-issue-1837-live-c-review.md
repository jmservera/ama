# Issue 1837 review (run c), 2026-11-27

Refs #1837. Review executed once, after implementation. Outcome: conformant for the harness-only scope; independent exact-head review, hosted CI and the coordinator's full-tier receipt remain open and owner-gated.

## Checks

* Diff is one route-handler condition in `src/api/checks/nomination_browser_check.py`; no handler, permission, CSRF or validation code changed. The reverted first attempt is not in the diff.
* The abort is narrow (`/api/assistants*` only); `non_get_requests_while_viewing` stayed empty and axe reported no violations in three runs.
* Evidence matches claims: failing-first is a captured lock-holder stack, not a deterministic test, and the changes record says so.
* No secret or credential appears in artifacts.

## Routed follow-up (not progressed here)

* `assistants.registry` runs a `GET` inside `BEGIN IMMEDIATE` and keeps running after client disconnect; under load it starves writers beyond the 5 s busy timeout. Own research needed (RAI control plane, SERIALIZABLE on MSSQL).

## Unproven

Live writes (withheld), independent review, hosted CI, full receipt.
