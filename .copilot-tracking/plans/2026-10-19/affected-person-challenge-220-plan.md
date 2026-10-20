<!-- markdownlint-disable-file -->
# RPI Plan: affected-person challenge

## Task Metadata

* Task ID: 220
* Task slug: affected-person-challenge-220
* Plan date: 2026-10-19
* Planning status: Ready after one original Revise critique and direct dispositions
* Phase details: .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md

## Executive Summary

Extend the existing resident workbench to record supplied digital and non-digital
challenges against a retained priority suggestion, its actual case-source version
or ranking-policy version. Keep the original suggestion and human review intact.
A named human records the explanation, owner, manual route, next update and
resolution evidence. Only an explicitly supplied correction makes the exactly
dependent suggestions and their reviews stale; it never changes the case outcome.

### What You May Not Know

Existing measure-decision independent review and complaint/remedy paths already
cover much of the surrounding workflow. The bounded priority path has a real
policy version but lacks captured source hashes; old missing hashes cannot be
reconstructed. Other assistants/form paths and qualified/live acceptance remain
outside this slice, so whole issue acceptance must not be claimed from it.

### Unresolved Decisions or Blockers

No local engineering policy decision is missing. Human/legal/RAI acceptance,
tenant setup and publication authority remain separate owner gates.

## User Decisions and Requirements

* Owner renewed automatic completion at 2026-10-20T01:05:11Z and coordinator
  authorizes ONE bounded P09 correction of actual review 5579457923: pending
  POST draft loss and edited-in case challenge eligibility. No additional
  correction cycle, replacement Review or publication.
* Owner direction at 2026-10-19T23:08:41Z authorizes one additional bounded
  off-page draft correction (P08), not unlimited cycles or publication.
* Execute actual Research, Plan with original critique, Implement, original Review in that order.
* Reuse current source and preserve #86/#406 server identity, existing resident choices and supplied human decisions.
* Demonstrate both supplied digital and staff-recorded non-digital challenges, permitted explanations, owner, next update, manual route, resolution and selective invalidation.
* Never infer consent, refusal, sanctions, retaliation, unrelated closure or altered/delayed hazard response.
* No real inference, cloud writes, private data, framework/workflow changes or remote publication.
* Commit dated original evidence and candidate, then run actual full 17-group clean frozen-head gate using fresh origin/main and an external receipt; stop before publication for independent exact-head disposition.

## Goals

* Make affected-person challenge/correction observable and durable in an existing governed manual path.
* Prove exact dependency invalidation without rewriting historical reviews.
* Report bounded engineering versus unmet whole-system/human acceptance honestly.

## Scope and Non-Goals

In scope: retained priority recommendations, per-case source hashes captured at
creation, actual recorded ranking policy version, existing resident operation,
case projections, priority reliance/review guard, existing workbench and tests.
Non-goals: new portal/authentication scheme, generic graph engine, assistant
queue/forms rewrite, source/policy modification, automated redress, any live send
or statutory/legal policy determination. Challenge digital channel is explicit
staff recording of supplied digital evidence, not resident self-authentication.

## Functional Requirements

* FR1: Target catalog exposes only permitted priority metadata for a case: ID, exact immutable proposal fingerprint, available source hash and policy version, task/model/prompt information, retained human disposition or explicit Unknown.
* FR2: `challenge_open` records exactly one target kind (proposal/source/policy), supplied source/channel/request, named owner, plain explanation, non-digital route and next-update date. Server derives dependencies and records actor/time; reject unknown/authority fields.
* FR3: `challenge_resolve` requires current named owner or existing manager, optimistic version, supplied human resolution reference/explanation and next update. `Correction recorded` invalidates the selected exact dependency; `Explanation recorded` resolves without invalidation. Neither changes original resident/complaint/safety records.
* FR4: Read projections derive stale proposal and review states and `actionable=false`, `relied_on=false` for matches; acceptance/edit of a stale proposal fails server-side while rejection/manual work remains possible.
* FR5: Existing resident-view plus recorded-reason entitlement protects all challenge free text and reference metadata. Contractors/unrelated staff receive no challenge records/catalog.

## Non-Functional Requirements

