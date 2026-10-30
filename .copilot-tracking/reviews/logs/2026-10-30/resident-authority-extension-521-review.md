---
title: Resident authority extension Review
description: Original independent post-implementation assessment for the October 30 continuation
ms.date: 2026-10-30
---

## Opening Review State

Task 521, resident-authority-extension-521, source-only continuation.
Current research, plan, details, critique and changes are dated 2026-10-30.
Original 2026-10-28 outcomes remain historical and immutable.
Declared boundary: complete authority implementation inherited in 92b66933 on
reviewed main a02984e8, plus current documentation/evidence changes.

P01 execution reconciled. Fresh local domain/helper/API/real-SQL results and
explicit skips/static failures recorded in changes. No runtime source correction
was required. Origin/main moved to 4b37c2c9 during validation; final gate and
exact-head assessment remain separately blocked. Live acceptance is prohibited.

## Execution Status

* Review execution status: Complete.
* Outcome: Residual work.
* Full-plan execution remains Partial: P01 is executed; this record completes
  the comparison assigned to P02-T01, not P02-T02 or live acceptance.
* Exactly one original independent post-implementation Review was executed
  for the October 30 continuation. No nested agent was used.
* Assessed HEAD: 92b669335cb8874df227cd2ecd90b45f1e3b0a8d.
* Pinned reviewed base: a02984e8d71d312f089ad75713d7a98e59aee420.
* Locally recorded origin/main: 4b37c2c9ae5553e55604a10e97e7ab21a2a265fb.
  This newer ref is a publication prerequisite observation, not the source
  comparison base. No fetch or other remote operation was performed.
* The assessed candidate includes the inherited implementation and current
  uncommitted documentation/evidence. It is not a clean, committed final
  exact-head publication candidate. No receipt exists for this boundary.
* Only this Review file was written. No tests, installation, gate, Azure,
  deployment, sign-in, credential access, private-data access, foreign-output
  or container access, push, source correction or historical-artifact edit
  was performed.

## Scope and Evidence

Acceptance basis: the supplied owner direction, current research C1-C7/W1,
the current plan's AC1-AC4, phase/task markers, PC-001 through PC-006
dispositions and the complete source diff against the pinned reviewed base.
The issue was not retrieved remotely during Review; issue criteria are
assessed as represented in the supplied current plan and caller direction.

Compared current task artifacts:

* .copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md
* .copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md
* .copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-30/resident-authority-extension-521-plan-critique.md
* .copilot-tracking/changes/2026-10-30/resident-authority-extension-521-changes.md

Complete twelve-file source/documentation comparison:

* src/core/src/zava_forward/core/resident-demo.json
* src/core/tests/test_resident_showcase.py
* src/core/tests/test_resident_showcase_sql.py
* src/api/tests/test_resident_demo_api.py
* infra/scripts/resident_showcase_sql.py
* infra/sql/resident-showcase.sql
* infra/tests/test_resident_demo_secrets.py
* infra/tests/test_resident_demo_deploy.py
* infra/README.md
* src/api/README.md
* docs/reference/README.md
* docs/reference/log.md

The pinned diff also contains seven inherited October 28 RPI/state artifacts.
These are historical evidence, not fresh execution or newly approved work.
The historical research, plan and original Review were consulted; read-only
git comparison confirms no current changes to that historical artifact set.
Its original critique Revise and Review Complete / Residual work, including
adverse validation/publication evidence, remain unchanged.

Supporting unchanged sources inspected: src/core/src/zava_forward/core/resident_showcase.py,
src/core/tests/test_resident_showcase_sql.py fixture/principal contracts,
src/api/src/zava_forward/api/resident_demo/app.py,
infra/resident-demo.bicep, infra/scripts/resident_demo_secrets.py,
infra/scripts/resident_demo_deploy.py, infra/scripts/credential_arm.py,
infra/sql/resident-assistant.sql, src/README.md and tools/rpi-checks.py.
Required project context was read in docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md,
docs/reference/memory.md and
docs/reference/research/sector/housing-association-primer.md.
Memory is context, not acceptance evidence.

