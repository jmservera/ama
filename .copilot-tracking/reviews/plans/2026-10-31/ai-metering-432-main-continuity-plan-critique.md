<!-- markdownlint-disable-file -->
# RPI Plan Critique: AI metering current-main continuity

## Metadata

* Task ID: 432-main-continuity; parent: 432-publication.
* Slug: ai-metering-432-main-continuity.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-main-continuity-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-main-continuity-phase-details.md
* Critique execution status: Complete.
* Observed HEAD: 61bc9d4abb758b2b8d633757eac2fb5e65d30c5f.
* Observed local origin/main: e64c6e6c9da407682de59b926944424f94f50671.
* Branch: feat/ai-metering-432.
* Execution boundary: exactly one bounded final-candidate plan critique; only this artifact is written.

## Inputs and Criterion Boundary

* Caller direction authorises the non-rewriting main merge, main rubric side, queued shared locking with wait 1800 and timeout exit 75, pip-only validation, normal git push -u origin HEAD and a main-targeting PR with Refs #432 before closeout. No force push or issue closure is authorised.
* Supplied continuity research: .copilot-tracking/research/2026-10-31/ai-metering-432-main-continuity-research.md, C1-C3/W1.
* Supplied continuity state: .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-main-continuity-state.json.
* Inherited publication contracts: .copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md; .copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md; .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-publication-plan-critique.md. Their prior findings/dispositions are inputs, not reopened findings.
* Historical preparation pointers: .copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-publication-review.md and .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-publication-state.json.
* Completed external publication Review and current state were read at ../../../.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-publication-review.md and ../../../.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-publication-state.json. These caller-linked external reads are necessary to distinguish completed evidence from preparation.
* Parent 432-publication execution Complete / outcome Residual work at HEAD 61bc9d4a and base a75bbdff is preserved. Its RV-003 routes new-main continuity; RV-001/RV-002 remain baseline/operational residuals. Neither its Review nor the original metering Review is repeated.
* The caller accepts only the known main B023 and synthetic chat-panel skip-log roots and their evidenced causal descendants if the baseline fix has not landed. This permits adverse-evidence publication, not passing receipt verification, complete integration acceptance or disregard of independent failures.
* Applicable policy inputs: src/README.md local-gate/publication contracts and this execution context's prohibition on temporary-directory file operations. Required project context was read in the original case study, current addendum framing, knowledge index and owner memory; no legal/customer conclusion is made.
* Assessment boundary: sequencing, archival, inherited ancestry/guard preservation, new-main-only assessment, exact-head evidence ownership and publication exception. Source implementation correctness, completed metering acceptance and the contents of main #600 are not independently re-reviewed.
* Intake has four untracked continuity plan/details/research/state artifacts. The planned pre-gate evidence commit addresses cleanliness; this critique does not move or commit existing work.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1/C2; functional preservation; P01-T01 | Covered | Both main runtime/verifier exact named chat-test guards and topic inherited-FD lifetime/validation are explicitly retained. |
| C3; parent Review preservation; P01-T01 | Partial | Completed external evidence is identified, but exact state destination and byte-preservation proof are not specified, PC-002. |
| W1; ancestry/rubric; P01-T01 | Covered | Authorised merge retains both ancestries and selects main rubric; actual current-main validation remains executor-owned. |
| Zero owned source/test changes | Covered | Source only through merge, zero new child methods/removals, main additions remain upstream-owned; existing runner/static validation is appropriate. |
| P01-T01 dependencies | Covered | Critique dispositions precede merge/archive/focused validation; P02 depends on committed completion. |
| P02-T01 full gate and shared admission | Partial | Wait 1800, exit 75 requeue, jobs 3 and inherited FD 3 are credible; the literal new output location violates the execution restriction, PC-001. |
| P02-T01 baseline exception | Covered | Known roots and causal omissions are expressly adverse evidence; inherited publication PC-002 supplies per-command/group identities, provenance and independent-blocker classification. |
| Final Review/state/PR-body ownership | Covered | Freeze in-tree evidence before gate; final assessment/state/results remain external and in the PR body without another candidate-changing commit. |
| P02-T01 freshness and publication | Partial | Freshness is specified before assessment, but the executable post-assessment freshness/verification transaction and exact push are incomplete, PC-003. |
| One critique / bounded NEW-MAIN Review | Covered | One distinct continuity assessment, not completed source re-review; later identity changes must not upgrade historical evidence. |
| Operational/hosted/human boundaries | Covered | Refs #432, unmet economics/resident/pitch evidence, hosted checks and owner approval remain separate. |

