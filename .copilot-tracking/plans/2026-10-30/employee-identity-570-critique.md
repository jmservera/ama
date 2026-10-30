---
title: Employee acceptance identity final-candidate plan critique
description: One independent bounded assessment of the identity predicate repair plan
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: employee-identity-570-2026-10-30.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/employee-identity-570-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/employee-identity-570-phase-details.md.
* Critique execution status: Complete.
* This is the ONE independent final-candidate critique. No delegation occurred.

## Inputs and Criterion Boundary

* Assessed the complete supplied plan, phase details, primary research C1-C8
  and task state; original acceptance.py, test_acceptance.py, second/attempt2.py,
  second/evidence.json and the original live-acceptance-1030c Review.
* Checked relevant supplied implementation and contracts:
  src/api/src/zava_forward/api/auth.py,
  src/api/src/zava_forward/api/server.py,
  src/core/src/zava_forward/core/identity.py,
  src/api/tests/test_auth.py, src/api/tests/test_entra_authoritative.py,
  src/api/pyproject.toml, src/api/README.md, src/README.md and
  tools/rpi-checks.py. Read the tenant staff initialization section of
  infra/README.md rather than assuming research line numbers remain current.
* Read the required project context documents. Read-only GitHub inspection
  confirmed issue #570's three criteria and no matching existing PR for
  fix/employee-identity-check-570. The worktree already contains four untracked
  parent-owned planning/state artifacts; this critique does not move or stage them.
* Confirmed authority: full RPI sequence and local commit, Refs #570 only.
  No push, issue mutation, live sign-in, private test-user file reads, Azure
  changes or deployment. Future runner integration and owner budget are
  explicitly outside this repair.
* Assessed all requirements, phases, tasks, dependencies, tests, ownership,
  acceptance claims and gate handoff once. This assesses plan credibility,
  not implemented correctness, real-user identity, serving-revision parity,
  live feature acceptance or human approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C1-C2/C8; historical diagnosis | Covered | Original predicate compares display account.email; retained booleans identify a failed equality, not the actual raw mismatch or historical account. |
| Research C3-C7; application boundary | Covered | Auth and identity already use tenant/object identity; roster metadata is optional. No mapping change is justified. |
| P01-T01; independently expected identity | Covered | Expected IDs must be separately verified, never copied from observed /me; same-email wrong-object and wrong-tenant negatives are explicitly planned. |
| P01-T01; failing-before proof | Partial | Constant substitution can fail solely on changed argument shape; PC-001. |
| P01-T01; HTTP-to-Node test placement | Covered | Real constructed App/HTTP response feeds Node's fetch stub; tests stay outside the installed package and do not inherit another test class. |
| P01-T01; schema/provider/role/view-only | Partial | Existing guards and negative categories are retained, but exceptional transport/JSON paths and request-contract assertions are unspecified; PC-003. |
| P01-T02; future integration and budget | Covered | Identity administrator supplies verified IDs; acceptance owner authorizes a fresh budget and guarded runner. No ready-to-run sign-in entry point or third historical attempt is authorized. |
| P02-T01; commands and runtime | Partial | API unit environment and Ruff/mypy commands are specified, but temporary-path assumptions conflict with current execution limits; PC-002. |
| P02-T02; original evidence and local persistence | Partial | Immutable history and local-only commit are explicit; exact new evidence ownership/commit allowlist remains incomplete; PC-004. |
| P02-T02; complete external gate | Partial | Correct post-commit full-gate intent and external results boundary; blocked execution constraints need explicit handling, PC-002. |
| Issue #570 acceptance | Covered with limits | Offline defect characterization and regression can support a bounded repair, not recover historical raw cause or prove live chat/map/case. Refs-only is mandatory. |

## Verdict

* Verdict: Revise.
* Severity: 0 Critical, 2 High, 2 Medium, 0 Low.
* The selected repair is credible and appropriately bounded. Revise the
  causal red-test protocol, validation feasibility, exception/request tests
  and evidence ownership before implementation. Missing current execution
  prerequisites block those checks, not this completed assessment.
* No significant or divergent product decision is required. Do not expand
  scope to a live runner, sign-in retry, roster provisioning or auth repair.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Constant substitution can produce a false failing-before proof

* Related IDs: P01-T01; first acceptance criterion; research C1.
* Evidence: Historical acceptance.py BINDING calls expected.toLowerCase().
  Phase details permit replacing only the new constant with that historical
  constant. The new interface takes expected tenant/object IDs rather than
  the old display-email string.
* Concern: The proposed red experiment does not require the historical
  invocation to retain its old argument shape. A TypeError, import failure,
  output-key mismatch or unavailable Node could be recorded as the required
  regression failure without exercising the display-email defect.
* Impact: Failing-before evidence could establish interface incompatibility
  rather than the reason the runner rejects a legitimate rosterless identity.
