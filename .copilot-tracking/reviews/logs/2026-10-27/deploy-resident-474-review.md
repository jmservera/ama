<!-- markdownlint-disable-file -->
# Review: deploy-resident-474

## Scope and Evidence

Task ID/slug: deploy-resident-474. Date: 2026-10-27.
Scope: one original independent Review of the deployment task, not a second
critique or authenticated/service acceptance.
Plan: .copilot-tracking/plans/2026-10-27/deploy-resident-474-plan.md.
Details: .copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-27/deploy-resident-474-plan-critique.md.
Changes: .copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md.
Research: .copilot-tracking/research/2026-10-27/deploy-resident-474-research.md.
Machine receipts: .copilot-tracking/changes/2026-10-27/deploy-resident-474-evidence/.

## Opening Review State

Goal: compare user requirements, final plan/critique dispositions, deployment
amendment, genuine live evidence and unproved requirements without conflating
safe operational completion with full acceptance.
Readiness: P01/P02 executed; P03 commit/scoped gate/publication pending.
Read-only scope: all sources/evidence; write only this canonical Review record.
First comparison: exact-source image/view deployment, original failed startup,
27 available live checks, cost/restoration and stopped final boundary.
Initial blockers: no owner-held credential access; no Azure runtime/ledger;
no authenticated/expiry/model acceptance; hosted/human approval unperformed.
The independent reviewer owns the complete findings/outcome and routing below.

## Execution Status

* Review execution: Complete. This is the one original independent Review.
* Deployment-task execution: Partial. P01/P02's bounded operations ran; required
  authenticated and Azure OpenAI outcomes did not. P03 publication remains pending.
* Full requested service outcome: Not accepted.
* Evidence-PR readiness: Conditional, not publication approval. Honest partial
  evidence is publishable in principle after RV-003 and the remaining P03 gates.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and evidence | Assessment |
|---|---|---|
| P01-T01 [x] | One remote build failed403; local build, exact-image scan/contracts and restricted push succeeded | Operational completion supported; original failure retained |
| P01-T02 [x] | Image deployed; first real startup failed; exact merged view batch then applied and subsequent HTTPS succeeded | Supported with justified deployment amendment below |
| P02-T01 [x] | Twenty-seven anonymous/negative checks passed; four blocked categories explicit in live receipt | Completed available test execution, not authenticated or AI acceptance |
| P02-T02 [x] | Exact ACR equality; safe preservation snapshots; ingress null/external404; revision inactive/zero replicas | Supported within metadata-only and estimated-cost limitations |
| P03/P03-T01 [ ] | Original Review now completed; commit, scoped receipt, exact-head assessment and publication unperformed | Correctly remains open; this record cannot certify a later candidate |
| Follow-Up Items | Credential-dependent acceptance and MI host/durable ledger engineering | Both remain distinct open follow-ups; neither is waived or added to active implementation |

The checked P02 marker is acceptable only with its stated available-check boundary.
It must never be projected as completion of the user's authenticated requirements.
The plan's closing "First eligible task P01-T01 after critique" is stale prospective
handoff prose; current markers and changes clearly place continuation at P03.
The changes record's earlier "No live check has run yet" and image-only/no-SQL
statements are historical intermediate states, superseded by subsequent named
sections, not current validation or final deployment assertions.

## Completed Work Assessment

