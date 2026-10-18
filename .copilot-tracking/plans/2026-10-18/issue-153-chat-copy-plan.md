<!-- markdownlint-disable-file -->
# RPI Plan: issue-153-chat-copy

## Task Metadata

* Task ID: 153
* Task slug: issue-153-chat-copy
* Plan date: 2026-10-18
* Planning status: Ready; one critique executed with Revise, all findings disposed
* Phase details: .copilot-tracking/details/2026-10-18/issue-153-chat-copy-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-18/issue-153-chat-copy-plan-critique.md

## Executive Summary

Extend the existing copy audit to case chat/alerts, replacing application-owned
hold and snapshot wording while preserving safety restrictions and human restart
authority. Align the lexical vocabulary with the written standard and exercise
the actual local app. This is a partial #153 delivery, not issue acceptance.

### What You May Not Know

Adding snapshot/envelope exposes three coupled time labels in app.js. Raw
technical JSON and source/user/model content must not be rewritten. The audit
is a conservative regression guard, not a visibility parser or human assessment.
Named resident-wording review is still absent. No semantic/authority blocker.

## User Decisions and Requirements

* Full ordered Research, Plan plus one independent critique, Implement, one
  original independent Review; preserve adverse records, at most two separate
  correction receipts, never repeat the original Review.
* Use supplied isolated branch/base. Commit all task artifacts, push and create
  a main-targeting PR with Refs #153; do not close the issue, mutate boards,
  merge, rebase or force-push. Stop after publication for coordinator review.
* Correct only application-owned wording using established safety concepts;
  preserve exact AI label, manual paths, unknowns and human/resident boundaries.
* Validate locally before publication; no private data, Azure/IAM/Graph,
  production, external inference or spend.

## Goals

* Prevent reintroduction of the observed chat labels without corrupting sources
  or changing behaviour.
* Record exact audit scope and unmet acceptance gates in the existing KB.

## Scope and Non-Goals

Included: chat.js, three coupled app.js labels, test_content_standard.py, existing
regulatory_ux_check.py, content-standard.md, KB index/log and task RPI artifacts.
Excluded: server/domain/safety logic, roles, persisted keys, source quotations,
new screens/styles/frameworks, all other issue work, resident approval.

## Functional Requirements

* Replace "decide a hold" with explicit authorised-human restart-decision
  guidance and "release a hold" with "restart stopped retrofit work".
* Replace "Check snapshot" with "Check recorded at"; restored-history status
  must say records remain historical and require a new lookup.
* Include chat.js in the existing lexical guard; add singular/plural
  snapshot/envelope to its regex. Preserve narrow identifier and raw technical
  detail exceptions; do not exempt whole files or rendered guidance lines.
* Add glossary time/payload wording and a dated audit boundary; preserve all
  existing content, named human review gap, and KB index/log history.

## Non-Functional Requirements

* No changed executable statements in production JS except string values.
* Native semantics, Fluent foundations, live regions, safety routes and reduced
  motion remain unchanged. Runtime checks are engineering evidence only.
* Original critique and Review become immutable on completion; any correction
  gets a new receipt, never edits those artifacts.

## Acceptance Criteria

* All four identified chat phrases and three coupled app time labels are
  corrected in application-owned copy, not rewritten dynamic content.
* Regression detects restored bad labels, all six prohibited vocabulary families
  and preserves documented identifier exceptions. Include mutation proof.
* Local real-app Chromium asserts changed visible labels, restored history,
  human authority, independent hazard route, unknown/unverified sources,
  proposal-only operation and exact AI label.
* Focused content and coupled chat/regulatory API tests, JS syntax, required
  existing API lint/format/type checks and diff check pass or explicitly report
  actual failures. No unavailable check is reported passed.
* Public docs remain byte-identical to the original reviewed candidate unless
  a separate source-correction receipt is required.
* PR reports exact base/candidate/head, ordered artifacts, results and unmet gates.

## Test Ownership and Locked Candidate

* Canonical unit owner: src/api/tests/test_content_standard.py. Removals: none.
  Maximum additions: four test methods (regex families, identifier exceptions,
  chat safety/copy contract, mutation proof); retain all existing tests.
* Canonical browser owner: src/api/checks/regulatory_ux_check.py. Add assertions
  in the existing flow, not a parallel test framework. Require a harness-local
  synthetic source quote containing all six prohibited term families; assert
  its exact blockquote text before and after restored history. The existing
  fixture supports source(text=...). Do not edit the shared fixture.
  The identifier-exception unit method must reject an adjacent bad visible
  label on the same line as an allowed identifier.
* No generated source targets. Generated browser JSON is task evidence, not
  application data. Record results under changes/2026-10-18/.
* Static guard tests are regression, not universal semantic coverage. Browser
  assertions supply actual visible-copy and source-preservation evidence.
