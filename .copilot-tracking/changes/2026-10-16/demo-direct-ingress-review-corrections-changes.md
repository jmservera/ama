# Direct ingress routed review corrections

Task ID: issue-360-review-corrections. Slug: demo-direct-ingress-review-corrections.
Parent: issue-360/demo-direct-ingress.

## Scope and Authorization

The user's original request requires complete working offline implementation
and PR delivery. The single completed parent Review found RV-001 High invalid
demo job names and RV-002 Medium ineffective role-denial endpoint. Apply only
these routed implementation defects and matching docs/tests before delivery.
This is later implementation, not a second Review or alteration of its verdict.
No new architecture/approval, live work or automatic follow-up loop is selected.
Research/plan are reused from the parent and the canonical review findings.

## Plan

* Shorten demo-only job role suffixes within the documented <32-character
  platform limit at supported main input bounds; preserve all non-demo names.
  Update ledger alert naming and output tests.
* Establish authenticated session with /api/me 200, then require Contractor
  denial at /api/stats 403. Distinguish invalid session 401. Use real provider/
  router regression, retain private credential handling and sanitized output.
* Update migration/probe docs and rerun compiled infra/probe checks.

## Execution and Validation

RV-001: demo jobs now use auth/orch/audit/load suffixes; supported main
workload/environment bounds produce unique names below 32 characters. Existing
non-demo names remain exact. Ledger alerts use the matching conditional name.

RV-002: role credentials must first return /api/me 200, then Contractor-denied
/api/stats 403. Invalid sessions fail before the role request. Added actual
trusted-provider/router loopback regression proving those statuses and
anonymous 401, with no response-body or credential output.

Both findings are implemented, not independently re-reviewed. The parent
Review remains Complete / Not accepted for its assessed candidate.
Corrected full infra suite: 237 tests passed, no skips, 60.298s.
Focused compiled tests 46 passed and probes 20 passed. Corrected templates
built/linted; scoped Ruff and CI format passed; git diff --check passed.
An initial fake-server test branch indentation error and two overlong new
lines were corrected before the successful results. No live validation.

Publication refresh found main now two commits ahead and PR 359 merged. The
initial merge-before-edit prerequisite was met at intake; integrate the newer
device-prompt fix before final publication without rewriting history.
