<!-- markdownlint-disable-file -->
# RPI Changes: Grant lifecycle controls

## Metadata

Task ID 95; slug grant-lifecycle-controls-95; implementation date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md.
Details: .copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md.

## Execution Status

Complete implementation, full-plan scope P01. P01-T01/T02/T03 complete.
Independent Review remains the next parent lifecycle gate.
Research complete and Ready; one independent critique executed, original Revise
retained, PC-001 through PC-006 directly resolved in current plan/details.

## Execution Summary

Existing states verified, not rewritten. Actual fail-before synthetic JSON and
SQLite probes accepted unregistered role-only grant writer, same-code alias
approval and silently ignored USD. Critique exposed application award wording
and missing event evidence; narrow UI correction included without redesign.

## Implementation-Time Plan and Detail Updates

All six critique dispositions are compatible local corrections. Exact
state/case/route human-exercise designation, fresh UTC validity at commit,
funding history, legacy pending re-proposal and path-specific fault tests are
required. Web guideline source fetched fresh 2026-10-17; no generic aesthetics
or WCAG acceptance inferred. No second critique.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| Research probes | Failed as intended | JSON/SQLite unauthorized acceptance, alias approval, USD ignored |
| Source packages | Installed | worktree .venv, pip editable core/dev/sql, agents/dev, api/dev |
| Failing-first regressions | Failed as intended | 22 tests, 39 failed subtests/23 errors on original source; probes separately confirmed actual unauthorized behavior |
| Focused regressions | Passed | 84 tests, one opt-in browser skip, before added recovery fault case |
| Core quality gates | Passed | Ruff check, format, mypy 112 source files |
| Focused final grant/finance/API/browser | Passed | 89 tests, no skips, 38.769s; actual local Chromium missing-evidence refusal and neutral confirmation |
| Full core discovery | Failed, repairing linked hash | 718 tests, 33 skips, two scenario-manifest stale source digest errors after dataset.py test-only fixture adaptation |
| Full API discovery | Passed | 588 tests, 121 skips, 347.576s, browser enabled; logs explicitly mark absent law-store checks unknown |
| Actual final SQL Server parity | Passed | 34 tests (15 grant, 19 preserved finance), 162.730s; responsive task-owned loopback container zf-grant95-ef8f1fc88d01 removed |
| API quality gates | Passed | Ruff, format and mypy 52 source files |
| Manifest integrity repair | Passed | All eight existing scenario-manifest tests; no coverage statuses changed |
| Full final core discovery | Passed | 724 tests, 35 explicit skips, 230.155s after digest repair |
| Final changed-label API/browser | Passed | 2/2, 6.458s after visible evidence label |
| Existing migration regressions | Passed | 25/25 after missing python-pptx/Pillow/PyYAML restored in local venv only |
| Independent Review | Executed Complete, Not accepted | RV-001 High: legacy preparer fallback frozen before transaction revalidation; four independent grant/finance code/OID probes wrongly committed |

## Completed Work

### P01-T01/T02: Authority and evidence isolation

Extracted #94's unchanged operation rollback boundary for grant/application reuse;
SQL validation repeats scoped designation and fresh time checks. Grant approval
captures independent email/code/OID, GBP and exact case/scheme/source/authority.
Application approve/submit/confirm append event-specific source and actor/authority.
Legacy unknown-currency pending proposals require withdrawal/re-proposal.
No production staff designation, schema, payment adapter or external action added.
New fixture authority is explicit, synthetic and isolated from shared STAFF/DATA.

Browser first attempt hit the welcome page, not `/app`; corrected harness route.
Actual changed UI assertions then passed, but deferred browser.close ran after
Playwright shutdown and failed cleanup; corrected to close inside the context.
Neither failed harness run is counted as a passing browser run.

### P01-T03: Source hash reconciliation