| Related marker | What was examined | Completion evidence | Assessment |
|---|---|---|---|
| P01-T01 | Exact source/image release | Source 885ee05fc45122cf7a1ea4f7f003dc88bfda08ee; image sha256:0568deb725e7258c3b09d425b6c0a28a736a2e23434fc22c350bac6333888043; matching scan ImageID/RepoDigests and push digest | Identity supported, not inferred merely from a tag |
| P01-T01 | Fresh image contracts | UID10001; assets present; hardened no-network/no-data invocation; missing configuration exit2; filtered scan zero fixable HIGH/CRITICAL | Passed for those contracts; not a full all-severity scan or configured live SQL contract |
| P01-T02 | SQL projection compatibility | view-admission.json, view-result.json and successful initializer log; recomputed exact third-batch hash d55376da6fe3b6131c261d342a4aa10b55d3b406b172818e2d6b6eeba02dcdc3 | Fourteen to sixteen columns supported; no table/row/grant batches executed |
| P02-T01 | Live HTTPS/Playwright | live-result.json, original first-live-failure.json, bounded live-check.py assertions | Twenty-seven actual checks, including final external404; no genuine login, own-case isolation or expiry proof |
| P02-T02 | Preservation and stop | Safe before/after app/job/SQL/ACR snapshots; revision-final.json | Three non-resident app projections identical; resident projection differs only in image; jobs/SQL/ACR equal; final revision stopped |
| Documentation | Four changed Markdown documents | git diff; index and appended knowledge-base log entry | Accurately distinguish authorization, deterministic deployment, blocked acceptance and final closed service |

No source or test mutation was found in the supplied diff. The four changed
documents are docs/architecture/resident-assistant-prototype.md,
docs/reference/README.md, docs/reference/log.md and src/api/README.md.
No new web implementation occurred; this is not a fresh UI/accessibility audit.

## Implementation-Time Plan and Detail Update Assessment

| Area | Trigger and reconciliation | Assessment |
|---|---|---|
| Four apps rather than three | Inventory corrected research, plan, details and preservation checks | Compatible clarification; stronger preservation, no expanded app deployment |
| Local build/restricted push | One admitted ACR run terminal Failed; fallback explicitly planned | Authorized fallback; script closes public access before restoring restrictions and checks exact equality |
| Merged SQL view amendment | Real startup ProgrammingError after ARM Healthy; initial failure retained; P01-T02 reopened, plan/details/changes updated | Material relative to the original image-only/no-SQL wording, but narrowly compatible with deployment intent; see below |
| Revision deactivation | Ingress closure/min0 still left one replica | Compatible finite-cost cleanup; only tested revision deactivated, final stop explicit |
| Model and authenticated blockers | Runtime lacks host/ledger; credential offline and unavailable under no-read rule | Honest blocked outcomes; no invented acceptance, password replacement, forged positive session or unused provisioning |

### Materiality and authorization of the view amendment

The change is not literally "no SQL change": it is DDL to an existing projection.
It is a material implementation-time deployment amendment, not a row migration
or a permission grant. The initial critique assessed an image-only plan and does
not provide retrospective independent approval of this amendment.

Within the supplied deployment authorization and SQL-preservation constraints,
the exact already-merged compatibility view is a justified interpretation:
it is required by the deployed reader, preserves existing tables/business rows,
principal and rights, and introduces no new source design, resources or grants.
The external deploy-view.py extracts only batch three from the merged file,
uses the existing initializer execution override and MI, runs with
autocommit=False, checks the expected principal and rights before and after,
compares permission snapshots, checks the exact sixteen columns, and rolls back
on failure. verify_principal invokes verify_rights, including role/ownership and
public-grant checks. The successful log reports the original fourteen columns
and matching batch hash. No case-data SELECT is present in that override.

Dependent testing resumed only after terminal initializer success; ingress had
been closed after the original failure. No application source or persistent job
definition change is evidenced. This supports the narrow amendment without
inventing a new owner approval or treating general deployment authority as
permission for arbitrary SQL changes. Sensor data availability and actual
authenticated history remain unproved. No rollback or additional DDL is requested
by this Review.

## Critique and Material Revision Assessment

Original critique outcome Revise is preserved; it is not rewritten as Pass.