## Verdict

* Verdict: Revise.
* Severity summary: two High, one Medium; zero Critical or Low.
* Rationale: the narrow continuity direction is credible and already authorised. Three direct parent-owned corrections are needed to make archival, execution location and final publication ordering unambiguous and executable. No finding asks for another critique, another parent Review, a new owned test or an unrelated source fix.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The new gate output is planned in a prohibited temporary directory

* Related IDs: P02-T01; non-functional clean-clone/full-gate requirement.
* Evidence: the continuity plan names the new gate-c output under /tmp. The applicable execution instruction forbids file operations in /tmp, /var/tmp and temporary directories. Phase details require a fresh external output but do not resolve that conflict.
* Concern: the literal new output cannot be created in this execution context. The older README and historical receipt locations describe prior evidence; they do not authorise new prohibited writes.
* Impact: the planned gate cannot be executed as written. Substituting an in-candidate output would dirty or alter the assessed inputs; silently changing the shared lock would break the caller's continuous-exclusion contract.
* Smallest useful change: name a fresh, task-owned, non-temporary output/log location outside both candidate checkouts, with an executable relative path from the gate working directory. Ensure any newly created checkout/environment scratch inputs also obey the executing context's storage rules. Retain the original receipts in place without rewriting them. Do not relocate the canonical shared lock or weaken inherited-FD admission; if the gate executor cannot legally use that shared lock or required scratch locations, record the prerequisite as blocked rather than claiming a run.
* Action owner: planning parent / continuity gate executor.
* Exact resolving evidence: revised P02-T01 names the permitted output/log root and compatible execution context, retains flock -w 1800 -E 75 on the existing shared lock and --heavy-lock-fd 3, and preserves timeout-only requeue semantics. Execution records the real command, fresh external directory and actual receipt/status, or an honest unresolved prerequisite blocker. No new forbidden-path operation is used.
* Decision route: direct planner correction. The selected shared-lock and publication direction is already authorised; no divergent user decision is requested.
* Parent-compatible disposition: correct execution location/preconditions only; no gate bypass, source change, shared-lock replacement or fabricated passing receipt.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Historical archival needs exact destinations and byte-preservation evidence for both completed records

* Related IDs: C3; P01-T01; acceptance requirement to commit completed old-base Review before the new candidate.
* Evidence: phase details direct copying completed publication Review bytes into its existing in-tree preparation path. The plan also requires archival of the current external state while preserving original parent files, but does not name that state's archive destination or a source-to-archive identity record. The in-tree publication state still says Implement/active and no Review; the completed external state says Follow-up/completed and names the new-main blocker.
* Concern: preparation state and completed state are substantively different. Without a named archive mapping, an executor can retain the stale preparation state as though completed, overwrite a protected original record, or archive a later-mutated external record without proving which completed bytes were preserved.
* Impact: the fresh candidate would not have demonstrable durable provenance for the completed old-base outcome and routing decision. Merely retaining HEAD/base prose does not prove preservation of the actual Review bytes requested by the caller.
* Smallest useful change: name the exact external Review/state sources, approved in-tree archive destinations and a companion source-to-destination hash/identity record before the candidate commit. Preserve the completed Review bytes verbatim at the caller-authorised preparation replacement path. Give completed state a separately identified historical destination if overwriting a preserved state is not authorised. Label chronology in companion continuity evidence, not by editing the archived Review bytes. Preserve original parent Review/critique/correction records and the external originals.
* Action owner: planning parent / archival implementation owner.
* Exact resolving evidence: revised P01-T01 contains both mappings; committed archival evidence records matching SHA-256 hashes for each stable external source and archived copy, Complete / Residual work, assessed HEAD 61bc9d4a/base a75bbdff and parent 432-publication identity. A preservation comparison proves protected original records unchanged. The archive and companion evidence are committed before gate c and the NEW-MAIN assessment.
* Decision route: direct planner correction. No new user response or re-assessment of the completed source is required.
* Parent-compatible disposition: strengthen provenance only; preserve all original outcomes and ownership, with zero new source/tests.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Final freshness and verification must occur after the sole assessment and immediately before the exact authorised push

