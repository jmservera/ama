<!-- markdownlint-disable-file -->
# Review: Issue 349 PR437 technical partial-delivery readiness

## Scope and Evidence

* Task ID: 349-tenant-readiness-preflight (PR-wide, all 2026-10-22 to 2026-10-26 cycles)
* Review date: 2026-10-26
* Review scope: whole technical PR artifact reconciliation; documentary and read-only. Not a source review.
* Assessed boundary: head 1da56057302b3c6ba0a8bfcb0991d863f7e03ff7, main acafc6ee04e3612cd62349ab9e4a0af3b24e8109; plans, phase details, critiques, changes records, reviews, follow-up items and process disclosures under .copilot-tracking for issue349.

## Opening Review State

* Interpreted review goal: decide whether the supplied artifacts reconcile enough to support a technical partial-delivery merge recommendation, without narrowing the original plan silently.
* Evidence readiness: all artifact sets present; final gate receipt and coordinator verification supplied (receipt SHA256 e35fecc03878bba80c50ca89aef37e4bc5c2c4f1f48e1ddc9ab10cd3692bdd2a).
* Acceptance basis: original plan (2026-10-22) requirements and critique dispositions, later correction plans, owner/coordinator instructions.
* First comparison boundary: original plan scope and file ownership versus the final PR file set.
* Active read-only boundaries: this record is the only file written; no source, plan, review or git change.
* Initial blockers: none.

## Execution Status

* Execution status: Partial
* Review execution evidence: executed once, 2026-10-26, inline by the active RPI parent. Read: original plan, critique dispositions, phase markers and follow-up items; review outcomes of 2026-10-22 to 2026-10-26; the 2026-10-26 plans, changes and reviews; gate receipt fields (status passed, 17 groups, head 1da56057); retained correction2 hashes (12 OK by sha256sum -c, read only); git diff names and reflog (merge amend tree identical to its pre-amend commit, message only).
* Not read or rerun, by instruction: source line by line (coordinator inspected), tests, Docker, builds, gates, cloud, hosted CI logs. Review is Partial because source, hosted results and live acceptance are outside the boundary; they are not claimed.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| Original P01-P03 (checker, tests, validation, draft PR), 2026-10-22 | changes 2026-10-22 plus correction1 to correction3 | Reconciled | Markers [x] are pre-gate snapshots; later receipts supply state (disclosed in PR body) |
| 2026-10-23 to 2026-10-25 current-main, ama-restart, main-integration, remote-reconcile | dated changes records, critiques Revise with dispositions, Conformant reviews | Reconciled | Historical diagnoses stay dated; Entra-authoritative note added |
| 2026-10-26 main-c8d1 integration | changes plus verbatim review preservation | Reconciled | Review preserved after the fact; disclosed in record |
| 2026-10-26 image-scan-correction1 | changes, review preserved verbatim | Reconciled | Cache-warm correction rejected as non-durable; Medium evidence gap closed by correction2 |
| 2026-10-26 image-no-cache-correction2 | changes, review preserved verbatim | Partial | Plan markers for phases 2 to 5 still unchecked although executed (changes record shows actual order) |
| 2026-10-26 main-acafc6ee integration | changes only | Partial | No critique file or review for this plan; changes record states no review was run (a decision, not an outcome) |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| Original P01-P02 | infra/scripts/tenant-readiness-preflight.py, infra/tests/test_tenant_readiness_preflight.py | read-only diagnostic; 13-role alignment (A1) | original review Conformant for bounded slice; coordinator inspected source and tests | 35 focused tests, coordinator-reproduced | Reconciled |
| Original P03 | receipts, draft PR | gate and draft publication | final receipt e35fecc0 passed, 17 groups, head 1da56057, coordinator verified | gate plus verify | Reconciled for technical gate; hosted and live separate |
| correction2 image | tools/rpi-checks.py, tools/test_rpi_checks.py | scanned image builds use --no-cache via one helper | /mnt/ama-rpi-gates/issue349-image-correction2 (12 hashes OK, versions deb12u2, exit 0) and fresh 17-group scans | 49 tests, lint, format (coordinator) | Reconciled; scope gap RV-001 |
| .github/rubric/scores/latest.json | bot | rubric baseline | bot-only delta, coordinator verified | none needed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|----------------------------------------|--------------------------|-----------------------------|------------|
| Original file ownership and non-goals (no edits to tools/rpi-checks.py) | runner changed | failed gate 0fe8c3be; coordinator authorisation in a session instruction, 2026-10-26 | correction plans and changes record the change | critique Revise before edit, summarised; original plan never amended | Gap: RV-001 |
| Original criteria (database staff roster) | superseded by Entra authority | owner-approved #360/#449 | PR body and 2026-10-25 records | no plan amendment of issue criteria | Gap: RV-002 |
| 13-role test (A1) | test aligned to ADMIN_ROLE | concrete current-main discrepancy | main-integration changes | critique Revise applied | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: original, current-main, correction2 and correction3 critiques are files with verdicts Revise and dispositions; ama-restart, remote-reconcile, main-integration, image-scan1, image-no-cache2 and c8d1 critiques are recorded only as plan markers or changes summaries.
* Material revisions: the runner change is a material scope extension; no fresh critique-bearing plan amends the original ownership boundary.
* Dependent-work pause assessment: no early resumption found; critiques preceded edits per recorded chronology (disclosed unverifiable by file for summarised ones).
* Justification assessment: supported by failed-gate evidence and coordinator authorisation; not by an owner-approved plan amendment.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live callback, browser and positive/negative API acceptance | tenant authority, human | tenant owner | Open; distinct follow-up |
| Hosted exact-head CI at 1da56057 | external | coordinator | Open |
| Independent coordinator exact-head assessment | external | coordinator | Open (in progress) |
| #349 criteria rewrite (database staff roster obsolete) | owner decision | owner | Open; RV-002 |
| #360 private transport, #126 budget and tranche | separate gates | owners | Open; untouched |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Runner change exceeds the original plan boundary without a plan amendment