Validation counts, failures, baseline reproduction and cleanup are supplied
implementation evidence from the caller and current changes/details. Raw
external logs and their recorded hashes were not independently reopened or
verified by this reviewer. No independently rerun validation is claimed.
The evidence is sufficient for a credible bounded source Review, not a
receipt, live-operation assessment or verification of every skipped contract.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record/current evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Existing distributions restored after missing imports/tools; focused domain/helper/API checks, separate real SQL and static checks recorded | Reconciled as execution | Explicit skips, initial harness failures and baseline infra failures remain visible |
| P01-T02 | Existing source retained; current infra guide, knowledge index/log and dated evidence reconciled | Reconciled | No demonstrated coupled defect required a new runtime or test change |
| P02-T01 | Independent technical/source Review assigned, marker unchecked at intake | Completed by this record | Parent owns marker/handoff updates; reviewer does not edit them |
| P02-T02 | Evidence commit, complete gate, receipt verification and final exact-head assessment pending | Reconciled as incomplete | Dirty/untracked candidate and newer main prevent present full-gate acceptance; RV-001 |
| Follow-Up Items | Owner live/funding review, gated publication/current-base reconciliation and pre-existing infra static debt | Reconciled as distinct work | RV-001, RV-002 and RV-003; no expansion of active source scope |

Research's execution-pending statements and phase details' Initial Readiness
describe their earlier planning point. The plan Executive Summary, details'
Current Execution Reconciliation and changes' final-results/pre-Review
sections agree on the later state: P01 executed, Review pending at intake,
full gate blocked and live acceptance unmet. Historical/intermediate failures
are not silently replaced by the final API success.

## Completed Work Assessment

### Shared boundary and regression coverage

src/core/src/zava_forward/core/resident-demo.json:2 changes only the maximum
to 2027-02-01T00:00:00Z. The unchanged runtime loads that packaged policy at
src/core/src/zava_forward/core/resident_showcase.py:34-38; Bicep loads the
same JSON at infra/resident-demo.bicep:29; the secret helper aliases
AUTHORITY_END at infra/scripts/resident_demo_secrets.py:51 and the deployment
helper uses its expiry parser. The SQL renderer now imports AUTHORITY_END
and substitutes it at infra/scripts/resident_showcase_sql.py:24-35.
There is no new independently maintained executable January authority.

The distinction between allowed configuration equality and exclusive serving
is technically consistent:

* config_from_env refuses startup at/after configured expiry and values
  above AUTHORITY_END; an earlier configured expiry is not raised.
* exclusion at src/core/src/zava_forward/core/resident_showcase.py:247-258
  preserves provenance, revocation, per-row windows, canonical synthetic
  email and duplicate checks, including now >= AUTHORITY_END denial.
* SessionCodec retains min(configured expiry, AUTHORITY_END), 1800-second
  sessions, process-bound signatures, revocation and exact-end refusal.
* The HTTP app caps its expiry to AUTHORITY_END and checks expiry before
  serving. The added real-loopback HTTP test constructs January-valid
  configuration and proves login/view before the cap, token rejection at
  the cap and HTTP 503 for existing-session access and fresh login then.
* The core admission test includes January 31 at 23:59:59.999999, former
  November/December cutoffs, exact February 1 and one second later.
  Config/helper tests accept cap equality and reject fractional/whole-second
  excess. These are configuration acceptance tests, not permission to serve
  at the cap.

The inherited additions are five test methods: core admission, SQL rendering,
SQL legacy/reapply, SQL rollback and HTTP boundary. Existing methods were
extended without removing refusal assertions. No additional method was added
in this continuation, within its two-method maximum. The core/helper/API
passing results are recorded execution evidence; ordinary SQL skips are not
counted as actual SQL proof.

### Checked SQL renewal and rights

infra/sql/resident-showcase.sql:24-45 keeps XACT_ABORT, BEGIN TRANSACTION,
the named check drop, WITH CHECK replacement, COMMIT and rollback/rethrow
inside one GO-delimited batch. Both table creation and replacement use the
rendered cap and preserve valid_to > valid_from. The renderer sends the
whole replacement batch to the existing autocommit connection; no split
commits the drop alone. WITH CHECK requires all existing rows to satisfy
the replacement, including revoked rows.

This is atomic constraint replacement, not an atomic transaction covering
all later view/grant batches. The migration does not update row windows,
insert residents, clear revocations, replace identity or broaden rights.
Existing DENYs and the single view SELECT remain unchanged. The existing
apply path still verifies external identity SID, no role membership or
ownership, narrow direct permissions and public-role grants.