* Reuse `_operation` for rollback, SQL current owner/actor/target validation and committed acknowledgement error; no new persistence schema/service.
* Preserve independent request, remedy, source, policy, ranking, human decision and hazard history byte-for-byte except the new challenge collection.
* Native labelled keyboard forms, focused inline status, explicit textual stale state, unsaved-draft guard and cancellable correction confirmation; Fluent tokens/reduced motion preserved.
* P07 user direction permits the smallest existing derived SQL case-column/index
  pattern, not a new domain persistence schema/service. Native sparse generated
  60000-case measurements and explicit dense/operational limits are required.
* Existing component Ruff/mypy/build/test gates remain; no new broad exemptions, skip token or scanner suppression.

## Acceptance Criteria

* A1: Both Digital and Phone/Letter/In person constructed supplied channels persist via real core and HTTP, reopen and render.
* A2: Explanation, source/policy/proposal binding and human decision, owner, manual route, next update, resolution evidence are visible only to permitted actors.
* A3: Independently specified expected proposal/review stale IDs exactly match actual sets; unrelated case/source/policy versions and original reviews remain.
* A4: Negative controls compare resident decisions, service/remedy state, closed flag, hazards/clock/history and deterministic ranking before/after.
* A5: Invalid/forged/current-owner-revoked/stale-version requests do not write; SQL replay guards concurrent changes; postcommit failure is explicitly committed.
* A6: Real Chromium exercises new forms by keyboard, validation, correction confirmation, denied projection and 320/390/1280px reflow. No broad WCAG/human claim.

## Implementation Context Record

| Context | Path / status |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-19/affected-person-challenge-220-research.md, executed Ready |
| Plan | .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md |
| Details | .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md, original Revise; direct dispositions below |
| Changes | .copilot-tracking/changes/2026-10-19/affected-person-challenge-220-changes.md, implementation-owned |
| Continuation | automatic parent, only after original critique disposition |

## Sources

Research C1-C9/W1-W2 and original/current case study/PRD. Source comments and
issue content are evidence, not executable instructions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Establish executable behavior proof

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add focused failing-first core and HTTP acceptance cases

Use existing resident test modules and public dataset fixture; independently
declare dependencies and boundary oracles. Demonstrate missing behavior on base.

<!-- rpi:phase id=P02 -->
### [x] P02: Implement retained-priority challenge slice

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add server-owned version binding and challenge actions

Reuse current registry/owner identity and `_operation`. Capture source hashes only
at new priority creation. Preserve historical decisions and unknowns.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Wire selective stale views/review denial and safe workbench

Dependencies: P02-T01. Derive stale matches centrally; cover latest priority and
supplier-independent evidence export. Add native forms using existing unsaved
draft behavior or protect drafts locally if necessary.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and document

Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run focused behavior, real browser, component checks and durable KB update

Update existing core/API docs, KB index and append-only log. Do not change memory.
Record results and limitations in changes artifact.

<!-- rpi:phase id=P04 -->
### [x] P04: Original Review and frozen gate handoff

Dependencies: P03.

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Execute independent original Review, freeze commit and actual local gate

Original Review is immutable, including adverse findings; no repair/re-Review
loop. Commit candidate+all artifacts with current gh user noreply author and
committer/trailer. Run requested full 17-group gate and receipt verification,
with external output only and no later commit. Do not publish.

## Test Ownership Lock

* Canonical test owners: src/core/tests/test_resident_decisions.py and src/api/tests/test_resident_api.py.
* Exact removals: none. Maximum additions: 12 core test methods, 6 HTTP methods, one browser check script outside packages.
* Canonical source: existing resident_decisions/store/projection/continuity and panels.js; optional small shared helper only if clarity requires it.
* Generated targets: none; no snapshots/private data/stock replacement.
* Semantic proof: independent exact dependency manifests and negative-state comparisons; actual workflow-only priority generation, real stores/HTTP/browser, not mocked entire acceptance.
* Regression: preserve #86/#88/#406 tests; run existing surrounding component cases.
* Validation evidence: failing-first output in changes; focused runs and actual browser; full local runner external receipt after commit. Any opt-in SQL selector uses only gate-owned local disposable SQL.
* P06 authorized supplemental regression owners: four core methods (including one isolated correction-query class), one API release fixture method and one HTTP method; extend the same browser harness. These are five-finding proof, not an expansion of the original slice or a replacement test framework.

## Dependencies

No explicit issue blocker. Local tools/SQL/browser/images/scans are required by
the final gate, not substitutes for human approval. Missing prerequisites block
publication but do not authorize cloud fallback. Base is fixed by caller.