* Related scope: original Scope, User Decisions (strict file ownership), correction2 image plan
* Evidence: plans/2026-10-22/issue349-tenant-readiness-preflight-plan.md forbids edits to tools/rpi-checks.py; git diff origin/main to HEAD includes tools/rpi-checks.py and tools/test_rpi_checks.py; authorisation exists only in session instructions and the 2026-10-26 correction plans.
* Impact: the original plan supports a bounded read-only diagnostic slice (its decision list says bounded, not full live acceptance, Refs only), but does not support the runner change. The partial boundary is the preflight plus a tightly coupled gate fix only if the coordinator or owner accepts that extension.
* Destination: rpi-plan (decision gap)
* Smallest useful next action: coordinator or owner records an explicit decision accepting the runner correction as part of PR437, or splits it to a separate PR.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Original #349 acceptance includes an obsolete database-staff criterion

* Related scope: original Acceptance, issue #349
* Evidence: PR body and 2026-10-25 records; owner-approved Entra-authoritative roles.
* Impact: no whole-issue acceptance is possible; the PR must stay Refs only and criteria unticked.
* Destination: rpi-plan (owner decision on issue criteria)
* Smallest useful next action: owner updates or reinterprets criteria; nothing is ticked from this PR.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Critique returns for 2026-10-24 to 2026-10-26 cycles are summarised, not preserved as files

* Related scope: ama-restart, remote-reconcile, main-integration, image-scan1, image-no-cache2, c8d1
* Evidence: plan markers and changes records; no reviews/plans files for these.
* Impact: critique execution and dispositions rely on recorded summaries; originals cannot be re-verified.
* Destination: follow-up (disclosure only; no fabrication or rerun)
* Smallest useful next action: accept as disclosed or record a coordinator waiver.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Stale plan markers and missing critique/review for the acafc6ee integration

* Related scope: image-no-cache-correction2 plan phases 2 to 5; main-acafc6ee integration plan
* Evidence: unchecked markers; changes record states no review was run.
* Impact: documentary only; later receipt and logs supply state.
* Destination: follow-up (documentary)
* Smallest useful next action: none required beyond disclosure.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Process nonconformances awaiting disposition (not waived)

