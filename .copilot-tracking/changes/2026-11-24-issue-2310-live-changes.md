# Issue 2310 changes, live run 4 (2026-11-24)

Tier: focused (documentation and evidence only; no src change). Planned files: docs/reference/research/issue-2310-live-r67-2026-11-24.md, docs/reference/README.md (index row), docs/reference/log.md. Record written before the index and log edits.

## Files

* docs/reference/research/issue-2310-live-r67-2026-11-24.md (new)
* docs/reference/README.md (index row)
* docs/reference/log.md (entry)

## Validation

* Auth suites (src/api, documented PYTHONPATH): 93 tests OK.
* Live read-only probes on revision 0000067: see the research note. Not run: rpi-checks, hosted CI (nothing pushed).

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Anonymous protected API GET with browser UA and Accept application/json returns 401, not a redirect | Proven in code and tests; unproven live | Edge answers 302 before the app (`RedirectToLoginPage`); edge change is a production auth boundary change, out of demo authority |
| Anonymous protected page request still redirects to Entra | Proven (tests and live) | curl 302 to Entra; Playwright reaches the Entra sign-in page |
| Existing auth tests pass; no weakening of any route protection | Proven | 93 tests OK; no source change |