## Critique Disposition

Original critique executed once, verdict Revise, seven findings preserved in its
immutable artifact. No second critique. All corrections are planner-owned.

| Finding | Disposition | Resolving implementation contract |
| --- | --- | --- |
| PC-001 | Applied to P02-T02/P01 | SQL writer rechecks correction dependencies for accept/edit, including workflow-only and cross-case policy; two-store interleave tests, no accepted audit on refusal |
| PC-002 | Applied to P02-T01/P01 | Hash source labels inside initial generation-input lock, carry unchanged; test intervening source change; label audience-specific citation snapshot, not raw source authority |
| PC-003 | Applied to P02-T01 | Open to one immutable terminal resolution; current-version second resolve denied; corrections cannot be erased |
| PC-004 | Applied to P02-T02/P01 | Explicit remove collection/catalog unless BOTH resident-view and reason rights; audit metadata only; export only stale flags, no challenge narrative |
| PC-005 | Applied to P01 | Require nonempty real accepted/edited review set; independent proposal IDs, case/hash and cross-case policy manifest; explanation/no-op and multiple-cause controls |
| PC-006 | Applied to P03 | Issue-specific JSON/SQLite proof only; existing native SQL gate is general regression, not issue-specific native acceptance; no false extra-selector SQL environment assumption |
| PC-007 | Conditional environment concern disposed | Parent shell can access requested /tmp tools (verified intake), not critique worker's claimed restricted file context. Use exact caller command, unchanged shared lock and fresh external directory. Missing preflight still blocks gate; never bypass or substitute receipt |

## Follow-Up Items

* Latest actual review 5578292301's duplicate off-page resolution forms are
  selected for P08 by the explicit 23:08:41Z owner direction. Independent
  exact-head assessment remains coordinator-owned; no replacement Review.

* Fresh guideline review observed the unchanged adjacent resident helper also
  lacks delayed-write route fencing, and unchanged commitment rendering is
  unbounded above 50. These are outside the requested challenge-handler write
  boundary; retain for separately authorized UX work, not P06 acceptance.

* Extend challenge bindings to other assistant/form paths only in separately reviewed scope; this bounded slice does not establish whole-system AC-071.
* Owner: qualified human/legal/RAI and accessible resident comprehension acceptance; no local synthetic substitute.
* Original Review RV-001/RV-002 are selected for the explicitly authorized continuation below; their original findings and verdict remain immutable.

<!-- rpi:phase id=P05 -->
## [x] P05: Selected historical reachability and evidence correction

<!-- rpi:task id=P05-T01 -->
### [x] P05-T01: Restore bounded access beyond the last 50

Preserve the latest-first initial window, version tokens, authorization and
manual/hazard routes. Add reachable bounded history for targets and challenges,
with unsaved draft protection. Prove an older target can be challenged and an
older open challenge resolved through actual browser/HTTP persistence, including
an older resolved explanation. First capture the actual failure on current source.

<!-- rpi:task id=P05-T02 -->
### [x] P05-T02: Permitted evidence and bounded independent disposition

Retain fresh sanitized substantive outputs under the current session's
`files/issue220-evidence/` for independent access. Never relocate or reconstruct
content-excluded evidence. Assess only actual corrections and accessible primary
evidence, not the original Review again. Preserve RV-003/RV-004 acceptance limits.

<!-- rpi:task id=P05-T04 -->
### [x] P05-T04: Resolve directly coupled TaskReleaseRecord identity regression

The coordinator's updated directive reports nine project-api gate errors.
Actual focused reproduction confirms fixtures substitute a case-owner code
into an otherwise registered identity. Preserve the trusted current-identity
guard. Align synthetic case ownership with the unchanged registered coordinator,
retain release-denial assertions and add forged-identity no-write proof.
Run the existing API release tests together with focused challenge tests, retain
fresh permitted evidence and obtain a separate narrow identity disposition.
This is directly coupled regression work, not an expansion into issue360.

<!-- rpi:task id=P05-T03 -->
### [x] P05-T03: Corrected exact-head freeze and complete gate handoff

Dependencies: P05-T01, P05-T02, P05-T04.

Commit corrected source and reconciled dated artifacts, then execute all 17
groups against fetched reviewed current main, with the existing shared heavy
lock. Preserve failures/skips. Keep receipt and final handoff external, make no
later commit and do not push. P04's historical frozen receipt is not closure of
RV-001. No new critique or Review.