src/core/tests/test_resident_showcase_sql.py:604-679 implements the required
legacy November constraint, two full reapplies, exact row/revocation
preservation, enabled/trusted check, view read/base denial and verify_rights
checks. Its failed-replacement fixture preserves the old check/state/rows,
tests @@TRANCOUNT = 0 on the failing connection and restores fixture state.
The supplied separate real-SQL result is 27 tests with zero skips, covering
these contracts. It is materially stronger than renderer inspection or
ordinary discovery's 27 opt-in skips.

Actual external managed-identity authentication is not proven by a disposable
SQL Server principal created WITHOUT LOGIN. SID validation is inspected and
covered by existing fake principal tests; actual live SID/rights verification
remains an owner-operation prerequisite. No false Azure-authentication
acceptance is inferred from local SQL.

### Independently assessed credential and SQL renewal plan

infra/README.md:3677-3721 is technically coherent as a conditional operations
plan, not an executable approval or evidence of completed rotation:

1. Metadata-only preflight identifies the exact app/vault/SQL scope, SID,
   rights, image, expiry and individually approved synthetic rows, using
   existing private paths. Unknown identity or permissions stops the operation.
2. Owner-held password/verifier and fresh signing key are distinct from SQL
   managed identity, which has no application password to rotate. Hidden
   handling and no secret-bearing arguments/logs are explicit. Expiries are
   capped; seven-day alert and at-least-30-day rotation requirements are
   proposed controls, not evidence that alerts or rotation already operate.
3. The plan correctly rejects using the existing helper to rotate existing
   names. infra/scripts/credential_arm.py:174-192 requires the exact distinct
   selected-vault secret set and actionable Create only.
   infra/tests/test_resident_demo_secrets.py:320-347 retains Modify refusal
   and no-write assertions. The deployment helper's separate Modify support
   does not authorize credential writes or relax this check.
4. Bounded prior-version overlap, versionless-reference/revision refresh,
   restart/session invalidation, owner sign-in, cross-case denial, logout and
   1800-second expiry verification precede disabling superseded versions.
   Bicep uses versionless vault URLs, consistent with the proposed refresh
   path. The stated up-to-30-minute refresh allowance is not a proven live
   completion time. Actual revision propagation must be verified before
   declaring rotation complete.
5. SQL constraint renewal and row renewal remain separate. Only individually
   approved existing rows may receive windows within the cap, preserving
   provenance/revocation; existing rows are not renewed by script reapply.
   No user/role creation, wider SELECT, identity replacement or works-consent
   inference is included.
6. Failure requires separately approved ingress shutdown and stop, without
   silently restoring compromised credentials. End-of-window denial,
   secret/row expiry and no resident-serving revision must be checked
   operationally; the local source change cannot establish them.

The source plan passes this independent technical assessment within its
declared conditional scope. An existing-secret exact-version write procedure,
actual version identities, rollback interval, image/configuration, approved
row set and verification evidence are deliberately deferred to a separately
reviewed exact operation and explicit owner approval. That deferral is
appropriate, not a request to weaken the helper or implement rotation now.
Independent technical Review does not satisfy owner operational review.

### Cost arithmetic and preserved approval/rights guards

infra/README.md:3723-3760 labels its historical-envelope proxy rather than
claiming a current tariff: USD30 / two assumed 30-day months = USD0.50/day.
November 30 + December 31 + January 31 = 92 days; 92 * USD0.50 = USD46.
January alone is 31 * USD0.50 = USD15.50. Adding the USD10 reserve gives
USD56 or USD25.50 respectively. These alternatives overlap and are correctly
not summed. USD700 - USD25.50 = USD674.50.

The arithmetic is correct under the declared assumptions. The historical
USD30 allocation is inside USD700, not extra headroom; earlier December
funding is not January funding. Source-only USD0 is expressly not zero
ongoing SQL/registry/private-endpoint/log/storage cost. Accrued, delayed/
unbilled, outside-group, committed and remaining-resource costs plus the
increment/reserve must be non-overlapping and <= USD700. Build, egress,
logging or workload increases require explicit re-estimation. No current
billing, quoted price, January funding or spendability is established.