| Finding | Independent disposition |
|---|---|
| PC-001 High | Operationally supported: inspected close-first restoration script, normalized owned-rule removal, three retries and raw before/after equality; RV-003 corrects contradictory bypass prose |
| PC-002 High | Supported: owned watchdog scripts and receipts for both windows; deadline armed before exposure; ARM null and external404 after both; HTTPS-only opening |
| PC-003 Medium | Substantially supported for finite release admission: rates/quantities, one terminal remote run, bounded overlap/test window and initializer duration recorded; ancillary charges and actual billing remain unknown |
| PC-004 High | Correct flags incorporated; execution/receipt verification still pending P03, not resolved by this Review |
| PC-005 High | Ancestry-stop/no-rewrite procedure incorporated; HEAD and local origin/main currently equal885ee05f, but fresh publication-time fetch/ancestry evidence pending |
| PC-006 High | Exact-head publication assessment explicitly separate from original Review; still pending after commit/gate |
| PC-007 High | Matching exact-image scan, DB identity, pinned scanner policy and non-secret contracts examined; all-severity report unavailable and not claimed passed |
| PC-008 Medium | Safe app projections and raw before/after comparisons examined; no hidden-value or employee-interactive acceptance inferred |

Thus "all eight applied" describes incorporated procedures, not eight completed
publication gates. Runtime evidence supports the operational dispositions.
The SQL amendment's original-critique coverage is limited as stated above; this
one Review evaluates its actual rationale and evidence rather than requesting
another critique or Review.

## Plan Follow-Up Assessment

| Follow-up | Why distinct | Owner and route |
|---|---|---|
| Genuine authenticated resident journeys and natural expiry | Offline credential unavailable without violating current no-read boundary | Owner-run bounded acceptance follow-up; RV-001 |
| MI Azure OpenAI host and durable inference budget ledger | New reviewed engineering, not deploy-only configuration; no working merged activation route | Separate engineering follow-up beginning with rpi-plan; RV-002 |

These are not implementation defects introduced by this deployment. Moving them
outside active deploy-only implementation does not remove them from the user's
full-task acceptance requirements.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Genuine authenticated resident and expiry acceptance is absent

* Related scope: User requirements; P02-T01; plan Follow-Up Item concerning
  owner-run authenticated acceptance.
* Evidence: .copilot-tracking/changes/2026-10-27/deploy-resident-474-evidence/live-result.json
  explicitly blocks registered login, own-case account/gauges/history/assistant/
  logout render and genuine1800-second expiry. The actual harness uses only
  invalid credentials and a forged cookie. Header markup and matching assets
  prove deployed identity, not authenticated layout or working sign-out.
* Impact: Full requested resident experience and cross-resident isolation are
  not accepted. Forged-cookie denial cannot establish session expiry.
* Destination: Distinct owner-run authenticated acceptance follow-up, not a
  defect in current deploy-only implementation.
* Smallest useful next action: In a separately bounded authorized test, owner
  supplies credentials directly without agent retrieval; reactivate/open only
  for that window, prove own-case features and negative cross-case access,
  top-right account/sign-out, logout replay and genuine natural session expiry,
  then close/stop. Preserve this unmet result until actual proof exists.
* Publication effect: Blocks service acceptance, not a candid partial-evidence PR.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Managed-identity Azure OpenAI activation remains undelivered

* Related scope: User AI requirement; engineering Follow-Up Item.
* Evidence: src/api/src/zava_forward/api/resident_demo/__main__.py constructs the
  deterministic runtime; assistant.py requires explicitly supplied token and
  durable reservation callbacks and retains its historical USD4 contract.
  Research, changes and cost-ledger.json record no model deployment/calls/roles.
* Impact: The requested MI-backed AI outcome is unmet. A USD20 authorization,
  empty deployment inventory or deterministic fallback does not establish a
  functioning capped AI route or tested model-failure fallback.
* Destination: Distinct model-activation engineering follow-up, starting at
  rpi-plan, not new active P01/P02 work and not an in-task implementation defect.