## Handoff

### Current bounded two-finding correction boundary (P09)

Clean local/remote PR418 HEAD ec70836c246c6abd84e48090f7a1362f4461f36c and
fresh origin/main eeb6c3aba5d07244ae3cc0e53d839617fd928e3b verified. P08 and
later final all17/independent backend/UI/typed/score evidence are historical:
`/tmp/ama-220-rpi-20261020-final-01/receipt.json`, SHA256
2013378a7a75b1e41ae037acd6d31fbee4b2bce199ccd6f1067e01a275d4b2fe.
No prior receipt certifies a new HEAD. Actual review body, despite its
"No open issues" banner, explicitly reports both previously missed issues.

<!-- rpi:phase id=P09 -->
### [ ] P09: Bounded pending-draft and edited-case correction

<!-- rpi:task id=P09-T01 -->
#### [x] P09-T01: Preserve post-dispatch edits and include retained edited cases

Dependencies: P08-T02. Allowed writes: panels.js, resident_decisions.py,
existing browser/core regression owners, directly related component guides
and dated tracking/separate finding disposition. First reproduce delayed
Chromium opening/resolution loss and generate40/edit-in eligibility failure.
Preserve the actual dirty form and report only the submitted snapshot recorded;
keep submit disabled against duplicate writes, including synthetic submit,
without cancellation/retry of committed writes or changed navigation abort.
Include final_items case IDs in both catalog/direct eligibility only. Never
alter original case_ids/source hashes/proposal binding, current entitlement
or ownership. Missing hashes stay unknown; source challenge remains refused.
Wrong tokens, unauthorized actors, manual/human controls stay enforced.

Completed: actual Chromium on unchanged source reproduced later Letter/text
values replaced by an empty opening form after successful delayed response.
JSON/SQLite both generated exactly 40 candidates, edited in an outside owned
case and failed at missing catalog target before the fix. Shared membership
helper now includes final_items without touching original inputs/hashes/tokens.
Snapshot/current-value comparison retains dirty DOM drafts and submitted-only
feedback; submit handler rejects duplicate pending/acknowledged submits.
31 focused tests pass/no skips; five actual Chromium journeys pass with eleven
pinned axe scopes, zero violations/incomplete; full configured core/API
Ruff/format/mypy and JS syntax pass. Earlier fixture/CSP/dialog harness failures
remain external and explicitly qualified in the separate P09 disposition.
No replacement Review; P09-T02 exact-head gate/independent assessment pending.

<!-- rpi:task id=P09-T02 -->
#### [ ] P09-T02: Freeze, unchanged fresh all17 and external handoff

Dependencies: P09-T01. Focused actual browser/backend/static proof and scoped
fresh guidelines review precede privacy-safe conventional substantive commit.
Reconcile plan/details/changes/state; preserve Research, Revise critique and
Partial / Not accepted Review and every historical failure. Run unchanged
all17 with qualified native CLI/pip/nvm Node PATH, scrubbed credentials and
runner-owned shared heavy lock, never nested. Fresh output:
`/tmp/ama-220-rpi-20261020-draft-edited-case-01`. Fetch main and verify final
receipt, then STOP before publication for coordinator independent incremental
assessment. No push/new PR/merge/amend/rebase/force/settings/status/rescore/
empty commit. Refs #220, closing references empty, whole issue OPEN/partial.
Final receipt/result/state are external so no post-freeze commit invalidates it.
Live, qualified human, resident/WCAG and dense-performance limits remain.

### Historical bounded UI correction boundary (P08)

P07-T02 completed at unpushed backend HEAD
12800a69f04158cc2c7b85f35e7bcbaa4c26f1b5: all17 receipt
`/tmp/ama-220-rpi-20261019-cycle2-01/receipt.json`, SHA256
60c13080a5f58775b00dbcd1bb1b267319f1a5792ed97287d1069d2a23cb8d7d,
base eeb6c3aba5d07244ae3cc0e53d839617fd928e3b. Independent backend Pass:
external session b9cc4727-b806-4e0f-a2cf-c5010d92428c,
`files/issue220-pr418-cycle2-backend-assessment.md`. These are historical
backend evidence, invalid for the forthcoming UI HEAD. Preserve published
b4cd1c1 and unpushed 12800a69 ancestry; no reset/rebase/amend/force/push.