The complete source diff adds no Bicep resource, RBAC assignment, network
path, replica or broader data scope. infra/resident-demo.bicep:108-140 retains
Single revision mode, the existing scoped versionless references, MSI SQL,
0.25 vCPU/0.5 GiB and min0/max1. Runtime own-case checks, synthetic admission,
1000-row fail-closed cap, row approval/provenance/revocation and shorter
expiries remain. Exact live image/configuration, SQL/credential operations,
cost and rollback approval are explicit at infra/README.md:3762-3773.
The separate paid-inference admission still refuses at November 1 in
infra/sql/resident-assistant.sql:37; no model tariff or paid authority is
extended.

## Issue Acceptance Criteria

Statuses below distinguish the current plan's source/local criteria from
whole-issue operational acceptance. They do not imply issue closure.

| Criterion | Status | Evidence and limit |
| --- | --- | --- |
| AC1: Consistent exclusive January boundary and migration/rights regressions | Proven for the supplied local source/test boundary | Shared policy and all changed consumers/tests inspected; recorded domain, HTTP/helper and 27 zero-skip actual SQL tests cover former/new boundaries, trusted reapply, rollback and rights. Compiled deployment/image/full-gate and live behavior are not proven by this result. |
| AC2: Added cost inside unchanged USD700 envelope | Partial overall; estimate/documentation proven | USD46/USD56 or overlapping January USD15.50/USD25.50 arithmetic and non-overlapping all-in check are correct. Actual liabilities, headroom and January funding are unknown, not a proven within-budget live outcome; RV-002. |
| AC3: Credential/SQL rotation plan and review | Partial overall; independent technical portion completed here | Technical plan is coherent and preserves Create-only refusal, rights, row approval and session invalidation. Separate exact-version procedure review and owner operational approval/execution remain pending; RV-002. |
| AC4: Separately confirmed live apply, verification and record | Unproven | No exact live confirmation/apply/sign-in/verification result is supplied or authorized in this run. Preserving that approval boundary is proven source behavior, not completion of live acceptance; RV-002. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and trigger | Reconciliation and readiness assessment |
| --- | --- | --- |
| P01-T01 / PC-002 | Default full runner does not select core SqlBoundaryTests | Separate owned loopback SQL lifecycle and exact selector added; recorded 27/0-skips result addresses the actual execution gap without claiming default-runner coverage |
| P01-T01 / PC-003 | Inherited opt-ins/config could cross the data boundary | Explicit env -i allowlist, isolated HOME/data/config/cache and separate SQL opt-in documented; current changes describe applying it, not inheriting production settings |
| P01-T01 / PC-005 | Default static groups omit the changed infra files | Exact changed-infra selectors/options added; final results report failure and same-base reproduction instead of suppression |
| P02-T02 / PC-006 | Original Review cannot assess a future commit/receipt; main may move | Commit/gate/refetch/current-base verification/distinct external exact-head assessment specified; actual newer-main drift now leaves it blocked |
| P01-T01 / harness correction | Missing Node caused 76 initial API errors; next retry used wrong CWD | Both attempts preserved; final correct src/api discovery passed, without source changes or invented success for earlier attempts |
| P01-T02 / final handoff | No demonstrated source defect; local checks completed with residuals | Only fresh evidence/docs reconciled; pending gate/live criteria and baseline infra failures remain explicit |

These are compatible validation/handoff refinements preserving the accepted
source direction. No significant divergent source decision or unaccepted
authority expansion was found. Newer-main reconciliation is deliberately not
silently performed; the pinned Review comparison is still well-defined.

## Critique and Material Revision Assessment

The one October 30 critique remains Complete / Revise, with its original
three High and three Medium findings intact.

* PC-001: the plan explicitly rejects the critic's worker-local storage
  constraint as inapplicable to its parent executor. This Review neither
  grants execution permission nor changes the current assessor's own
  restrictions. No setup/gate/storage operation is repeated here.
* PC-002: applied; actual core SQL is separately selected with fixture
  ownership/isolation/cleanup described and 27 zero-skip tests recorded.
* PC-003: applied in the explicit isolation contract and execution record.
  This is inspected recorded evidence, not an audit of every external
  process/environment or independently read raw log.
* PC-004: partially applied: holder inspection and no nested lock/foreign
  access retained; the caller-specific 600-second wait is the recorded
  rationale for rejecting nonqueued advice. The initial timeout is retained
  as failed admission, not successful setup. Review does not retry the lock.