* Related IDs: P02-T01; current-base acceptance; external final Review/state/results; publication handoff.
* Evidence: phase details say to refetch and verify immediately before the new-main exact-head assessment and normal push. The plan says refetch before final assessment and immediate push, but does not specify a distinct post-assessment check/verification transaction. Its push wording omits the caller's exact git push -u origin HEAD. Main advancement during the completed parent Review is the demonstrated cause of this child.
* Concern: an independent assessment is an intervening operation during which main, local candidate identity or evidence inputs can change. A pre-assessment verification does not establish immediate pre-push eligibility. The generic changed-base continuity sentence does not provide the executor's concrete stop/routing branch after this child's sole Review.
* Impact: publication could again claim a current-base exact-head assessment using evidence made stale during Review, or require an unplanned repeat of this completed assessment. A passing receipt and an authorised failed/unverified exception need different, explicit final evidence routes.
* Smallest useful change: spell out the final transaction: freeze committed HEAD/base/tool identities and clean checkouts; run fresh gate and the sole NEW-MAIN Review; keep final Review/state/results external; then fetch main again, compare the same identities and cleanliness, and immediately before git push -u origin HEAD verify the passing full receipt against that freshly resolved main. On the exception route, record failed/unverified status, exact known-root/causal matrix and actual baseline-fix/main ancestry check instead of claiming verification success. Any independent failure or changed HEAD/base/tool/evidence/dirty input blocks this assessed publication boundary and routes distinct continuity work, without repeating this or the parent's completed Review. Open or update the main PR with Refs #432 and durable final evidence before closeout.
* Action owner: planning parent / publication executor; independent reviewer owns only the bounded assessment result.
* Exact resolving evidence: revised P02-T01 states both final branches and the identity-change stop. External final Review and completed child state name identical assessed HEAD/base and the correct gate-c receipt/tool identities. A post-Review fetch/cleanliness record and immediate passing verification, or precise failed/unverified exception record, precede the exact normal push. The main PR body names the historical parent assessment separately, the NEW-MAIN assessment/outcome, receipt identity/status, all causal omissions and unresolved approval/issue criteria. No later candidate-changing commit is presented as assessed.
* Decision route: direct planner correction. Main integration, exception publication and normal push/main PR are already authorised.
* Parent-compatible disposition: tighten the new continuity transaction without reopening inherited metering findings or treating hosted/human approvals as satisfied.

## Strengths and Residual Risk

