---
title: Employee acceptance identity changes
description: Offline runner expectation repair, regression and validation evidence
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

Task employee-identity-570-2026-10-30. Refs #570.
Declared scope: full bounded plan. Research executed / Ready; Plan Ready after
one Complete / Revise critique and recorded direct dispositions.
Implementation started at P01-T01; no live permission.

## Plan and Evidence

* .copilot-tracking/research/2026-10-30/employee-identity-570-research.md
* .copilot-tracking/plans/2026-10-30/employee-identity-570-plan.md
* .copilot-tracking/details/2026-10-30/employee-identity-570-phase-details.md
* .copilot-tracking/plans/2026-10-30/employee-identity-570-critique.md

## P01: Causal Regression and Predicate

P01-T01/T02 complete. New capture-free BINDING under src/api/checks is a
reusable next-run predicate, not a sign-in executable. Expected tid/oid are
mandatory independent inputs. Display email and roster binding remain
diagnostic booleans. App auth/me mapping is unchanged. Future integration
requires explicit owner authorization and fresh guarded attempt ledger.

### Failing-before reproduction

External red harness AST-extracted original BINDING without importing the
historical runner. It generated an actual local HTTP /me using existing
test_auth fixtures and a trusted-proxy ProgrammeManager principal with
independently specified tid/oid, no staff binding and no display email.
Old invocation retained its expected-email string argument.
All five non-identity guards passed normally; expectedIdentity=false,
rosterBound=false, authenticated=false. The final assertTrue(authenticated)
failed with exit 1, exactly the intended defect, not interface/import failure.

Command shape (under flock -w 600 /tmp/ama-rpi-heavy.lock, src/api):
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
/tmp/mv/bin/python -B - [external AST/HTTP/Node red harness].
Full output: external session files/identity-570/red.log.
No live raw claim or historical account identity was inferred.

### Corrected regression

Same real constructed auth-to-/me fixture and Node fetch seam, now invoking
new BINDING with independent expected-ID object. Initial focused command:
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
/tmp/mv/bin/python -B -m unittest test_employee_identity_check -v.
Seven tests passed, including multiple subcases; external green.log.
Additional strict GUID-newline, optional diagnostic-email and media-type
coverage added before final package validation.

Coverage includes missing/multiple/aliased display claims, display name/case,
optional bound/unbound roster, wrong tenant/object despite matching display
email, malformed expected IDs and observed schema/providers/role/view-only,
HTTP/redirect/media-type guards and fetch/abort/JSON canaries. Exact URL,
redirect:error, 120000ms AbortSignal and boolean-only results are asserted.
Faults return explicit transportFailed/jsonFailed booleans, not silent success.

Initial lint/type corrections were local formatting/import sorting and typed
heterogeneous invalid-fixture tuples; no ignores or dependencies added.
PC-003's explicit exceptional-output contract was implemented as planned.

### Diagnosis and limits

Confirmed runner contract error: display-email equality incorrectly
represented immutable Entra account identity. Original code already normalized
email case and never gated on rosterBound, so neither roster provisioning nor
case/display-name changes explain or fix that contract.
The historical boolean record does NOT establish missing versus duplicate
versus alias versus wrong-account claim, or serving-revision parity. No app
mapping bug is demonstrated; no historical requested-account acceptance.
The original Review, failed evidence and consumed two slots remain unchanged.
The guide supplies the owner-authorized next-attempt prerequisites.

## P02: Validation and Review

API full units passed under the exact requested shared flock/environment:
1368 tests in 503.341s, OK (skipped=318), exit 0. General discovery's skips
remain skips, not SQL/browser coverage or a successful complete gate.
External api-units.log retains full output.
Ruff check . passed, Ruff format --check . passed (60 files already formatted),
mypy passed (116 source files). External static.log preserves exact output.
Initial targeted lint/type failures were corrected before these final passes.
No successful full gate, live acceptance or human approval claimed.

### Original evidence integrity

All seven files compare byte-for-byte to HEAD; pre-Review hashes:

| File in original 1030c directory | SHA256 |
| --- | --- |
| acceptance.py | bfca66bdc4623e35c33f056497613592d417a3db3e98d61363b64bd2fe8e10ee |
| evidence.json | fe5f0dcb185774c2c62a5e036386ebf80b7cc936acd7c2bc737a9c57d0bafa4c |
| manifest.json | 099da77011f5b443f54435b563980187c81dbecc03441cb463ce3cc4ba460c19 |
| second/attempt2.py | 861d494e8665fa057d07534b5f1ce0bf3db6015d4b212b50b7a238d06596f356 |
| second/evidence.json | b0f9075b963a96cf2e4cb2cdf8a1cc5d599a2827368de91e9f1897f9155eaf6d |
| second/manifest.json | e6eaf7f62a0ea3eacf155d86670dce5db95cc4bfb4082a22e556e3cdb8630d10 |
| test_acceptance.py | 4cf4dd96886f1b6fd01a06516182361c768accf2307071a46b10a61bfabd9669 |

Fresh fetched origin/main and branch base both:
3d9d523df35e3a974e1586e23f3f6aa2d0447dbd.
No original evidence staged; only the plan's exact ten allowlisted paths.

### Remaining work and follow-ups

P02-T01 complete; P02-T02 awaits one Review, local commit
and external complete-gate attempt. No significant divergence or new user
decision; critique original Complete / Revise preserved, not repeated.
Follow-up owners and exclusions match plan: identity administrator/acceptance
owner for expected IDs, fresh budget and live chat/map/case; runner maintainer
for prior visibility/fault-path findings; model/accessibility owners for their
separate gates. No live activity is authorized by this repair.

### Pre-Review reconciliation

P01-T01/T02 and P02-T01 checked with completion evidence. P02-T02 remains
unchecked for Review/local persistence/full-gate attempt. Product change is
exactly two outside-package Python additions plus API guide; app auth/me,
infra and original evidence untouched. No plan amendment beyond direct
critique dispositions, no significant divergence, no second critique.
Required human approval stays unclaimed. One Review is next.

## Original Independent Review

Record:
.copilot-tracking/reviews/logs/2026-10-30/employee-identity-570-review.md.
Execution Complete; outcome Residual work. No implementation defect or material
decision gap found in this offline repair. Independently executed 42 Node
evaluations plus syntax/hash checks; full API/static logs inspected, not rerun.
Original Review is preserved without re-review or closure verification.

* RV-001 Medium: local persistence/full gate pending at review boundary.
  Parent continuation below owns this, not a source correction.
* RV-002 Medium: independently expected live identity and employee chat/map/
  case acceptance remain unestablished. Separate owner-authorized live work.
* RV-003 Medium: inherited visibility and fault-path runner defects remain
  separate later runner-maintenance work, not repaired by this predicate.
* RV-004 Low: enabled-model and direct human/AT acceptance remain separate.

## Local Persistence and Post-Commit Gate Handoff

Authenticated gh api user returned id 8036360, login jmservera. Author and
committer use repository-local 8036360+jmservera@users.noreply.github.com,
Conventional Commit, required Copilot coauthor and Refs #570 only.
Only the exact ten task paths are authorized for staging; all seven originals
remain HEAD-identical. No push, PR/issue mutation, live login or Azure action.
Git-commit skill's referenced message-instruction file and get_changed_files
tool are unavailable. Repository Conventional Commit/noreply/coauthor rules,
exact path staging and staged diff inspection provide the bounded fallback;
no broad add or history rewrite is used.

At this artifact freeze, P02-T02's original Review is complete; the immediately
following local commit and external complete-gate execution are parent-owned.
This committed record cannot contain its own final commit/receipt identity.
Final command and actual result will be retained outside the checkout under:
/home/azureuser/.copilot/session-state/3539d050-474b-4068-aa36-221cce5866bd/files/identity-570/
(final-gate directory, final-gate.log and closeout.json).

Command:
python3 tools/rpi-checks.py --all --base
3d9d523df35e3a974e1586e23f3f6aa2d0447dbd --lock-timeout 600
--out [external session files]/identity-570/final-gate.
Run directly: gate owns /tmp/ama-rpi-heavy.lock. Full gate outcome pending at
commit, not inferred from passing units; publication remains blocked until a
valid successful receipt and required human/hosted approvals. No push requested
or authorized. Any actual gate failure is preserved without unrelated repair.

## Parent Closeout Boundary

Research, Plan, Implement and exactly one independent Review have run in
order. Bounded offline implementation/review complete; local persistence
and post-commit gate continuation use the frozen handoff above. No whole
issue delivery: exact historical raw cause and live employee criteria remain
unknown/unverified. No new child task starts automatically.
Prioritized follow-ups match plan/Review: fresh expected-ID/owner budget and
guarded live acceptance; separate runner visibility/fault-path hardening;
separate enabled-model and human/AT acceptance.