* PC-005: applied as coverage, not as passing results. The same targeted
  failures are recorded on a02984e8; unrelated cleanup remains outside scope.
* PC-006: applied as a conditional sequence and drift stop rule, not completed.
  The current newer-main blocker is correctly retained under RV-001.

No evidence of early live resumption or concealed gate completion was found.
There is no basis to demand a second original critique or Review.

## Plan Follow-Up Assessment

| Existing follow-up | Why outside immediate source work | Owner and next action | Assessment |
| --- | --- | --- | --- |
| Exact live renewal/funding/operational review | Requires separate exact approval and information prohibited in this run | Exercise owner and separately approved operator define/fund/review the operation before apply | Open; RV-002, non-blocking for source authorship but blocks live acceptance |
| Gated publication/human/hosted approvals | Original source Review is not final-candidate or hosted approval | Coordinator preserves hold until required prerequisites and independent exact-head assessment exist | Open; RV-001 |
| Newer-main reconciliation/current-base gate | Candidate was assessed on a02984e8, not 4b37c2c9 | Coordinator obtains permitted reconciliation and a clean committed candidate before a current-base gate | Open; RV-001; not a new active source revision authorized by Review |
| Pre-existing infra static debt | Same findings recorded on reviewed base; unrelated to the authority change | Infra maintainer tracks separate lint/format/driver typing remediation | Open; RV-003, not a defect introduced by this change |

Current changes mirror owner/live/publication items and describe baseline
infra findings in Validation Record/Blockers. The plan/details also identify
newer-main reconciliation. No unresolved follow-up is silently marked
complete, converted into a source defect or added to active implementation.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Complete current-base gate and final-candidate assessment remain unavailable

* Related scope: P02-T02; PC-006; coordinator publication/current-base follow-ups.
* Evidence: current plan P02-T02 and Dependencies; details' Current Execution
  Reconciliation; changes' Blockers. Local read-only git inspection confirms
  HEAD 92b669335cb8874df227cd2ecd90b45f1e3b0a8d, reviewed base a02984e8d71d312f089ad75713d7a98e59aee420
  and cached origin/main 4b37c2c9ae5553e55604a10e97e7ab21a2a265fb.
  The candidate has tracked documentation changes and untracked dated
  evidence. tools/rpi-checks.py:159-174 rejects dirty/untracked/ignored
  inputs, then a reviewed base unequal to origin/main. src/README.md:61-76
  requires the complete committed-candidate gate for SQL/infra work.
* Impact: no full receipt, current-base verification, exact-head publication
  assessment or publication acceptance can be claimed. The runner has not
  yet been attempted; refusal is predicted from inspected admission logic,
  not an observed gate result. Fresh local results do not replace it.
* Destination: distinct coordinator publication/current-base follow-up;
  remaining P02-T02 accounting stays with the active parent.
* Smallest useful next action: preserve the no-publication hold and this
  pinned Review. Parent records the actual evidence commit and any permitted
  gate refusal truthfully. Coordinator separately resolves current-base
  reconciliation, then requires a clean committed candidate, complete gate,
  fresh current-main comparison/receipt verification and distinct read-only
  exact-head assessment. Do not silently rebase, fabricate a receipt, waive
  prerequisites, push or repeat this original Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Funded live renewal and exact operational approval remain unproven

* Related scope: AC2-AC4; owner live/funding/operational follow-up.
* Evidence: infra/README.md:3677-3773 explicitly marks rotation/live apply
  Pending, requires a separately reviewed existing-secret version operation,
  individually approved SQL rows, exact image/configuration, rollback/
  verification intervals and fresh non-overlapping <= USD700 liabilities.
  Current changes and caller confirm no live apply, credential access,
  billing query or owner sign-in. Editing the policy does not change deployed
  configuration, existing secret versions or row expiries.
* Impact: the source and technical plan are credible, but cannot prove live
  January access, completed owner review/rotation or budget availability.
  USD25.50 is an assumed January increment with reserve, not granted funding
  or demonstrated headroom. This is intentionally deferred operational work,
  not a source defect.
* Destination: distinct owner operational/funding follow-up.
* Smallest useful next action: owner and authorized operator select the exact
  operation/version/row set and bounded refresh/rollback/verification plan,
  establish current full liabilities and approved resident allocation,
  obtain separate exact confirmation and only then apply/verify/record.
  Preserve Create-only refusal, synthetic resident-only scope, min0/max1,
  narrow private access and independent inference cutoff. Nothing in this
  Review authorizes that operation or closes #521.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Changed-infra static checks remain failed on recorded baseline debt