* Both source ancestries and main rubric selection are explicit. Main exact chat-test runtime/verifier parser guards and the topic's inherited-lock feature must coexist; neither may be weakened to suppress baseline failures.
* Existing runner/static checks assess merge composition. Main-added regressions remain upstream-owned; this child adds zero test methods and removes none. No new metering, UI, privacy fixture or presentation implementation is planned.
* The inherited exception contract already requires per-group/per-command status, diagnostic/test identities, baseline provenance, tool/receipt binding and causal dependency links. Apply it to gate c's actual results, not by copying gate b's outcome.
* A new exact named chat-test guard failure is not automatically covered by the synthetic skip-log exception. Only evidence attributing a failure to the expressly accepted unchanged baseline roots and their causal descendants permits publication; unrelated command identity, unexpected skip, cleanup, ownership, scanner/prerequisite or receipt defects still block.
* Exit 75 is queued admission timeout and requeue only, not gate completion. No holder interruption, unlock/reacquire, foreign-artifact cleanup, uv, cloud fallback or paid/private input is authorised.
* If the baseline fix is actually in freshly checked main ancestry, integrate it and rerun at the new committed candidate before the sole assessment. An absent branch/PR name alone is not current-main provenance; the inherited contract already makes that distinction.
* Parent publication Complete / Residual work and original metering adverse evidence remain historical, unchanged outcomes. New-main assessment covers merge/archival/current-base publication composition only.
* Known-failure permission does not make the receipt passing/verified, establish omitted SQL/browser/scanner/image/infra/migration execution, close #432 or satisfy operational economics, resident-history, pitch, hosted checks or human approval.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is needed. All three findings are compatible parent-owned corrections.
* The permitted gate execution location/context must be established before heavy work; an unresolved storage/shared-lock prerequisite is a real execution blocker, not an exception-covered failure.
* No fresh remote fetch, baseline-fix ancestry check, merge result, gate-c receipt, completed continuity Review or PR exists in the inspected inputs. Those are planned executor/reviewer obligations, not missing evidence that prevents this plan critique verdict.

## Limitations

* This is a plan credibility assessment, not a source Review, merge validation, full gate, receipt verification or publication approval. No tests, gate, private dataset, credentials, delegation, paid call or Git mutation occurred.
* Completed external parent Review/state were read for identity, preservation and inherited contracts only; their source findings and runtime evidence were not re-reviewed. Historical gate-b logs/receipts were not opened or rerun.
* Main #600 facts and known-root provenance are supplied research/parent evidence. Only local HEAD/base/branch/status identities were directly inspected; no fresh hosted lifecycle conclusion is claimed.
* Every plan/details/research/state and parent/source artifact remains unchanged by this critique. Only the caller-specified output is added.

## Recommended Next Action

* Highest-impact finding: PC-003, final current-base publication transaction.
* Action owner: planning parent / publication executor.
* Smallest next action: directly dispose PC-001 through PC-003 in the continuity plan/details before P01; specify the permitted gate location, archive identity mapping and post-assessment pre-push branches together.
* User response required: no.
* Execution is Complete; verdict is Revise. This is the full compatible finding set for the supplied boundary. Finalize after direct dispositions without another critique or parent Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/ai-metering-432-main-continuity-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-main-continuity-plan.md) | Assessed continuity plan, unchanged. |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-main-continuity-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-main-continuity-phase-details.md) | Assessed phase details, unchanged. |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-main-continuity-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-main-continuity-research.md) | Supplied C1-C3/W1 evidence. |
| [.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-main-continuity-state.json](.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-main-continuity-state.json) | Parent-owned continuity Plan state. |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-main-continuity-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-main-continuity-plan-critique.md) | This sole Complete / Revise critique. |
| [.copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-publication-plan.md) | Inherited publication sequence/dispositions. |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md) | Inherited exact-head and causal-exception contracts. |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-publication-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-publication-plan-critique.md) | Preserved parent critique, not repeated. |
| [.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-publication-review.md](.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-publication-review.md) | In-tree historical preparation/archive target. |
| [.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-publication-state.json](.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-publication-state.json) | In-tree historical preparation state. |
| [../../../.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-publication-review.md](../../../.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-publication-review.md) | Completed old-base parent Review, preserved. |
| [../../../.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-publication-state.json](../../../.copilot/session-state/78bc570d-9a9a-4914-a18c-763026950ae0/files/ai432-publication/.copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-publication-state.json) | Completed parent state and continuity routing. |
| [src/README.md](src/README.md) | Local-gate and publication policy. |

## Next Steps

No user action is required. Return Complete / Revise to the active planning parent for direct PC-001 through PC-003 dispositions and finalization. Continue only the authorised continuity merge/archive/gate/NEW-MAIN-assessment/publication sequence after those corrections and execution prerequisites are resolved. Do not repeat this critique or either completed parent Review. This reviewer stops after the one bounded critique.