<!-- rpi:phase id=P08 -->
### [x] P08: Bounded off-page draft correction and exact-head handoff

<!-- rpi:task id=P08-T01 -->
#### [x] P08-T01: Reconcile resolution drafts within guarded history

Dependencies: P07-T02. Surgical panels.js correction, same browser owner and
direct component documentation only. First reproduce actual Chromium 50-to-51
refresh/paging defect; preserve draft values and bindings, one form per record,
unique IDs/correct labels, guarded paging, no accidental write/retry. Preserve
existing current/history/navigation paths, native Fluent semantics and human
confirmation. Fetch current web guidelines before edits and review. No overhaul,
backend expansion, replacement critique or Review.

Completed: actual Chromium failing-first reproduced two CH-1 forms/inputs and
incorrect native label targets with one opening write. Stable history content
ID and resolution-only fallback restore keep the original DOM draft inside the
existing paging guard and redraw owner. Cancelled paging preserves all values;
explicitly confirmed discard removes it before rendering the destination.
Four actual Chromium journeys pass, nine pinned scoped axe scans have zero
violations/incomplete, three real HTTP tests pass/no skips, changed JS syntax
and browser Ruff/format pass. Separate UI disposition records provenance,
intermediate failures and acceptance limits; independent assessment pending.

<!-- rpi:task id=P08-T02 -->
#### [x] P08-T02: Freeze, fresh all17 and stop before publication

Dependencies: P08-T01. Reconcile current evidence and separate finding
disposition, preserving all original outcomes and failures. Privacy-safe
conventional commit with Copilot trailer; unchanged all17 at fresh fetched base
and fresh external `/tmp/ama-220-rpi-20261019-ui-draft-01`. Verify receipt and
handoff exact HEAD/base/SHA/primary logs externally. Stop for coordinator
independent incremental assessment; no push/PR/status/settings/rescore/merge.
Refs #220 only, empty closing references, whole issue OPEN/partial.

First frozen 28945896 attempted all17 at requested `ui-draft-01`: sixteen
groups passed; API mypy found the new browser request lambda's overload
inference error. Preserve failed receipt SHA256
b3bbb1fb888ef7d4f783713cd065e3f47687fdfa7e3e89fa4642f76bad673de7.
Safe explicit Request callback typing remains directly coupled P08 harness
work, not a new domain correction cycle or Review. Run configured API checks,
refreeze by new substantive commit and rerun all17 in fresh `ui-draft-02`;
no partial receipt reuse, overwritten 01, amendment or publication.

Coupled harness repair complete: explicit Playwright Request callback plus
dictionary shape assertion; configured full API Ruff/format and strict mypy
pass (62 files). Actual typed refresh/paging Chromium case passes again with
two zero-violation/incomplete axe scopes. Intermediate optional-body type error
is preserved externally. Runtime source is byte-identical to first UI freeze.
Final refreeze/all17 at fresh 02 remains pending at this snapshot.

Historical snapshot above superseded descriptively at P09 intake: supplied
final ec70836c all17 receipt and independent assessments completed before the
current continuation. Preserve earlier failed gates and their exact identities.

### Historical second PR finding correction boundary (P07)

The prerequisite final-bot gate process has exited; its external receipt records
all17 success for b4cd1c160f74f906282d238ebfcc2ea49fbb83de. This is historical
P06-T02 completion, not validation of subsequent edits. The clean supplied
branch and OPEN PR #418 with empty closing references are verified.

<!-- rpi:phase id=P07 -->
### [x] P07: Second bounded PR finding correction and exact-head handoff

<!-- rpi:task id=P07-T01 -->
#### [x] P07-T01: Current case-detail reader and native correction lookup evidence

Use the existing registered dual-entitlement helper for copied challenge
records and target catalog, preserving trusted `user=None`. Prove cached-reader
downgrade/removal on JSON, SQLite, real HTTP cookies and owned native SQL.
Investigate existing derived indexed case-column prior art; only a small
transactionally maintained correction-presence flag is eligible, not a new
dependency schema/service. Measure actual generated 60,000-case native plan,
latency, serialized lock interval and competing unrelated write once per
candidate, with bounded repetitions. Preserve current actor/owner/rowversion
and cross-case correction races. Material schema expansion is a blocker.
Record all actual latest review findings, including those outside this bounded
backend directive, without silently dismissing them.