Full core discovery correctly rejected the old public `dataset.py` digest in
the existing #103 scenario manifest. The only dataset.py change is explicit
test-only exercise authority/evidence for existing funding success tests; DATA,
case selection, continuing 60,000-home data and journey coverage are unchanged.
Refreshed that one source digest from actual SHA-256. This is a tightly coupled
integrity repair, not new coverage or a changed acceptance claim. No new critique
needed; independent Review must see the refreshed digest and retained limitations.

### Scoped web guidelines check

Fetched the current source before edits and refreshed before review on 2026-10-17.
Reviewed changed fundingPanel controls/copy against all applicable fetched rules;
native buttons, labelled uncontrolled input, name/autocomplete/spellcheck and
status-region errors are retained. No style, motion or navigation changes.

src/api/src/zava_forward/api/web/app.js:885 - existing shared refresh reports
errors in the case status region, not field-inline with first-error focus;
broader async/focus/unsaved-draft behavior remains pre-existing UI debt.

This is a scoped changed-surface review, not a fresh complete review of all
app.js panels or WCAG conformance. Actual Playwright checks missing evidence,
successful neutral confirmation and retained Opportunity history, not human
task comprehension or full accessibility acceptance.

## Pre-Review Reconciliation

Ready. Plan markers/details/changes and guides/index/log are current. All
implementation tasks complete; no source work remains before independent Review.
All requested local checks passed with explicit suite skips retained. Source
hash repair and failed harness/dependency attempts are not hidden. DATA AST,
original case and owner memory are unchanged; KB log remains exact old prefix.

## Blockers

None for synthetic engineering. Real delegation/human/live-platform acceptance
not supplied and not claimed.

## Follow-Up Items

Full PRD pack/export/version workflows and real verified delegation remain
outside these two issue criteria; canonical plan owns follow-up scope.

## Coordinator-authorized correction ONE: RV-001

The one independent Review returned **Not accepted**, preserved unchanged in
the review record. It found that returning resolved legacy identity for history
also accidentally replaced the absent identity in transaction validation. That
prevented the #94 fallback from rereading current persisted preparer identity at
commit. This is an in-scope fixable regression, not a human permission blocker.
Coordinator explicitly authorized correction ONE. Routed later implementation
will restore the original unresolved-versus-captured validation distinction,
add failing-first grant and preserved-finance code/OID rebinding regressions,
and retain original verdict. No second Review or independent Pass is authorized
or claimed. External coordinator owns the final independent gate.

Failing-first RV-001 regression executed one semantic test with all four
grant/finance x code/OID subtests failing because PermissionError was not raised.
Root correction changes only the validation-context identity back to the
original supplied identity (including absence), while the resolved entry
identity remains available for event history. This restores the original #94
legacy lookup inside the SQL writer transaction without weakening captured
historical identities or changing current actor/designation checks.

P02-T01 is complete. Post-correction combined grant/finance/API/actual Chromium
and eight scenario-manifest tests pass: 98 tests, no skips, 61.115 seconds.
Actual local SQL Server passes 35 tests (16 grant including the new four-way
legacy regression, 19 preserved finance), 228.464 seconds. Task-owned loopback
container zf-grant95-74996418b02e and its UUID databases were removed. Core/API
Ruff, format and mypy pass for 112/52 source files. Absent-law-store warnings
remain explicit unknowns, not legal acceptance.

Earlier full discovery (core 724/35 skips, API 588/121 skips) and migration
25/25 remain pre-correction evidence, not a claim they were rerun after the
one-line restoration. Current targeted suites cover the changed validation
boundary on SQLite and actual SQL Server, both grant and preserved finance.
Correction source and regression are complete; no implementation blocker.
Original independent Review execution Complete / outcome Not accepted is
unchanged. Local RV-001 closure evidence is not independent Pass. Coordinator
retains final independent gate and merge; no second Review executed.