* Related scope: P01-T01; PC-005; infra-maintainer follow-up.
* Evidence: changes' P01-T01 final local results and Targeted infra findings;
  details' changed-infra selector list and Current Execution Reconciliation.
  Recorded checks cover infra/scripts/resident_showcase_sql.py,
  infra/tests/test_resident_demo_deploy.py and
  infra/tests/test_resident_demo_secrets.py. Ruff RUF100/FURB162, renderer
  formatting and invariant attrs_before dict typing fail; corrected baseline
  probes using a02984e8 reproduce the same findings. Initial baseline
  mode/import-path probe errors are distinguished from the final comparison.
* Impact: these checks cannot be described as passing. The recorded baseline
  comparison and unchanged offending expressions do not establish an
  authority-change regression, so unrelated cleanup is not a prerequisite
  invented by this Review. API/core static success does not cover these files.
* Destination: distinct infra-maintainer static-debt follow-up.
* Smallest useful next action: retain failed status and baseline evidence;
  track targeted lint/format/driver typing remediation separately with its
  own scoped validation. Do not add ignores or change tests to hide debt.

## Defects

No new source correctness defect or significant unaccepted implementation
decision was independently established in the complete pinned source diff.
RV-001 is a publication blocker; RV-002 and RV-003 are distinct residual
operations/static-debt work, not new active source-fix tasks.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct publication/current-base follow-up; parent retains P02-T02 | Coordinator clears reconciliation/gate/receipt/exact-head prerequisites | Missing later-stage publication evidence, not a source defect |
| RV-002 | Distinct owner operational/funding follow-up | Exercise owner and authorized operator obtain exact approval/funding before live apply/verification | Deliberately deferred live acceptance |
| RV-003 | Distinct infra static-debt follow-up | Infra maintainer scopes baseline lint/format/type repair | Recorded pre-existing failures, no unrelated cleanup here |

No new rpi-implement source fix, rpi-plan design decision or rpi-research
investigation is warranted by the inspected boundary. Required future live
cost/identity evidence is owned by the separately authorized operation, not
permission for an agent to retrieve credentials or cloud data now. Later work
does not require another original Review.

## Validation Evidence

All execution rows below are supplied current implementation results, not
tests run by this reviewer. Runner totals include skipped methods.

| Check/command boundary | Status | Evidence and limit |
| --- | --- | --- |
| Initial namespace/tool probes and pip restoration | Recorded missing imports/tools, then restoration | Changes records justification and existing manifests; no reviewer installation |
| Initial heavy admission | Recorded timeout | 600-second wait expired before setup; not recorded as successful validation |
| Core resident/rendering suites | Recorded passed | 78 total, 27 explicit SQL opt-in skips, exit 0; 51 non-skipped methods |
| Infra secret/deploy fake-CLI selectors | Recorded passed | 32 total, zero skips, exit 0; not compiled Bicep or live what-if/deployment |
| First full API discovery | Recorded failed | 1380 total, 76 errors, 320 skips; isolated PATH omitted installed Node |
| Node-restored retry | Recorded failed before discovery | Wrong repository-root CWD; preserved separately, not application failure evidence |
| Final API discovery from src/api with requested PYTHONPATH | Recorded passed | 1380 total, 320 opt-in integration skips, exit 0; 1060 non-skipped methods |
| API/core Ruff check, format --check and mypy | Recorded passed | Each exit 0; does not imply infra static success |
| Separate test_resident_showcase_sql.SqlBoundaryTests with owned loopback SQL opt-in | Recorded passed | 27 total, zero skips, exit 0; legacy/reapply/trust/rows/rollback/rights included; not Azure MSI/live proof |
| Owned SQL cleanup | Recorded passed | Exact labelled container removed, exit 0; reviewer did not access any container |
| Changed infra Ruff/format/mypy | Recorded failed | Each exit 1; corrected a02984e8 comparison records same failures; RV-003 |
| Read-only git diff --check against pinned base | Passed during Review | Exit 0; whitespace integrity only, not runtime/gate validation |
| Compiled Bicep, container/browser/scanner and complete gate | Not attempted for this final candidate | P02-T02 requires evidence commit; known newer-base drift blocks admission; no partial receipt substituted |
| Current-base receipt verification and final independent exact-head assessment | Unavailable | No complete receipt or final evidence commit; this original Review cannot assess a future candidate |
| Actual spend/headroom, owner operational approval, credential/SQL renewal, live sign-in/apply/verification | Unproven/not performed | Outside authority; RV-002 |