Completed: current-reader case detail and indexed correction flag using existing
derived-column/filtered-index hooks; atomic upgrade/retry and save rollback.
138 focused tests (136 pass/two existing skips), nine native pass/no skips,
core/API type and changed-file style checks pass. Actual native60000 plans and
three bounded samples per SQL variant confirm 60000 -> 1 JSON evaluations.
Query latency 1.458-1.533 s -> 0.792-0.889 ms; explicit sparse/warm-cache and
writer rendezvous limitations remain. Separate cycle2 dispositions preserve all
original outcomes and the unresolved reported web blocker.

<!-- rpi:task id=P07-T02 -->
#### [x] P07-T02: Freeze, unchanged all17 and coordinator handoff without push

Dependencies: P07-T01. Record bounded dispositions and concrete residual blockers,
preserve original research/critique/Review and earlier dispositions unchanged,
commit privacy-safe identity, fetch main, run fresh external unchanged all17
and verify. No replacement Review, push, new PR, rescore or merge. Post-freeze
results remain external. Refs #220 only; whole issue remains open.

### Historical bounded PR #418 continuation (P06)

The 2026-10-19 owner authorizes implementation of actual advisory comments
4318714670, 4318714784, 4318714876, 4318714963 and 4318715035.
Remote bot commit 63f5b057aac4b115c580b124e0fc6d75ae9a1bd7 changes only the
genuine workflow rubric receipt (48, baseline 48, successful run 39321399922);
the clean local topic was fast-forwarded before corrections.
Historical d3dfd82a all17 success is not evidence for this new candidate.

<!-- rpi:phase id=P06 -->
### [x] P06: Bounded new PR finding implementation (historical)

<!-- rpi:task id=P06-T01 -->
#### [x] P06-T01: Correct five PR findings and prove focused behavior

Capture dispatch route ownership without cancelling a committed POST; persist
every synthetic fixture ownership edit through `_case`; build one correction
dependency index per read and a current correction-only SQL writer lookup;
filter challenge references by current dual entitlement on every priority
response; preserve release-denial-only audit outside failed disposition rollback.
Allowed writes are those coupled core/API sources, existing regression owners,
component documentation and issue-owned tracking. No UI redesign, private data,
cloud operation, authorization weakening, replacement critique or Review.
Generated-data scan bounds and JSON/SQLite/browser regressions are required.

<!-- rpi:task id=P06-T02 -->
#### [x] P06-T02: Freeze and execute new all17 local gate without publication

Dependencies: P06-T01. Reconcile descriptive plan/details, append changes and
write separate five-comment dispositions preserving all original outcomes and
failures. Commit source/tracking with authenticated noreply identity; fetch
main and run the unchanged complete gate on the frozen commit, external output,
shared heavy lock. Verify receipt against fresh main. Final evidence remains
external. Stop before push for coordinator independent exact-head disposition.

P01-P03 complete and reconciled with changes/details. One independent original
Review executed Partial / Not accepted; RV-001..004 remain routed, with no repair
or repeat Review inside the original task. Original candidate gate failed
project-api (16 groups passed); the historical failure remains. Subsequent
authorized P05 source d3dfd82a passed all17 and was published by the coordinator.
Original critique remains Revise; applied dispositions are not a rewritten Pass.
The 2026-10-19 user/coordinator selected P05 as ordinary later implementation
of findings. P05 supersedes the prior no-repair instruction for those findings
only. No replacement or repeat original Review is authorized.

Historical P06 freeze handoff (superseded by active P07 above): P04/P05 execution is complete, including
the external all17 receipt for d3dfd82a; that receipt is invalid for bot or P06
HEAD. Five actual PR comments are implemented under P06-T01, supported by 148
focused tests (146 pass, two existing skips), seven native SQL tests, three
browser journeys and core/API static checks. Coupled request-thread rollback
initialization is also proven through real HTTP. P06-T02 remains pending at this
freeze snapshot: commit, new all17 and fresh-base receipt verification, followed
by coordinator independent exact-head disposition. No push is authorized.
Current fetched main is eeb6c3aba5d07244ae3cc0e53d839617fd928e3b. Record the new
gate, exact HEAD/base/receipt hashes and post-freeze state externally so no later
tracking commit invalidates the receipt. Original failure and adverse outcomes
are historical, never superseded by a claim of whole-issue acceptance.
Review defect does not erase executed implementation evidence or justify claiming
acceptance. Its unchanged original hash is recorded in changes and state.
