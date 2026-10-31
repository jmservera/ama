---
title: PR 558 unresolved threads final-candidate plan critique
ms.date: 2026-10-31
---

## Metadata

* Task ID: pr-558-unresolved-threads-2026-10-31.
* Critique date: 2026-10-31.
* Plan: .copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/pr-558-unresolved-threads-phase-details.md.
* Critique execution status: Complete.
* Independent critique count: one; this is the complete supplied-boundary finding set.
* Inspected HEAD: ed888a91f6da20165f84ddf220386f103721635d.
* Inspected branch: tmp/fabric-558-merge, tracking origin/jmservera/fabric-research. aedc6713 is inherited history, not the current exact HEAD.

## Inputs and Criterion Boundary

* Caller requirements: complete ordered research-plan-implement-review; exactly three PR558 fixes; LF-normalized four textual hashes; actual Verify before receipt regeneration; retained finite-guard correction; January authority, SQL migration, assistant routing/UI and hosted execution disclosure without closing keywords; requested unittest; pip, never uv; required commit trailer; authorized normal push followed by replies/resolutions; no merge or force push.
* Candidate locks: no removals, at most one new PowerShell source-hash regression script, unchanged delivered deck and no duplicate Python verifier.
* Supplied evidence: .copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md, C1-C7/W1; supplied plan and details; relevant owning verifier, native helper/test, source guide/receipt, src/README.md, tools/rpi-checks.py and hosted browser selector.
* Repository context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory was context, not evidence.
* Dependencies and acceptance: existing Docker, unavailable host PowerShell, PowerShell 7.4+ verifier, preserved 5.1-compatible helper, complete external exact-head local gate, clean committed inputs, current-main receipt verification, independent Review and exact-head assessment.
* Assessment boundary: credibility of this supplied implementation/publication plan. No implementation, runtime validation, network research, PR mutation, independent implementation Review or complete local gate was performed by this critique.
* Applicable execution constraint: file operations in /tmp and /var/tmp are prohibited. An external output location does not override this constraint.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3, P01-T01: four canonical text hashes | Covered | Owning verifier has four raw source hashes after Test-DeckCandidate; byte-preserving newline replacement and exact binary/media hashes are explicitly scoped. |
| P01-T01/P01-T02: regression and regenerated receipt | Partial | Semantic fixtures are specified, but comparing the changed builder to the old receipt before regeneration produces a stale-binding failure; PC-002. |
| C4-C5: finite guards and existing tests | Covered | Current helper uses IsNaN/IsInfinity in all four guards; existing test exercises 32 assertions. Windows 5.1 execution is explicitly unperformed. |
| P01-T02: actual Verify and unchanged deck | Covered | Verify checks an external copy; receipt follows successful package checks; native/preview history remains qualified. |
| P01-T02: isolated PowerShell prerequisite | Partial | UID/GID, read-only source and execution-network isolation are stated; immutable image selection and runtime evidence are missing; PC-003. |
| C6/W1, P02-T01: PR disclosure | Covered | Details include February 1 exclusive ceiling, activation/expiry/consent, SQL constraint replacement/idempotency, employee/resident routing/UI and hosted browser execution, with ancestry qualification. |
| P02-T01: original Review and commit | Covered | One independent Review, original evidence preservation, authenticated privacy-safe author/committer and required trailer are explicit. |
| C7, P02-T02: complete external exact-head gate | Partial | Mandatory gate is retained, but its hardcoded prohibited lock path makes the proposed command unavailable here; PC-001. |
| P02-T02: push and thread operations | Covered | Normal named-ref push precedes body edit/replies/resolutions; failure blocks publication; final thread re-read is required. |
| Scope locks and tooling | Covered | No removals, one regression script maximum, no Python duplicate verifier, no deck edit, no new authority/SQL/UI edits, pip-only direction and no merge/force push. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the bounded implementation is credible, but the publication path contains a demonstrated execution-policy blocker and the validation order/runtime provenance need correction. Complete assessment is possible from supplied evidence; Revise is distinct from the blocked publication dependency.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Mandatory gate cannot execute under the current file-operation constraint

* Related IDs: C7, P02-T02, exact-head gate acceptance criterion.
* Evidence: tools/rpi-checks.py:2273-2276 hardcodes Path("/tmp/ama-rpi-heavy.lock") and opens it with O_CREAT/O_RDWR. The phase command uses this unchanged runner. Current execution instructions forbid file operations in /tmp; --out and --lock-timeout do not relocate the lock.
* Concern: the plan treats missing tools, foreign-lock contention and failed checks as blockers, but omits this known incompatible mandatory gate. A different external output directory or TMPDIR does not fix the hardcoded lock.
* Impact: executing the proposed gate violates the applicable constraint; omitting it prevents authorized publication. No valid local receipt, push or thread resolution can be claimed from this execution path.
* Smallest useful change: record this as an explicit publication blocker and stop P02-T02 before running the incompatible command. Retain the mandatory complete gate and every original adverse outcome. Do not relocate locks through wrappers, patch the runner, change protections, substitute hosted CI or widen this candidate's source scope.
* Action owner: planning parent.
* Exact resolving evidence: revised plan/details explicitly acknowledge the blocker and prevent publication until a separately authorized compliant gate execution path is available; before actual publication, a full external exact-head receipt and successful verification against current origin/main remain required. No compliant path is established by the supplied inputs.
* Decision route: direct planner correction to record and enforce the blocker. Existing owner direction does not authorize a divergent runner/environment change; such a future proposal requires separate authorization, not a question needed to complete this critique.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Four-input receipt assertions are scheduled against a necessarily stale builder digest

