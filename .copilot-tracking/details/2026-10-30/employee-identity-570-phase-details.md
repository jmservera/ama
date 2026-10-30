---
title: Employee acceptance identity phase details
description: Task-level implementation and validation boundaries
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

Task employee-identity-570-2026-10-30. Refs #570.
Initial direction: source/HTTP-contract repair of acceptance, not auth mapping.
Research Ready; no unresolved local implementation decisions.

<!-- rpi:phase id=P01 -->
## P01: Offline predicate and regression

<!-- rpi:task id=P01-T01 -->
### P01-T01: Failing-before reproduction and corrected predicate

Own src/api/checks/employee_identity_check.py (one constant BINDING, no
credential/browser entry point), and src/api/tests/test_employee_identity_check.py.
Reuse Base, principal and local App/HTTP fixture patterns from test_auth and
test_entra_authoritative. Avoid inheriting their test classes (duplicate tests).
Extract historical BINDING as inert AST data for the recorded red experiment,
without importing/executing historical runners. Final regression runs the new
predicate through Node's fetch stub against real constructed /me payloads.
Red invokes the historical predicate with the old expected-email string;
green invokes the corrected predicate with independent expected-ID pair.
Both consume the same actual constructed /me payload. In red, first assert
responseOk/schemaValid/providerMatches/employeeRole/notViewOnly are true and
expectedIdentity/authenticated/rosterBound are false, then intentionally fail
assertTrue(authenticated). Interface exceptions do not count as regression.
Use an external red harness, no permanent legacy selector.
No raw live claim is needed or available.
Completed: causal red assertion reproduced normally; corrected same-contract
regressions pass, including seven test methods in final API discovery.

Cover absent email, aliased preferred_username, multiple email-like claims,
case/trim/display-name variations, unbound and bound roster, mismatched tenant/
object with same display email, invalid/missing expected IDs, malformed observed
IDs/schema/app_roles, wrong providers/role/view-only, redirects/content type/
non-200 and boolean-only results. Tests make no live requests; Node stub only.
Exact expected pair is constructed fixture data, not taken from payload.
Assert exact /api/me, redirect:error, AbortSignal timeout 120000; fetch rejection,
abort and rejected JSON parsing return fixed explicit failure booleans without
canary-bearing error contents. Include top-level/user/account shape errors and
mixed-type app_roles even when a valid manager role is also present.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Guide and evidence

Guide explains display versus immutable account identity, argument shape and
page.evaluate(BINDING, expected) use. No tracking paths in production code,
docstrings or commit messages. No example real expected IDs or credentials.
State missing raw historical cause, no demonstrated app bug, no retrospective
acceptance. Next live run requires fresh guarded runner/manifest and explicit
owner budget; never rerun exhausted historical sources or provision roster
as a login fix. Chat/map/case only after strict identity admission.
Completed in src/api/README.md; no live runner or live attempt added.

<!-- rpi:phase id=P02 -->
## P02: Validation and persistence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validation

Use existing /tmp/mv tools without modifying shared editable installs.
From src/api, PATH=/tmp/mv/bin:$PATH selects Python 3.12 and pinned tools.
Run under flock -w 600 /tmp/ama-rpi-heavy.lock:
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
python3 -m unittest discover -s tests -q.
Run ruff check ., ruff format --check ., mypy in src/api.
New modules must pass package-config lint/types without new ignores.
Preserve full output externally and concise exact counts in changes.
Check original seven evidence files by hashes/git diff and git diff --check.
Unexpected skips/failures are reported, not silently upgraded or repaired
outside scope. Focused regression first; package validation second.
Completed: 1368 API tests, 318 skips, exit 0; Ruff check/format and mypy pass.
Discovery skips are not integration/gate acceptance.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and local persistence

Reconcile plan/details/changes/state before one independent Review.
Reviewer assesses actual changed files, failing-before and validation evidence,
original failure limits and integration docs. Preserve findings, route later
work without another Review. Required human approval stays unclaimed.
Resolve gh api user; repository-local noreply author/committer; required
Copilot trailer and Conventional Commit, Refs #570 only.
Commit the exact ten-path allowlist in plan locally, no push. Review output:
.copilot-tracking/reviews/logs/2026-10-30/employee-identity-570-review.md.
Fetch main read-only, run complete
tools/rpi-checks.py --all --base reviewed-main --out new external directory
after commit, respecting shared-lock policy. Do not repair unrelated gate
failures, use cloud fallbacks, skip controls or claim successful receipt.
Final receipt/results remain external, avoiding self-invalidating commit.
The full gate owns its shared lock: invoke directly, never double-wrap it.
If any prerequisite is unavailable, record actual blocked/failed command,
retain original failure and stop publication, not the authorized local commit.
The critique worker's local temporary-path restriction is not a parent
restriction; the explicitly requested /tmp shared lock and available session
external output are usable here. Do not modify shared runtime installations.