* Smallest useful next action: Plan reviewed MI host wiring, suitable current
  tariff/model and durable atomic aggregate reservations across workers/restarts;
  reconcile historical USD4 with authorized <=USD20, preserve the fresh total
  <=USD30 and 2026-10-31T23:59Z end, refusal/fallback and least privilege.
  Apply its own source/infrastructure gates, not this deploy-only scoped exception.
  After expiry or insufficient remaining headroom, require fresh authority.
* Publication effect: Blocks service acceptance, not a candid partial-evidence PR.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: ACR restoration narrative names the wrong baseline bypass

* Related scope: P01-T01; PC-001; evidence truthfulness.
* Evidence: .copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md,
  "Image release completed", says "bypass AzureServices unchanged".
  Both committed acr.before.json and acr.after.json instead contain
  "bypass": "None"; the external raw snapshots agree and independently compare equal.
* Impact: An audit narrative misstates an important network-policy property.
  Restoration succeeded for the evidenced None baseline; it did not demonstrate
  preservation of an AzureServices baseline.
* Destination: Later rpi-implement evidence-only correction on the same topic.
* Smallest useful next action: Correct the current descriptive sentence to the
  evidenced None value, preserving original raw receipts, failed build/startup
  and this Review. Do not change cloud policy to match the prose.
* Publication effect: Correct before final candidate commit/gate and exact-head
  assessment. The correction does not require this Review to run again.

## Defects

* RV-003 is an evidence-documentation defect, not an observed cloud-restoration
  failure. No source defect was established within this deployment-only boundary.

## Routed Findings

| Finding | Destination | Owner and next action |
|---|---|---|
| RV-001 High | Distinct authenticated-acceptance follow-up | Owner performs credential-dependent bounded live proof |
| RV-002 High | Distinct model-activation engineering follow-up, rpi-plan first | Engineering parent scopes host/MI/tariff/ledger/fallback work |
| RV-003 Medium | rpi-implement | Deployment parent corrects bypass narrative before publication gates |

## Residual Work

* Retain the two existing plan follow-ups as open; neither is a waiver.
* Reconcile delayed release billing against the fresh allocation when available.
  The USD0.053977 compute/request estimate excludes unknown ancillary charges;
  USD1 is a reservation, not an invoice or enforceable hard cap.
* Employee interactive login, hidden-setting preservation, whole-issue462,
  human/hosted approval and accessibility acceptance were not established.

## Blockers and Remaining Work

* B1: No genuine owner-held credential access; RV-001.
* B2: No merged model runtime or durable cost ledger; RV-002.
* P03 remains active: correct RV-003, commit original artifacts, fetch current
  main, check ancestry, run --changed --lock-timeout0 gate with fresh external
  output, verify --required-scope partial, obtain independent exact-head
  publication assessment and reverify immediately before push.
* The supplied user explicitly substitutes the scoped gate for --all for this
  deploy-only evidence PR. This Review does not reinstate --all or extend the
  exception to later engineering. No receipt or final-head approval exists yet.
* Original adverse outcomes remain unchanged. No second RPI Review is required.

## Validation Evidence

| Check | Status | Boundary |
|---|---|---|
| Direct artifact/source/diff comparison | Passed | Exact requested research/plan/details/critique/changes, receipts, relevant source and four changed documents |
| Durable evidence SHA256/size verification | Passed | All13 indexed files match committed manifest at the supplied release-2026-10-27-474 root; manifest's original session-root pointer remains historical |
| Recomputed merged third-batch SHA256 | Passed | Matches admission, SQL execution log and committed result |
| Raw safe preservation comparisons | Passed | Three non-resident app projections identical; resident only image delta; eight jobs, SQL SKU and ACR policies equal |
| Scan report/image/push linkage | Passed | Exact digest and merged-source label; zero fixable HIGH/CRITICAL in retained filtered report |
| Image contracts | Passed, supplied execution | Non-root/hardened/no-data/assets and missing-config refusal, not live positive authentication |
| First live startup | Failed, retained | HTTPS readiness failed before view correction; ARM Healthy was insufficient |
| Second live HTTPS/Playwright | Passed, supplied execution |27 checks; direct inspection confirms the assertions and limits |
| Registered features/real logout/natural expiry | Unavailable | No credential access within approved boundary |
| Azure MI model and live failure fallback | Not run | Missing runtime/ledger; no unused paid provisioning |
| Full all-severity scan report | Unavailable | Timeout-zero lock contention; blocking policy report exists and was examined |
| Fresh scoped gate/exact-head/hosted approval | Not run | P03 pending; not prerequisites falsely credited to this Review |
| git diff --check | Passed | Reviewer ran against supplied working diff |