P02 planning maintenance is an immediately relevant update explicitly selected
by coordinator, not a new architecture or acceptance decision. Plan markers,
phase details, changes and state reconcile the original adverse outcome and
authorized later implementation. P02-T02 publication remains active until
normal push, main-targeted PR and clean remote-head verification.

## Publication and explicit stop boundary

P02-T02 complete. Fresh gh account resolution set repository-local privacy-safe
author/committer identity. Source, documentation and all seven task artifacts
committed as a82da8d1d8f2e912330af76d47ad143f24309eca with Conventional Commit
and required Copilot trailer, pushed normally and published as open main-targeted
PR #386: https://github.com/jmservera/ama/pull/386. Local, remote and PR source
heads match and worktree was clean; final publication metadata is committed
separately and final head reverified before return.

Original Review SHA-256 remains
e20213f915717975739159925319ce290d13180d8938e2e5e5c5fba76db2e22b.
Original Complete / Not accepted retained; no second Review or independent Pass.
Initial PR check rollup was empty, not a CI pass. Coordinator final independent
closure, checks and merge decision remain. No merge, rebase, force push, issue
closure or new child work. Explicit stop-at-clean-pushed-PR instruction ends the
automatic session, not an invented follow-up selection.

Original resume ID: 24912f4a-8570-4de8-ad93-fe62376fb3f1.

## Authorized latest-main integration after completed publication

Coordinator explicitly authorized rebase only after the full loop, correction
and publication. Started with clean topic at
6692a97632ac2b4a2189c7a3c1c8bbf8b32918d9, also the expected remote lease.
Fresh fetch verified latest origin/main
1fc7325b93ea845b9cb2e827efbea624f7d20d30 and merged PR #385. This base also
includes #384 provider-capacity controls, not just documentation/infra.
Previous base was d400eb8d1d0d6567445b0fc11803260eab897a65.

Rebased both run-owned commits onto that exact fetched main. Source, tests,
component guides and index merged automatically; no blind side selection.
Two manual conflicts:

* KB log: retained entire upstream exact byte prefix, then original own entries.
* Scenario manifest fixture digest: retained all upstream metadata and replaced
  only digest with actual combined dataset.py SHA-256
  cdc3beba9fb6ff5dac05ac5db3222ac5e8df243d74da72a1386b870cb41747c9.
  Neither side's old digest could describe the combined public test source.

Exact added/removed byte comparison of the entire own src patch, old base/head
versus new base/head, passed for all 12 production/test/config/component-guide
files, with identical changed file sets. Shared Store, app.js and dataset
therefore retain both upstream intent and unchanged own edits; upstream
SQL/procurement protections were not overwritten. Whole manifest structured
comparison to upstream differs only by fixture digest: no authority, status,
coverage or approval promotion. All upstream Inspect/Audit index routes remain.
Original case/addendum/memory exactly match upstream; KB prefix and original own
log suffix proved. Rebased source head before this evidence commit:
ae81ea0651a39ab9e86b5d3955c57099a8c2a4a6.

Fresh integration validation: 156 tests pass, no skips, 47.330 seconds, combining
grant, preserved finance, procurement, API, actual Chromium and manifest checks.
Core/API Ruff/format/mypy pass: 112/54 source files. Diff whitespace clean.
No transaction implementation was changed by conflict resolution: actual SQL
Server 35/35 remains the earlier correction evidence, not a fresh integration
rerun. Earlier full discovery and all prior counts remain historical.
Absent-law-store messages remain explicit unknowns. No new full Review or
independent Pass; original adverse Review and its phase history remain intact.

Final evidence/state commit follows privacy-safe fresh identity and required
trailer. Publish only this topic with explicit expected-remote lease
6692a97632ac2b4a2189c7a3c1c8bbf8b32918d9, update PR #386 integration receipt,
verify clean local/remote/PR final head, then stop. Coordinator retains final
independent closure/checks/merge. No main write, merge, issue closure, Azure
action, authority change or other issue's finance implementation.
