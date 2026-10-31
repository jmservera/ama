---
title: Employee expected identity and live acceptance research
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

Task #570, slug employee-identity-check-570. Convergence research for the
explicitly requested research, plan, implementation and review sequence.
Determine the remaining runner defect, preserve Entra-authoritative identity,
and prepare credential-safe live employee chat/map/case acceptance.

## Research Parameters

Focused, from the caller's bounded source and failure evidence.
Evidence root: .copilot-tracking/research/2026-10-31.
Candidate areas: src/api/checks, src/api/tests, historical employee runner
and identity evidence. External scope: issue/PR metadata and authorized
demo only. No Azure changes, no private datasets, no feature code in mvp.
At most two sign-in attempts; password read only inside automation and
never captured. Expected identity must come from independent evidence.

## Extensions and Participation

Repository guidance and rpi-research selected. Research specialists skipped:
one continuous runner-to-auth trace, no independent lane.
No UI changes intended; design skills not applicable. Caller explicitly
authorizes this full loop, commit, non-force push and main PR. No routine
confirmation required. Existing merged PR #574 is background, not current
acceptance. Explicit branch/base direction governs this clean worktree.

## Questions and Prior Knowledge Gate

* Q1: Which remaining runner uses display email as identity?
* Q2: Where can independently verified expected tenant/object IDs be obtained?
* Q3: How can the live checks execute safely with bounded attempts?

Prior 2026-10-30 research identifies a display-email predicate defect and an
already merged immutable-identity helper. Verify the current caller path
before proposing another mapping change. Historical artifacts are immutable.

## Research Cycle Log

Cycle 1, inline, in order:

* Wider: helper and HTTP regressions exist, but no maintained src runner
  invokes them. Historical runners still compare display email or merely
  accept any response with a user-like field. Reflection: repair caller
  integration, not application role mapping.
* Deeper: trace historical sign-in admission and chat/map/case selectors.
  Preserve origin checks, one submission per invocation, explicit failure
  results, no body/identity capture and independently supplied IDs.
  Read-only directory resolution failed with insufficient privileges.
  Reflection: live expected-account acceptance must not learn IDs from /me.
* Contrarian: current helper tests already reject wrong tenant/object despite
  equal email; no evidence of application authorization defects. Historical
  browser checks use synthetic sign-in and cannot stand in for Entra live
  acceptance. No independently verified object ID exists in the searched
  scoped evidence. Reflection: implement a maintained fail-closed runner,
  prove integration locally, and report live checks blocked if directory
  evidence remains unavailable.

Parent synthesis: accepted caller integration gap; rejected roster provisioning
and HTTP/role-only admission. Deferred actual live acceptance until independent
expected object ID is available. No further cycle: directory access is a
concrete external prerequisite, not an uncertainty resolvable by code research.

## Evidence Log

* C1: src/api/checks/employee_identity_check.py:3: immutable GUID checks exist;
  display email and roster binding are diagnostics only.
* C2: src/api/tests/test_employee_identity_check.py:142: regression already
  covers a correct rosterless account with absent display email.
* W1: https://github.com/jmservera/ama/pull/574, retrieved 2026-10-31:
  merged repair deliberately performed no live retry.
* C3: .copilot-tracking/changes/2026-10-30/live-acceptance-1030c/acceptance.py:28:
  old predicate gates on account.email, not tenant/object.
* C4: .copilot-tracking/changes/2026-10-30/employee-password-acceptance/employee_acceptance.py:144:
  alternative old probe admits any user-like field, insufficient verification.
* C5: src/api/README.md:19: independently verified expected IDs are required
  before attempting sign-in, never copied from the observed response.
* C6: src/api/checks/employee_chat_browser_check.py:148 and
  src/api/checks/employee_workspace_browser_check.py:30: local synthetic
  browser selector patterns, not live Entra proof.
* W2: authorized read-only `az ad user show --id <authorized-test-upn>` on
  2026-10-31: insufficient privileges. Independent object ID unavailable.
* W3: authorized demo /healthz on 2026-10-31: HTTP 200 after warming.

## Findings, Alternatives and Current Decisions

Use the merged immutable helper in a maintained src/api/checks runner with
mandatory expected IDs and external sanitized output. Add real Chromium
caller-integration regression against constructed actual /me payloads.
Historical runners and evidence remain unchanged. No identity mapping change.
No UI source edits or web guideline review needed: automation only.

Cause identified at the contract level, not a reconstructed historical raw
claim: mutable/optional display email was used as identity authority.
Actual Aadi object ID and historical mismatching claim remain unknown.
Local engineering completion cannot establish live acceptance.

## Planning Readiness

Ready for the bounded runner repair. Research disposition: executed, complete.
Live validation is separately blocked by unavailable independent expected
object ID; no credential file has been read and no sign-in attempt consumed.
Parent continuation: Plan, one independent critique, Implement, one Review.
