# Issue 444 boundary threat model documentation: changes

Date: 2026-10-25. Implements the plan written and critiqued before the edit (commit b7966f5d).

## Changed

* src/api/README.md: new subsection "Threat model for the synthetic preview (#444)": scope and non-goals (not suitable for public hosting, no password auth, issue 462 separate), assets, trust boundaries, a 13-row threat and control table with test or inspected evidence, and residual risks (same-host users, fixture tampering, no rate or concurrency limit, uneven unexpected-error handling, dataset and authority loaded once so a restart is needed, invented fixture, no human review).
* src/core/README.md: one link to the subsection.
* No source, test, web, staff, score, baseline, scorer or workflow change.

## Independent scoped review (documentation accuracy)

Executed once by a code-review agent against the code and tests. It read the code and the 36 named tests (all exist) but could not run the test files (python not on PATH; pytest collection errors not investigated). Findings and dispositions:

| Severity | Finding | Disposition |
| --- | --- | --- |
| Medium | Security-header row overclaimed `test_health_pages_and_security_headers`, which asserts only no-store and default-src none on page assets. | Fixed: the row names what is tested and marks the rest inspected. |
| Medium | Data-entry row omitted the ~/.zava-forward guard. | Fixed. The reviewer's suggested residual (grants markers checked only at start-up) was not applied: resolve_grant re-checks the synthetic and disposable markers on every request through _load_fixture, so it would be wrong. |
| Low | CSP list omitted img-src. | Fixed. |

Correction cycle 1 of at most 2; no accuracy finding remains open.

## Limits

Documentation evidence only. Not a security certification, not an accessibility or live acceptance claim, and no promise of a rubric score change; the assessor's own result will be reported as it is.