* Smallest useful change: Specify a test-only red harness that passes a
  synthetic expected-email string to the inertly extracted historical
  predicate and an independently defined expected-ID pair to the new one.
  Feed both the same actual constructed HTTP /me payload. Assert the old
  predicate executes normally, responseOk/schemaValid/providerMatches/
  employeeRole/notViewOnly are true, expectedIdentity and authenticated
  are false, and rosterBound is false. Make the intentional failing assertion
  be expected authentication for that legitimate fixture, then prove the
  corrected predicate passes. Reject harness/environment exceptions as red
  proof; retain no production legacy selector.
* Action owner: Planning parent specifies the protocol; implementer records it.
* Exact resolving evidence: Revised P01-T01 names the two invocation shapes,
  assertion and commands; the changes record later contains a deliberate
  assertion failure and matching green result on the same HTTP-derived
  fixture, not an exception traceback counted as success.
* Decision route: Direct planner correction; no user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Validation assumes paths prohibited by the current execution boundary

* Related IDs: P02-T01, P02-T02; validation acceptance criteria.
* Evidence: Details prescribe /tmp/mv tools and
  flock -w 600 /tmp/ama-rpi-heavy.lock. Reused test_auth.Base creates
  tempfile.TemporaryDirectory() without a selected directory.
  tools/rpi-checks.py heavy_lock itself opens /tmp/ama-rpi-heavy.lock;
  its main also requires a new output directory outside this worktree.
  Current execution constraints prohibit temporary-directory operations and
  do not authorize arbitrary external artifact writes.
* Concern: The plan says no unresolved local decisions but gives no blocked
  path for this known conflict. Changing only TMPDIR or only --out would not
  repair the hardcoded shared lock. A different private lock would not
  coordinate with the required shared lock.
* Impact: The parent could execute a prohibited operation, bypass resource
  coordination or claim an unperformed gate. The original Review explicitly
  warned that a historical disposition cannot authorize later execution
  outside the later process's own constraints.
* Smallest useful change: Keep the requested shared-lock/API-unit and complete
  gate contracts unchanged, but state their current execution blocker before
  invocation. Use only a permitted durable runtime and approved fixture/output
  locations where independently available; do not silently substitute another
  lock, rewrite gate tooling or use a cloud fallback. Where no compliant path
  exists, record the exact not-run commands and blocker in changes/state,
  complete only feasible checks, and leave full validation and acceptance
  blocked. Invoke the full gate directly when eligible: it owns its shared
  lock, so do not wrap it in another acquisition of the same lock.
* Action owner: Planning parent owns the correction and honest execution
  disposition; the acceptance coordinator owns later compliant gate execution.
* Exact resolving evidence: Revised validation details distinguish runnable
  checks from blocked commands, identify permitted locations only when
  established, and define the blocked closeout. A passing gate claim requires
  the actual clean committed head/base, external full receipt and verification;
  otherwise record no successful receipt. No prohibited probe is needed.
* Decision route: Direct planner correction within existing constraints.
  Current user direction already resolves no-push/no-live scope; no new
  budget or user waiver is requested.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The transport failure envelope does not cover rejection and parsing faults

* Related IDs: P01-T01; functional fail-closed and boolean-only requirements.
* Evidence: Details enumerate redirects, content type and non-200, but not
  rejected fetch, timeout/abort, rejected r.json() or malformed JSON.
  The historical predicate lets await failures escape. Node stubbing can
  return a good payload even if the request URL or redirect policy regresses.
* Concern: "Each HTTP/schema guard" does not explicitly establish whether
  these failures return boolean-only unauthenticated results or reject the
  evaluation. An exception can cross the boundary with string diagnostics,
  contrary to the new no-string-output promise.
* Impact: Happy-path and status-mutation tests could pass while a future
  guarded runner receives an exception instead of a safe admission decision,
  or silently loses same-origin/redirect controls.
* Smallest useful change: Require the predicate to return boolean-only
  unauthenticated results for synthetic fetch rejection/abort and JSON
  parsing rejection. Add canary-bearing errors and assert neither returned
  fields nor captured process diagnostics emit their contents. Have the stub
  assert exactly /api/me, redirect:error and the bounded abort signal.
  Include invalid top-level/user/account shapes and malformed app_roles
  elements even when a valid ProgrammeManager string is also present.
  Keep the existing independent provider, effective-role, app-role and
  strict false view_only negatives; correct IDs must not override any guard.
* Action owner: Planning parent specifies the failure contract; implementer
  adds the cases within the two already owned additions.
* Exact resolving evidence: Revised P01-T01 lists these fault/request
  assertions and expected boolean-only outcomes; the outside-package Node
  regression later passes them without live transport or browser launch.
* Decision route: Direct planner correction, implementing existing stated
  fail-closed/privacy requirements; no user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The local commit's evidence allowlist and Review output owner are not exact