* Validation: installed .venv; API/core/agents test paths as component guides.
  Focused unittest selection; node --check for app.js/chat.js; API ruff
  check/format/mypy; existing regulatory Chromium harness, optional pinned axe.
* Actual SQL Server parity not applicable: no backend, query, schema, payload,
  persistence or adapter change. Browser exercises synthetic SQLite, not claimed
  MSSQL parity. Docker image contract applies to API asset packaging if local
  daemon available; attempt build/non-root startup, otherwise report unavailable.
* Use `.local/issue-153-chat-copy/` scratch, set TMPDIR/TMP/TEMP to its resolved
  absolute tmp directory for fresh validation processes and verify
  tempfile.gettempdir(). Keep axe/cache/output task-local; remove scratch before
  staging. Run the workflow's isolated E,F,I,B,UP ruff and isolated format
  commands for checks/regulatory_ux_check.py as well as ordinary API checks.
* Implementation-caused scoped failures or unresolved actionable scoped Review
  findings block validated publication. Correct within two separate receipts
  or return unresolved evidence to coordinator; do not claim a pass. Only an
  explicitly blocked/draft evidence handoff may publish unresolved work.
  Demonstrated inherited failures, optional axe/Docker unavailability and named
  human/whole-issue gates remain explicit limits rather than slice acceptance.
  Significant semantic/authority choices stop immediately.

## Sources

Research .copilot-tracking/research/2026-10-18/issue-153-chat-copy-research.md
(C1-C6/W1); src/api/README.md and src/README.md; actual src-ci workflow.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Copy and regression evidence

Dependencies: completed Research and independent critique dispositions.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend copy guard and change application-owned labels

Chat/app literals, existing test and browser harness only; details P01-T01.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Update existing audit record and KB routing/history

Precise scope, limitations and glossary additions; details P01-T02.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and freeze candidate

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run local checks and freeze reviewed file hashes

Record commands/results/mutation/browser evidence before original Review.

<!-- rpi:phase id=P03 -->
### [x] P03: Independent Review and publication

Depends on P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run one original independent Review

Refresh web guidelines before changed-file review. Preserve record unchanged.
Apply scoped findings only with separate correction receipts (maximum two).

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Reconcile artifacts and publish for coordinator

Resolve GitHub identity, commit/push/create PR without closing words or merge.
Report base movement rather than integrate without authorization.

## Dependencies

#150 CLOSED verified. #149 grouping only. Exact base and clean supplied branch
verified before writes. Resident human acceptance is not a prerequisite for
this synthetic-only partial engineering delivery, but remains unmet for use.

## Critique Disposition

One original independent critique executed: Revise, three Medium findings.
Original record is frozen and will not be rerun or rewritten.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied directly | Test Ownership and Locked Candidate publication gate; P03 details prohibit validated publication with scoped failures |
| PC-002 | Applied directly | Mandatory six-term exact source canary before/after restore; mixed identifier/visible-label negative unit case |
| PC-003 | Applied directly | Workspace-local scratch/temp controls and isolated harness lint/format added; adopted as additional containment without relying on the critique's unsupported assertion that the caller forbade /tmp |

## Follow-Up Items

* Universal core-flow/error coverage and actual comprehension remain outside
  scope; owner/coordinator to select later work.
* Named human must review exact resident wording before any use.
* RV-001 (Low, inherited): form metadata and label association; coordinator to
  scope a separate forms task.
* RV-002 (Low, inherited): unsent chat drafts lack navigation warning integration;
  coordinator to scope retained-draft/navigation work.
* RV-003 (Low, inherited): ordinary list filters/search/sort are not URL-restorable;
  coordinator to assess separately from this text-only slice.
* RV-004 (Low, inherited): long lists lack virtualization; measure impact before
  selecting a performance change.
* RV-005 (Low, residual evidence): eight textarea contrast incompletes need a
  separate rendered-background/contrast assessment, not a presumed failure/pass.

## Handoff

Implementation evidence: .copilot-tracking/changes/2026-10-18/issue-153-chat-copy-changes.md.
P01/P02 and P03-T01 complete. One original independent Review executed Complete,
outcome Conformant for the exact bounded candidate; no introduced scoped defects.
Five inherited/residual Low follow-ups are routed, not corrected in this slice.
P03-T02 published as PR #402 to main. Initial delivery commit:
ea3208fb6068a2293210f830c71c5eed50fe8be5. A final tracking-only reconciliation
commit records publication and stopped session; exact final head is GitHub PR
headRefOid and the coordinator handoff, avoiding a self-referential commit hash.
No source correction or second Review. All plan markers complete.
Owner-directed stop after publication; coordinator exact-head review and explicit
moved-main integration authorization remain next.
Adverse original critique remains Revise, not relabelled Pass.
