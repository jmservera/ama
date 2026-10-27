<!-- markdownlint-disable-file -->
# Review: Retire legacy MVP directories

## Scope and Evidence

* Task ID: issue-201
* Task slug: mvp-cutover-201
* Date: 2026-10-27
* Scope: completed source/validation P01-P02; P03 publication pending.
* Plan: .copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md
* Details: .copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/mvp-cutover-201-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/mvp-cutover-201-changes.md
* Research: .copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md

## Opening Review State

* Goal: independently assess surgical retirement, evidence preservation,
  reference reconciliation and scoped test evidence before publication.
* Readiness: plan/details/changes agree P01/P02 complete, P03 pending;
  original Revise critique has recorded dispositions.
* Acceptance: user-directed deletion after 2026-10-27 sign-off; local-only tag,
  no full gate/check rename/private data reads; Refs for all five issues.
* Comparison: actual diff against main65a514ed and scoped test logs.
* Read-only: only this canonical Review record may be written.
* Blockers: none known; verdict not yet assessed.
* Independent review opening: artifact set resolved; source boundary is the
  16 changed non-tracking files against
  65a514ed20e97816dbf47e9fb981ab4cfe40597d. Validation logs are available
  externally; no full gate, test rerun, source fixes or publication authorized
  in this Review.
* Initial source-diff SHA256: c06d4a24ea2c37e8166fa7c3d05fbaf4fdaff675a335f170e777e6ffef165404.

## Execution Status

* Review execution status: Complete.
* Review execution evidence: one independent post-implementation Review on
  2026-10-27, comparing all supplied RPI artifacts, the complete 16-file
  non-tracking diff, existing validation receipts and cheap read-only assertions.
* Full-plan execution remains Partial: P01/P02 are complete; this record
  supplies P03-T01 evidence. P03-T02 commit/push/PR has not run in this Review.
  The parent owns later marker reconciliation and publication.
* Original critique execution Complete / verdict Revise is preserved. No
  second critique, source implementation, test-suite rerun or second Review
  occurred.

## Assessed Source Identity

* Base and observed origin/main:
  65a514ed20e97816dbf47e9fb981ab4cfe40597d.
* Branch: chore/mvp-cutover-201; HEAD was the base during assessment.
* Exact command:
  git diff --binary 65a514ed20e97816dbf47e9fb981ab4cfe40597d -- . ':!.copilot-tracking/**'
* SHA256 of command stdout:
  c06d4a24ea2c37e8166fa7c3d05fbaf4fdaff675a335f170e777e6ffef165404.
* Initial and final hashes match. This freezes the assessed source delta,
  including staged pointer deletion and unstaged documentation edits, not
  future publication metadata or tracking-record changes. The parent can
  compare the final committed source delta against this value without
  repeating Review. A different source delta is not covered by this verdict.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Local archive and pointer retirement | Reconciled | Base tree contains only mvp/README.md; prototype already absent. Local annotated tag and deletion match the plan. |