* Related IDs: P01-T01, P01-T02, regenerated four-hash acceptance criterion.
* Evidence: phase details require the new regression to compare the actual four inputs with the current receipt. P01-T02 in the plan runs source-hash tests, then actual Verify, then refreshes the receipt. tools/capstone/Invoke-Capstone.ps1:463 hashes its own source; docs/capstone/source/validation.json currently binds the pre-change builder.
* Concern: adding the canonical hashing helper changes the builder's meaningful bytes. Consequently the new canonical builder digest cannot match the old receipt, even though LF normalization itself is correct. Treating that early mismatch as a successful test or manually refreshing digests before Verify would contradict the task.
* Impact: the documented sequence either fails its required regression or invites an unverified receipt workaround.
* Smallest useful change: separate semantic fixture assertions from receipt-binding assertions within the same single regression script. Run semantic/native checks first, run actual Verify, regenerate the receipt only from its successful report, then run all four receipt-binding assertions against that regenerated receipt. Preserve any observed pre-refresh mismatch as adverse historical evidence.
* Action owner: planning parent.
* Exact resolving evidence: corrected order in plan/details; later execution logs showing semantic checks, successful actual Verify with unchanged delivery SHA-256, report-derived receipt regeneration and four passing post-refresh bindings. No additional verifier or script is needed.
* Decision route: direct planner correction; no significant or divergent user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Container runtime is not yet reproducibly selected or evidenced

* Related IDs: P01-T02, isolated Docker dependency, actual Verify acceptance criterion.
* Evidence: owning verifier requires PowerShell 7.4+. Plan/details propose an isolated local Docker runtime but specify no immutable image identity, image acquisition boundary or recorded runtime version. Existing receipt describes historical PowerShell 7.6.4, not a proven runtime for this candidate.
* Concern: Docker availability alone does not establish an available compatible PowerShell image. A mutable image tag or unrecorded runtime cannot establish which executable performed fresh Verify, and execution-network isolation does not by itself document whether the image was already local.
* Impact: fresh verification may block on an absent image or be presented without adequate provenance; historical native_shape_runtime must not silently stand in for the actual candidate run.
* Smallest useful change: specify a trusted PowerShell image resolved to an immutable digest, a local-image/version preflight and recorded Docker invocation with --pull=never and --network=none during execution. Record any separately permitted acquisition honestly before execution; if no compatible image is available, stop verification and receipt refresh. Keep current UID/GID, read-only repository and only owned external writable output; explicitly direct scratch/HOME/cache paths to allowed owned locations.
* Action owner: planning parent, then implementing agent for execution evidence.
* Exact resolving evidence: plan/details identify immutable runtime selection and preflight; execution record contains image digest/ID, actual $PSVersionTable version, invocation/mount/isolation settings, successful verifier exit and report hash; regenerated receipt labels the actual Linux/container runtime while retaining unperformed Windows 5.1/Office acceptance.
* Decision route: direct planner correction within the already-proposed Docker approach; no significant or divergent user decision.

## Strengths and Residual Risk

* Normalization remains limited to four textual inputs. BOM, significant whitespace, empty input and newline variants are named; template/media/delivery hashes remain exact.
* Verification uses the actual unchanged delivery rather than a newly built substitute. The generated report is the source of regenerated receipt fields.
* The already-delivered finite correction is retained rather than redundantly rewritten. Portable tests are not promoted to Windows 5.1 or Office acceptance.
* Current-main ancestry is acknowledged in PR disclosure. January authority remains bounded by activation, expiry and consent rather than being described as newly granted.
* The complete external local gate, current-base verification, independent assessment and retained hosted controls remain publication conditions, not interchangeable evidence.
* Missing prerequisite handling and a foreign-lock timeout must remain honest failures; they do not authorize interference with another user's processes or locks.

## Questions or Blocking Evidence Gaps

* No user response is required for these direct corrections.
* Publication remains blocked by PC-001 until a separately authorized compliant execution path is established.
* Compatible local PowerShell image availability is an implementation preflight, not an assumed successful check.

## Limitations

* Supplied W1 thread IDs and ancestry claims were assessed as research evidence; remote state and hosted outcomes were not freshly retrieved.
* No container was started, no report/receipt regenerated and no tests executed. Those are implementation evidence obligations, not critique results.
* This assessment does not grant publication permission beyond the owner's existing bounded authorization or establish human, resident, legal, accessibility, Windows or Office acceptance.
* Pre-existing untracked plan/details/research/state artifacts were left untouched. Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: record the hardcoded-lock publication blocker, correct receipt-test sequencing and add runtime provenance requirements directly. Finalize the plan without another critique; implementation may proceed only through eligible steps, while publication remains blocked.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md](.copilot-tracking/plans/2026-10-31/pr-558-unresolved-threads-plan.md) | Supplied final-candidate plan |
| [.copilot-tracking/details/2026-10-31/pr-558-unresolved-threads-phase-details.md](.copilot-tracking/details/2026-10-31/pr-558-unresolved-threads-phase-details.md) | Supplied execution details |
| [.copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md](.copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md) | Supplied C1-C7/W1 evidence |
| [.copilot-tracking/reviews/plans/2026-10-31/pr-558-unresolved-threads-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/pr-558-unresolved-threads-plan-critique.md) | Complete independent critique |

## Next Steps

Planning parent: resolve PC-001 through PC-003 by direct plan/detail corrections and finalize without another critique. No user action is required for the critique disposition. Do not publish, reply with claimed completion or resolve threads until the unchanged mandatory complete local gate and exact-head assessment can actually be satisfied through an authorized compliant path.
