---
title: Issue 350 feedback correction4 research
description: Strict JSON type contract research for the final authorized correction
ms.date: 2026-10-22
---
<!-- markdownlint-disable-file -->

## Research Brief

Status: Complete. Research disposition: executed. Output mode: convergence.
Focused posture selected from the owner's bounded failure report.
Evidence root: `.copilot-tracking/`.

Investigate only account name/email/provider and map tiles/attribution JSON
types in the checker against the actual server/auth contract. Audience: the
coordinator's independent assessment. Writes are limited to
`tools/check-demo-feedback.py`, `tools/test_check_demo_feedback.py` and this
task's dated correction4 artifacts/state.

## Direction Controls and Participation

The owner explicitly requested one complete Research, Plan, Implement, Review
loop in this invocation, citing authorization at
https://github.com/jmservera/ama/issues/350#issuecomment-6351734485.
The authorization is supplied by the caller, not independently fetched because
network actions are excluded. Start HEAD:
`05b5b7d2b754ae0e7134df8db1a867861726a821`; required base:
`b4d467cad84535ed106cffa1ae9aa303db7bfed2`.
Branch: `test/deployed-feedback-harness-350`; clean at intake, including ignored
inputs. No push, PR update, issue closure or acceptance-checkbox changes.
PR #436 must remain draft and issue #350 open.

No Azure, tenant, credential, live-data or live-endpoint actions. The separately
requested authenticated `gh api user` identity lookup is conditional on passing
gate/receipt verification before commit. No private datasets will be read.
All test evidence is local synthetic engineering evidence, not deployed,
SQL-durable, AI-live, Azure, tenant or human acceptance.

## Extension Registry and Prior Knowledge Gate

* Selected `.github/copilot-instructions.md`: repository evidence and gate rules.
* Selected `rpi-research`: focused inline wider/deeper/contrarian cycle.
* RPI phase skills will be activated in the owner's requested order.
* Research specialists skipped: one tightly coupled trace, no independent lane.
* Web/design skills skipped: no web implementation or UI review.
* Required original case study, addendum, reference index and memory inspected.
* Correction3 plan, details, critique, changes, review and state located for
  detailed inspection; prior 58-test/Ruff claims are not correction4 evidence.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What exact JSON types does the actual runtime emit? | Answered C1-C3 |
| Q2 | Which valid empty/null values must remain accepted? | Answered C2-C3 |
| Q3 | Can commit-after-gate meet the exact-HEAD clean-input gate contract? | No, C4 |

## Research Cycle Log

### Cycle 1: Wider

Located the checker, focused tests, server, auth module, correction3 artifacts,
and full-gate implementation. Initial reflection: the missing type checks appear
localized, but clean exact-HEAD gate sequencing requires explicit investigation
before any commit.

### Cycle 1: Deeper

Read correction3 plan/details/critique/changes/review/state in full. Its critique
was post-implementation, original review residual work remains, and its state
still names Implement/P03. This correction4 is a distinct explicitly authorized
task, not a rewrite or acceptance of those artifacts.

Read `check_me`, both provider `account` implementations, `tile_config`, the
`/api/me` handler, focused fixtures, and gate preflight. Reflection: exact key
checks do not validate account name/email or either map value. Provider already
uses `nonempty_str`, which rejects wrong types and must not be weakened.

### Cycle 1: Contrarian

Challenged a blanket nonempty/nonnull rule against production tiles and proxy
email fallback. Both are legitimate counterexamples: production with no tile
configuration emits null URL and empty attribution; trusted proxy may emit empty
email. No URL, email-format, HTML or name-content restriction is warranted.
Existing provider nonempty and deployed trusted-proxy rules remain unchanged.

Challenged the proposed gate/commit sequence against actual `clean_identity`:
tracked modifications or untracked artifacts are refused before lock acquisition,
output creation or checks. The gate snapshots committed HEAD; staging is not a
solution, and committing after verification would invalidate the receipt.
Reflection: correction and focused validation can proceed, but publication is
blocked under the explicit no-pre-gate-commit direction. Invoke exactly one
unchanged gate command as requested; preserve its real failure rather than
fabricate a receipt, hide inputs or validate the old HEAD.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Server assigns provider account and configured map values directly | src/api/src/zava_forward/api/server.py:365-372 | High |
| C2 | Account fields are strings; proxy claims filter strings and email fallback is empty | src/api/src/zava_forward/api/auth.py:91-92,136-141,174-179 | High |
| C3 | Production without tile URL returns null URL and empty attribution; configured values are strings | src/api/src/zava_forward/api/server.py:47-57 | High |
| C4 | Gate rejects dirty/untracked inputs, binds exact committed HEAD and current local origin/main | tools/rpi-checks.py:149-175,1693-1727 | High |
| C5 | Missing field-type checks are localized; provider restrictions already exist | tools/check-demo-feedback.py:247-261 | High |
| C6 | Existing contractor fixture has empty email; tests import installed runtime builders | tools/test_check_demo_feedback.py:19-22,63-71,275-339 | High |

No external sources fetched. Authorization provenance is the owner request,
not independently retrieved issue content. Local `origin/main` equals the
required base; no fetch performed under the no-network boundary.

## Findings, Alternatives and Current Decisions

Q1/Q2: accept strict string checks for name/email, retain provider check, accept
only null-or-string tiles and string attribution (C1-C3/C5). Reject blanket
nonempty constraints and URL/email/content checks as unsupported. Focused tests
must mutate every field through all non-string JSON types for staff/contractor,
except valid null tiles, and retain valid empty contractor email.

Q3: pre-gate commit conflicts with owner sequence (C4). No commit will be made
unless the requested gate and exact receipt verification actually pass. This is
a publication blocker, not a reason to skip the narrow implementation.

## Parent Synthesis and Re-entry

Accepted C1-C6. No independent research delegation: evidence is a single compact
trace. Scope questions are answered; another cycle cannot resolve the explicit
commit-order conflict. Wider, deeper and contrarian waves executed inline.

## Risks and Further Research

The focused module is outside the full gate matrix (prior correction evidence);
run it directly. Prior adverse outcomes and whole-issue acceptance remain
unchanged. Required full gate is expected to refuse dirty input. No live runtime
or original acceptance evidence is obtained. No further source research needed.

## Planning Readiness

Ready for bounded implementation and focused validation; publication blocked by
commit-order conflict C4. Research self-check: Q1-Q3 answered, evidence and
counterexamples recorded, scope preserved. No source edits in Research.
Next action: parent continues to Plan, with gate blocker retained.