Reviewer validation was read-only and local: no cloud calls, secret/.env reads,
new live sessions, image rebuilds, scans, commits, pushes or agent launches.
Operational receipts are supplied execution evidence independently reconciled
here, not a claim that the reviewer repeated cloud operations. The manifest
records DB timestamps; this Review did not restore or independently rescan that DB.

## Outcome

* Review execution: Complete.
* Deployment-task execution: Partial.
* Outcome: Not accepted for the full requested deployed service.
* Severity summary:0 Critical,2 High unmet-outcome findings,1 Medium evidence defect.
* The exact merged image/view deployment, negative tests and closed/stopped
  restoration have credible bounded evidence and justified operational divergence.
  They do not satisfy the two principal missing authenticated/AI outcomes.
* Candid partial-evidence PR publication is separately supportable in principle
  after RV-003 and actual P03 completion. This is neither final-head approval nor
  authority to claim service acceptance, close issues or bypass hosted/human gates.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation/evidence defect | rpi-implement | Parent corrects RV-003 before final candidate/gate |
| Significant unresolved in-task decision gap | None | Narrow exact-merged view amendment justified; no broader SQL authority inferred |
| New material research gap | None within deploy-only scope | Later model scope must obtain its own tariff/capability evidence |
| Residual required acceptance | Distinct owner follow-up | RV-001, genuine authenticated session/features/expiry |
| Residual required engineering | Distinct follow-up beginning at rpi-plan | RV-002, MI host/ledger and actual activation/fallback |
| Remaining active plan work | P03-T01 | Commit, fresh scoped receipt/verification, independent exact-head assessment, conditional push/PR |

| [.copilot-tracking/research/2026-10-27/deploy-resident-474-research.md](../../../research/2026-10-27/deploy-resident-474-research.md) | Deployment research |
| [.copilot-tracking/plans/2026-10-27/deploy-resident-474-plan.md](../../../plans/2026-10-27/deploy-resident-474-plan.md) | Active plan and distinct follow-ups |
| [.copilot-tracking/details/2026-10-27/deploy-resident-474-phase-details.md](../../../details/2026-10-27/deploy-resident-474-phase-details.md) | Operational details and publication sequence |
| [.copilot-tracking/reviews/plans/2026-10-27/deploy-resident-474-plan-critique.md](../../plans/2026-10-27/deploy-resident-474-plan-critique.md) | Original Revise critique |
| [.copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md](../../../changes/2026-10-27/deploy-resident-474-changes.md) | Partial execution and RV-003 correction target |
| [.copilot-tracking/changes/2026-10-27/deploy-resident-474-evidence/live-result.json](../../../changes/2026-10-27/deploy-resident-474-evidence/live-result.json) | Actual checks and explicit blocked outcomes |
| [.copilot-tracking/reviews/logs/2026-10-27/deploy-resident-474-review.md](deploy-resident-474-review.md) | One original independent Review |

## Next Steps

Return to the active parent: apply RV-003 through later rpi-implement, preserve
this original Review, and continue P03 only through its actual scoped-gate and
exact-head publication checks. Keep RV-001/RV-002 as separate unmet follow-ups.
Do not invoke another RPI Review or represent partial publication as service
acceptance. No immediate owner action is required to correct the evidence.