| P01-T02 | Live guidance reconciliation and final reference sweep | Reconciled | Current instructions/navigation corrected; historical outcomes and old log bytes retained with additive repair map. |
| P02-T01 | Initial failures, prerequisite restoration and final validation | Reconciled | Existing logs substantiate final passing scoped runs and explained skips; original failures remain available. No manifests changed. |
| P03-T01 | One independent Review | Reconciled by this record | Parent may mark complete after receiving this original outcome; opening pending markers were honest at handoff. |
| P03-T02 | Authorized maintenance PR | Pending, intentionally | No commit/push/PR claimed. Required Refs, identity, branch-only publication and retained hosted checks remain publication obligations. |
| Follow-Up Items | Broader hosted/deployed/baseline/rubric/release acceptance | Reconciled | Explicitly outside P01/P02; not converted into source defects or closure claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | mvp/README.md | Delete obsolete pointer only | Base Git tree has this sole legacy file; current tracked/path queries empty | Semantic assertions independently rerun | Safe pointer retirement; no application code removed |
| P01-T01 | README.md | Archive target and exact owner push command | Annotated v0.21.0 object 0096b11301236c6eef85fd3cdefc657582109b8a targets the base; archived BRD version is 0.21.0 | Git object/type/target/version readback | Correct pointer-era archive, not a claim that earlier executable modules remain in that tree |
| P01-T02 | .github/copilot-instructions.md; .github/agents/ama-backlog-delivery-coordinator.agent.md | Replace transitional location/retirement facts only | Complete two bounded diff hunks inspected; current owner sign-off is explicit | Static delta assessment only | Minor factual improvement; no broader prompt audit or tools-frontmatter inspection performed |
| P01-T02 | src/README.md; src/core/README.md | Current source index, retirement status and eval registry description | Source guides and registry agree; migrated project links exist | Changed-link assertions and registry receipt | Conformant |
| P01-T02 | .github/rubric/README.md; docs/capstone/README.md | Match existing source/synthetic-generator scoring includes | .github/rubric/artifacts.json includes src and registered generator scripts, not mvp | Registry read; no private generator data opened | Correct factual prose; no new rubric score claimed |
| P01-T02 | docs/architecture/mvp-to-src-parity-matrix.md; docs/architecture/README.md | Replace live pointer navigation and expose dated retirement | New source and evidence-pack destinations resolve | Changed-link assertions | Historical matrix/audit content not regenerated |
| P01-T02 | docs/architecture/cutover-evidence-pack.md; docs/adrs/0006-src-layout-and-cutover.md | Qualify original date and append prospective owner authority | Original evidence-pack body and prior ADR decision text independently checked as preserved byte sequences | Diff inspection and byte assertions | Failed bootstrap, blocked gates and original unchecked outcomes remain historical, not reclassified as passed |
| P01-T02 | docs/prds/zava-forward-retrofit-programme-demonstrator.md; docs/reference/research/ux/regulatory-literacy-for-journeys.md | Repair current source locations without requirements/legal changes | Dated PRD baseline retained; assistants.py destination exists | Full changed hunks and semantic checks | Immediately relevant location repairs, no scope expansion |
| P01-T02 | docs/reference/README.md; docs/reference/log.md | Update KB routing and append retirement/old-anchor repair map | Original log is exact byte prefix; new source anchors resolve | Independent semantic rerun | All four old log occurrences retained; three distinct old targets intentionally remain broken in historical entries, with additive destinations |
| P02-T01 | Existing tests, workflow files and manifests unchanged | Validate without new code or regenerated reports | API/rename/parity receipts and unchanged tracked-file queries | Passed within stated skip boundary | No runtime, workflow/check-name, pin or test change |

Retirement is safe within this accepted source boundary: main already uses
installed source distributions and src-context image builds. Direct inspection
of retained CI commands and Dockerfile guidance confirms these locations;
anchored legacy Python-import search in src/infra/tools found none. Legacy
data refusal checks, old check/image identifiers, audit parser fixtures, dated
snapshots and pinned URLs are intentional, not current build inputs. The
unchanged workflow diff establishes check-name continuity without renaming or
removing required contexts.

The current owner's SIGNED OFF #201 direction dated 2026-10-27 is the
prospective retirement authority. Earlier unsigned records do not veto that
later authority; equally, the new direction is not evidence that historical
technical, private-backup, operational or human-approval gates passed.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 / PC-001 | Explicit sanitized test-launch contract | Tests have opt-in SQL/browser integrations; current caller permits task-owned external evidence | Details and changes specify env -i, isolated scratch/home/data/cache and no inherited credentials or integration settings | Original High finding retained; applicable safety correction applied before execution | Compatible correction, no missing owner decision |
| P01-T01 / P03-T02 / PC-002 | Derive authenticated privacy-safe identity rather than literal email | Repository identity requirement | Details/changes record fresh derivation before tag; future commit repeats derivation | Original Medium finding retained and disposed | Completed tag handling reconciled; commit handling remains pending publication |
| P03-T02 / PC-003 | Unconditional Refs for all five issues in this PR | W1-W5 show broader criteria unproved; current owner only permits closure if all criteria are proven | Plan and details lock publication to Refs #199-#203 | Original Medium finding and original provenance wording retained, corrected interpretation recorded in plan | Preserves current owner intent; no unauthorized closure escape |
| P01-T02 | Regulatory UX path, actual assistant anchor destination and coordinator factual retirement note | Final source-reference sweep | Plan/details target list and changes record name the additions and narrow rationale | No material architecture, capability, requirements or autonomy change needing another critique | Justified immediately related reconciliation |
| P02-T01 | Restore missing packages and expose existing Node in allowlisted PATH | Preserved initial import/PIL/pptx/Node failures | Final results, pinned dependency sources and unchanged manifests recorded | Environment correction only, not a new implementation direction | Adequately evidenced and bounded |