The changes record supplies external log names and hashes for final API,
actual SQL and results.json. This Review relies on the stated results and
inspected test assertions; it does not attest those raw-log hashes.
Historical October 28 failed/blocked results remain original evidence, not
relabelled as October 30 successes.

## Blockers and Remaining Work

* This bounded Review is not blocked: the task set and pinned source boundary
  support the completed comparison.
* P02-T02 remains incomplete. The current uncommitted candidate cannot earn
  an exact-head gate, and the reviewed base differs from recorded newer main.
  No gate execution, passing receipt or final-candidate assessment is claimed.
* Live funding/approval/apply/verification remains separate; AC4 is unproven
  and AC2/AC3 are partial at whole-issue level.
* Targeted infra static failures remain failed and separately routed.
* Parent may reconcile its own completion markers and handoff to this result.
  Reviewer changes neither parent artifacts nor immutable historical outcomes.
* No source/base correction, live action, cloud fallback, protection change,
  publication or second original Review is requested by this record.

## Outcome

* Review execution: Complete.
* Outcome: Residual work.
* Severity summary: 0 Critical, 1 High, 1 Medium, 1 Low.
* The shared exclusive cap, SQL migration, recorded local regression evidence,
  technical rotation/renewal proposal, cost arithmetic and preserved guards
  support the source-only implementation. No new source defect was established.
* Whole-issue acceptance, live readiness and publication acceptance are
  withheld: AC1 is locally proven, AC2/AC3 remain operationally partial, AC4
  is unproven, and the full current-base gate is unavailable.
* The current and historical original adverse critique/Review outcomes remain
  immutable. This result is neither a passing receipt nor permission to spend.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | None established | No source-fix invocation requested |
| Significant decision gap/invalid assumption | None established | Preserve accepted source-only scope; no new planning stage required |
| Material research gap | None newly established | No new research invocation or cloud retrieval authorized |
| Publication/current-base residual | Distinct coordinator follow-up, RV-001 | Parent records remaining P02-T02 state; coordinator clears exact-candidate prerequisites |
| Live operation/funding residual | Distinct owner follow-up, RV-002 | Exact technical/operational review, funding and confirmation before apply |
| Pre-existing static debt | Distinct infra-maintainer follow-up, RV-003 | Separately scope baseline remediation |

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md](.copilot-tracking/research/2026-10-30/resident-authority-extension-521-research.md) | Compared research and source/issue provenance |
| [.copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md](.copilot-tracking/plans/2026-10-30/resident-authority-extension-521-plan.md) | Compared AC1-AC4, markers, critique dispositions and follow-ups |
| [.copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md](.copilot-tracking/details/2026-10-30/resident-authority-extension-521-phase-details.md) | Compared validation isolation, tasks and current execution reconciliation |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-authority-extension-521-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-authority-extension-521-plan-critique.md) | Original Complete / Revise critique, preserved |
| [.copilot-tracking/changes/2026-10-30/resident-authority-extension-521-changes.md](.copilot-tracking/changes/2026-10-30/resident-authority-extension-521-changes.md) | Compared current execution evidence, failures, skips and remaining work |
| [.copilot-tracking/reviews/logs/2026-10-30/resident-authority-extension-521-review.md](.copilot-tracking/reviews/logs/2026-10-30/resident-authority-extension-521-review.md) | This one original October 30 Review: Complete / Residual work |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-authority-extension-521-review.md) | Historical adverse Review, unchanged |
| [infra/README.md](infra/README.md) | Independently assessed renewal/rotation, cost and live-approval plan |

## Next Steps

Return this completed Review to the active parent. Parent records P02-T01
completion and retains P02-T02's actual unmet commit/gate state; coordinator,
owner and infra maintainer own RV-001, RV-002 and RV-003 respectively.
Preserve the publication/live holds and original outcomes. Do not repeat the
original Review, fix sources, execute validation/gates, access cloud/credentials
or push in this assessment. No further reviewer action is required.