* Related scope: merge 147980af; final gate launch
* Evidence: reflog shows 211d048e amended to 147980af; the two commits have identical trees (message only; trailer added). The final gate was started with nohup against launch instructions. Receipt passed, 17 groups, head 1da56057, coordinator verified.
* Impact: functional risk is not indicated by the evidence (identical tree; verified passing receipt). The nonconformances are process breaches of explicit instructions. This review does not decide whether they block or clear merge.
* Destination: follow-up (owner or coordinator disposition)
* Smallest useful next action: the coordinator or owner records a disposition for both items; the exact approval is a written acceptance of the amend and the nohup launch, or a requirement to redo.

<!-- rpi:review id=RV-006 -->
### RV-006 [Low]: Byte-preserved patch archives trigger whitespace warnings

* Related scope: research/2026-10-23/issue349-current-main-evidence/score-3b881a65.patch, score-6c284d45.patch
* Evidence: archived historical diffs; not edited.
* Impact: known archived evidence, not source whitespace.
* Destination: none
* Smallest useful next action: keep bytes unchanged.

## Defects

* None found within the read boundary.

## Routed Findings

* rpi-plan: RV-001, RV-002 (decision gaps; coordinator or owner)
* follow-up: RV-003, RV-004, RV-005, live acceptance, hosted CI, coordinator exact-head assessment
* rpi-research: none. The original image Medium evidence gap is closed by retained correction2 artifacts (12 hashes OK, openssl and libssl3 deb12u2 in all four).

## Outcome

* Execution status: Partial.
* Outcome: Residual work. Original Conformant, Residual-work and adverse reviews are unaltered and none is relabelled a Pass.
* Technical partial merge recommendation: not supportable yet. It becomes supportable once (a) RV-001 is decided (runner fix accepted into this PR or split) and (b) RV-005 receives an explicit disposition, together with hosted exact-head CI at 1da56057 and the coordinator assessment. No waiver is inferred.
* Boundary: not whole-issue acceptance; no criterion ticked; live callback, browser and API acceptance unproven. Current PR disclaimers stay.

## Current Disposition Addendum (2026-10-26, after the coordinator handoff of 09:41 UTC)

The sections above are the original dated review and are unchanged. This addendum
is a documentary update only. It is not a new source review and is separate from
the coordinator's own source and test acceptance, which this record neither
performs nor verifies. Plan: .copilot-tracking/plans/2026-10-26/issue349-pr-scope-reconciliation-plan.md; critique: .copilot-tracking/reviews/plans/2026-10-26/issue349-pr-scope-reconciliation-plan-critique.md (executed once, Revise, applied); changes: .copilot-tracking/changes/2026-10-26/issue349-pr-scope-reconciliation-changes.md.

| Finding | Current disposition (coordinator decision, recorded now) |
|---------|------------------------------------------------------------|
| RV-001 | Decision gap closed by current coordinator decision: original file ownership superseded only for tools/rpi-checks.py and tools/test_rpi_checks.py, only for the reviewed image_build_argv and --no-cache correction of four scanned images. No workflow, Dockerfile, scanner, ignore, threshold or dependency authority. The amendment is current; no past decision or critique is claimed. |
| RV-002 | Open owner criteria reconciliation; #349 open, Refs only, no ticks; not a blocker for the bounded diagnostic delivery. |
| RV-003, RV-004 | Remain disclosed. Retrospective factual status only: acafc6ee integration had no independent review; coverage is limited to the clean merge evidence, coordinator assessment and the passed gate on 1da56057. Original plan markers are not edited. |
| RV-005 | Coordinator records both breaches (message-only amend of 147980af with identical trees; nohup launch) as nonconformances, not retroactively authorised, not waived or accepted by the owner; no repeat. For the technical partial-delivery gate they are disclosed process residuals. No higher-priority owner instruction requiring retrospective waiver was found; none is inferred. |
| RV-006 | Patch archive bytes preserved. |

Original conclusion retained: a technical partial merge recommendation was not
supportable when first written. Remaining prerequisites after this addendum:
hosted exact-head CI at the final head, and the coordinator assessment; the RV-005
process residuals stay disclosed and unwaived. Receipt e35fecc0 validates only
head 1da56057, becomes historical for the new artifact-only head, and is not
whole-issue acceptance. Source and tests are byte-identical to 1da56057. No live,
browser or tenant acceptance is claimed.