The two instruction deltas meet the supplied HVE Builder Minor improve
boundary: behavior gate Satisfied-and-skipped, execution Not run, fidelity
Not applicable, verdict Not applicable. This Review assesses only factual
source-location/retirement wording, not capabilities or tools frontmatter.
No comprehensive HVE conformance or executed behavior claim is inferred.

## Critique and Material Revision Assessment

* PC-001 through PC-003 have explicit dispositions and resolving changes.
  The original Complete / Revise and severity findings remain untouched.
* The applicable PC-001 requirement is isolation from inherited application,
  SQL and cloud settings. The parent rejected its unsupported system-scratch
  restriction under the current external-evidence authority; that does not
  discard the substantive isolation requirement. Review performed no
  scratch-file writes or test launches.
* No significant/divergent implementation decision requiring new user
  acceptance was found. The added source-location targets and prerequisite
  restoration preserve the approved maintenance direction.
* Plan/details/changes agree on completed P01/P02, pending P03 and distinct
  follow-ups. No evidence of dependent work resuming before the critique
  dispositions was found in the supplied execution chronology.
* Phase details' shorthand "Accepted/Not accepted" is not used as Review
  vocabulary here; this record preserves execution and outcome separately
  using the canonical vocabulary.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Hosted CI, deployed health and broader acceptance for #199-#203 | Requires hosted/deployed evidence beyond pointer/prose retirement | Owner/coordinator retains issue acceptance; run retained hosted checks on published candidate | Open distinct follow-up, not a defect |
| All-suite baseline comparison and post-merge rubric comparison | Scoped API results are not all-suite baseline parity or post-merge scores | Owner/coordinator obtains separately authorized comparison evidence | Open distinct follow-up, no fabricated acceptance |
| Archive tag publication/release | Agent tag push/release expressly prohibited | Owner may run git push origin refs/tags/v0.21.0:refs/tags/v0.21.0 | Open owner-only follow-up |
| Existing changed-document link debt | Pre-existing links unrelated to this retirement | Owner/coordinator may triage separately if desired | Recorded baseline debt: architecture index 1, KB index 1, log 7 distinct failures; not claimed repaired |

## Findings

No substantive RV-xxx findings within the assessed P01/P02 source and
validation boundary. Severity counts: Critical 0; High 0; Medium 0; Low 0.
Unrun broader acceptance and pending publication are explicit remaining work,
not defects in this bounded implementation.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | No rpi-implement, rpi-plan or rpi-research handoff | Parent continues P03-T02 | No source defect, unaccepted decision or material evidence gap found |

Later implementation of any separately identified work does not require this
Review to run again or its original outcome to be rewritten.

## Residual Work

* Distinct owner/coordinator follow-ups are listed above. They remain outside
  the accepted retirement scope and do not authorize issue closure.
* The local archive tag was verified; remote absence/no prior tag push is
  supplied dated execution evidence, not freshly queried in this Review.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: parent records P03-T01 completion and performs
  authorized P03-T02 publication with fresh main/account checks, required
  trailer, source-identity comparison and branch-only --no-follow-tags push.
  Review performed no commit, push, tag mutation, cloud change or merge.
* Hosted checks and owner merge remain independent gates. All five issues
  must remain non-closing Refs in the PR.

## Validation Evidence