* Related IDs: Scope and Non-Goals; P02-T02; original-evidence preservation.
* Evidence: Plan fixes two Python additions and one guide edit, but describes
  additional outputs as "dated phase/state evidence." P02-T02 says "commit
  exact allowlist" without listing it. Changes has a reserved path; Review
  has no reserved path, and the state currently has null Review/critique paths.
* Concern: The authorized RPI loop necessarily adds research, plan, details,
  this critique, changes, state and one Review, not only phase/state files.
  There is no single exact path set for reviewer ownership, reconciliation
  and staging in the already dirty worktree.
* Impact: A broad add could include unrelated or historical material; a
  narrow literal allowlist could omit original required evidence from the
  candidate before the complete gate. This is a persistence gap, not a
  request for extra source files or another assessment.
* Smallest useful change: Enumerate the three product paths and every
  authorized dated evidence path, reserve the one Review destination, and
  assign parent/reviewer ownership. Explicitly exclude all seven original
  1030c paths and external logs/receipts. Require pre/post hashes for those
  seven originals and an exact staged-path comparison before the local
  authenticated noreply commit. Do not stage pre-existing artifacts merely
  because they are untracked; identify them as this task's authorized inputs.
* Action owner: Planning parent.
* Exact resolving evidence: Revised scope/details contain the complete
  workspace-relative allowlist and Review destination; later changes/state,
  original Review, staged names and seven unchanged hashes reconcile with it.
* Decision route: Direct planner correction under the already authorized
  full RPI/local-commit direction; no user decision.

## Strengths and Residual Risk

* The repair targets the expectation contract, not application authorization.
  Both auth.py and identity.py establish that display claims are not identity.
  The original predicate already trims/folds email and does not gate on
  rosterBound, so neither a case-only fix nor roster initialization addresses it.
* The planned wrong-object and wrong-tenant negatives use matching display
  email. Together with separately verified expectations, these prevent
  "any role-bearing 200" from becoming the replacement admission rule.
* Tests use real synthetic auth-to-HTTP projections before the Node seam,
  remain outside zava_forward/api and add no dependencies or live entry point.
* Future ownership is sufficiently bounded: owner/identity administrator
  verifies expected IDs; acceptance owner authorizes budget and guarded-runner
  integration; runner maintainer retains original RV-002/RV-003; model and
  accessibility owners retain their separate acceptance work.
* Two historical employee slots remain consumed. No attempt quantity or
  future financial budget is invented. This task authorizes zero live attempts.
* Local commit must retain Conventional Commit, authenticated repository-local
  noreply author/committer, Copilot trailer and Refs #570 only. Complete gate
  output stays external after the frozen commit; later changes invalidate it.
  No publication, hosted approval or human acceptance is inferred.

## Questions or Blocking Evidence Gaps

* No user question is required for these planner-owned revisions.
* Actual historical raw claims, requested-account equality and serving
  revision remain unknown. Synthetic regression cannot resolve them.
  Record issue #570's historical-cause criterion conservatively and leave
  its live chat/map/case criterion unmet; do not claim whole-issue delivery.
* Current validation-path constraints are an explicit execution blocker,
  PC-002, not permission to change controls or expand this repair.

## Limitations

* Read-only assessment; only this critique file was written. No credential
  reads, browser launch, live app request, Azure change, source edit, commit,
  push, install, test scratch directory or gate execution occurred.
* Independently executed an in-memory AST extraction and Node fetch-stub
  experiment using the exact historical BINDING. With a synthetic absent-email
  payload and old string argument, every existing non-identity admission
  guard was true and expectedIdentity/authenticated were false. Passing a
  new-shaped object instead produced TypeError. This supports PC-001; it is
  not the planned real-HTTP failing-before proof or an implementation result.
* The supplied original Review's adverse outcomes remain unchanged. No
  second critique or retrospective acceptance is performed or requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Revise P01-T01's causal red-test protocol, then resolve
  PC-002 through PC-004 in plan/details with explicit dispositions and blockers.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/employee-identity-570-plan.md](.copilot-tracking/plans/2026-10-30/employee-identity-570-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-30/employee-identity-570-phase-details.md](.copilot-tracking/details/2026-10-30/employee-identity-570-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-30/employee-identity-570-research.md](.copilot-tracking/research/2026-10-30/employee-identity-570-research.md) | Primary evidence synthesis |
| [.copilot-tracking/plans/2026-10-30/employee-identity-570-critique.md](.copilot-tracking/plans/2026-10-30/employee-identity-570-critique.md) | This original Complete / Revise critique |

## Next Steps

The active planning parent revises and records dispositions directly, preserving
this original critique without another critique pass. Continue the authorized
loop only within the recorded constraints; report blocked validation honestly.
No user action is required. This reviewer stops after the critique.