External receipt root supplied to and inspected by this Review:
/home/azureuser/.copilot/session-state/064745c5-eb4a-4eda-a5d3-e54696e0c15f/files/cutover-201/.
These files are external evidence, not committed full-gate receipts.

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q, from src/api | Requested API discovery | Passed, receipt inspected; not rerun | api-final.log records 1121 tests in 423.800s, OK, 314 skips; 807 non-skipped |
| skip-reasons.json and source skip explanation in changes | API coverage boundary | Skipped with reasons | 313 declared skips: 308 SQL and 5 browser; one dynamic JSON-store SQL-COMMIT-inapplicability skip. No SQL/browser integration success claimed |
| python3 tools/rename-zava-tests.py | Requested rename regressions | Passed, receipt inspected | rename.log records 25 tests, zero skips; broken.pptx diagnostic belongs to exercised negative fixture, final result OK |
| python3 -m unittest test_cutover_audit test_eval_registry -q with fixture-only PYTHONPATH | Existing parity/registry selectors | Passed, receipt inspected | parity-registry.log records 17 tests, zero skips |
| api-initial.log; api.log; rename-initial.log | Original prerequisite attempts | Failed, preserved | 69 tests/53 import errors; later 1058 tests/6 prerequisite errors/310 skips; rename 25 tests/7 missing-package errors. Final success does not erase these results |
| semantic-final.json and python3 -B verify_cutover.py | Directory, tag, workflow, original log and changed links | Passed, independently rerun read-only | No filesystem/tracked legacy paths; annotated tag at base; unchanged workflow bytes; exact log prefix; zero new/changed link failures except explicitly preserved old log targets |
| Git object/type/version and base-tree queries | Archive correctness | Passed independently | Exact object/target matches supplied values; BRD 0.21.0; only mvp/README.md existed in legacy base paths |
| Byte preservation assertions and complete source diff | Historical evidence | Passed independently | Original evidence-pack body and prior ADR decision text retained; no historical outcome rewriting, memory/original case study changes or regenerated audit TSVs |
| git diff --check; git diff --cached --check | Source whitespace | Passed independently | No errors |
| Anchored legacy Python-import search; current CI/build-path inspection | Live source inputs | Passed independently | No legacy namespace imports in src/infra/tools; retained workflow commands use installed src distributions and src image contexts |
| git diff --binary BASE -- . ':!.copilot-tracking/**' SHA256 | Assessed source identity | Passed independently | Same hash before and after assessment; frozen above |
| Full rpi-checks --all; optional --changed | Broader gate | Skipped | Full gate expressly unauthorized; optional changed tier unnecessary for accepted bounded work |
| Hosted/deployed/full SQL/browser/baseline/rubric/release acceptance | Broader issue acceptance | Not run / unavailable in this Review | Distinct owner/CI follow-up; no whole-issue closure or deployment inference |

## Outcome

* Outcome: Conformant.
* Outcome rationale: completed P01/P02 implement the authorized surgical
  retirement and honest evidence boundaries. Archive, current navigation,
  preserved historical bytes and unchanged workflow identities are verified;
  final scoped tests pass with explained opt-outs. No material source,
  decision or evidence gap remains in this boundary.
* This is not a full-plan completion, hosted approval, release authorization
  or whole-issue acceptance verdict. P03 publication and broader follow-ups
  remain explicitly pending.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No later source correction requested |
| Decision gap or invalid assumption | None | Current owner authority respected |
| Material evidence gap | None within boundary | No additional research requested |
| Non-blocking residual work | Distinct follow-ups above | Owner/coordinator retains broader acceptance and tag publication |

* Review execution status: Complete.
* Full-plan execution status: Partial, pending P03-T02.
* Outcome: Conformant within completed P01/P02.
* Validation coverage: 1121 API tests with 314 explained skips, 25 rename
  tests, 17 parity/registry tests; independent cheap semantic/byte/hash checks.
* Blockers: none for the bounded source result; hosted/owner approval is not
  established by this Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md](.copilot-tracking/research/2026-10-27/mvp-cutover-201-research.md) | Research and issue evidence |
| [.copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md](.copilot-tracking/plans/2026-10-27/mvp-cutover-201-plan.md) | Assessed current plan and dispositions |
| [.copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md](.copilot-tracking/details/2026-10-27/mvp-cutover-201-phase-details.md) | Assessed task details |
| [.copilot-tracking/changes/2026-10-27/mvp-cutover-201-changes.md](.copilot-tracking/changes/2026-10-27/mvp-cutover-201-changes.md) | Original execution results and remaining work |
| [.copilot-tracking/reviews/plans/2026-10-27/mvp-cutover-201-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/mvp-cutover-201-plan-critique.md) | Preserved original Complete / Revise critique |
| [.copilot-tracking/reviews/logs/2026-10-27/mvp-cutover-201-review.md](.copilot-tracking/reviews/logs/2026-10-27/mvp-cutover-201-review.md) | This one independent Review and frozen source identity |

## Next Steps

Return this original Complete / Conformant Review to the active parent for
P03 reconciliation and authorized branch/PR publication. Preserve Refs for all
five issues, compare the final source hash, and retain separate hosted checks
and owner acceptance. No additional RPI Review, plan critique or source fix is
requested. No user action is required for this review handoff.
