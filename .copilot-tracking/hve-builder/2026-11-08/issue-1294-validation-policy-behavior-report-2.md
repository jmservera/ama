# HVE Artifact Test Report: issue 1294 validation policy (run 2, correction C1)

- Tested profile(s): Medium intended (first canonical model GPT-5.6 Terra). Executed profile UNRESOLVED: the host task tool disallowed a model override, so executor, designer and grader ran on the host default. This is a proxy run; it establishes nothing about behavior at the intended profile.
- Run type: full
- Behavior gate: Executed
- Fidelity: simulation (read-only literal conformance)
- Execution status: Complete
- Verdict: Revise (independent grader, proxy profile). One Medium correction was found and applied after grading; the applied wording was not re-simulated.
- Sandbox: retained at .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-2 (retain-sandbox requested; nothing deleted)

## Summary

Targets: the three C1-corrected files (.github/copilot-instructions.md, src/README.md, .github/agents/ama-backlog-delivery-coordinator.agent.md), as an uncommitted working tree over HEAD 397ce435ae4dddfcf9279179656049b8b670b720. A fresh generic design subagent, given no lead-drafted scenarios, designed twelve black-box scenarios (S01-S12) covering documentation-only, small employee chat, zero-pass, wrong-order and boolean passes, skipped and two-test selector output, SQL, Bicep or security, mixed, comment-only versus permission-changing workflow and gate-tool edits, false green CI, partial and blanket --changed receipts, and the hosted-only label question. The hve-artifact-tester executor traced all twelve with instruction quotations; a separate fresh grader, which was given the examples table and the full employee-chat contract and verified quotes against the targets, the runner, the harness and the workflow, graded S01-S11 as matching and S12 as partly matching, and returned Revise with one Medium correction, two Low corrections or improvements and one cosmetic note.

## Fidelity and limitations

* Observed: file reads by executor and grader. Simulated: the reasoning conclusions. Emulated: every command the executor named; none ran.
* Proxy: executed model unknown to the executor. Intended Medium profile not established. A higher-tier simulator may repair ambiguity a lower-tier run would expose, so this does not show the wording reads unambiguously at lower tiers.
* Designer and grader independence is real (fresh subagents, no lead scenarios, no prior review reads) but they shared the host default model with the executor.
* Not verified by the grader: the `--changed` group selections in the examples table (the lead separately reproduced them read-only, see the correction changes record), what-if enablement, local SPDX document verification, and the 58-byte path mechanics.
* Claims this run cannot support: native tool use, real command execution, hosted CI results, intended-profile behavior.
* Rerun condition for an intended-profile claim: re-execute with an explicit Medium model (GPT-5.6 Terra) when the host permits a model selection for subagents.
* Earlier report 1 and its log are preserved unchanged. Its sandbox was deleted; that loss is adverse evidence and is not reconstructed here.

## Reuse eligibility

Not applicable (full run).

## Findings

| # | Action | Mapped dimension | Artifact | Profile | Evidence class | Severity | Evidence | Resolving change |
|---|--------|------------------|----------|---------|----------------|----------|----------|------------------|
| 1 | correction | accuracy of coverage labels (R2) | src/README.md Shared bullet | proxy | simulated, verified against workflow | Medium | The tracked working-data guard was placed in hosted `src-namespace` and local `namespace`/`migration`; the workflow shows it only in the `src-no-working-data` job (src-ci.yml lines 281-290) and the runner maps it to `static`. The executor repeated it in S12. | Applied after grading: guard is hosted `src-no-working-data`, local `static`; Bicep and migration are hosted `src-namespace`, local `namespace`, `infra`, `migration`. Not re-simulated. |
| 2 | correction | internal consistency (R1) | src/README.md Local-only bullet | proxy | simulated | Low | Said the harness was "run only by the runner" while the section instructs a direct run. | Applied: "run by the runner and directly". Not re-simulated. |
| 3 | improvement | completeness of the contract (R1) | src/README.md direct-check list | proxy | simulated | Low | Omitted that the `skipped` match is case-insensitive and that the 58-byte `--out` limit applies to the direct harness command. | Applied: added both. Not re-simulated. |
| 4 | improvement | readability | src/README.md around the classification link | proxy | simulated | Low | One long unwrapped line. | Not changed; cosmetic. |

Executor gaps 1-12: the grader found none to be a contract miss. Gaps 2, 3, 4, 7 and 10 remain open as owner or policy follow-ups: rubric workflow applicability to documentation PRs, whether a disabled what-if is applicable CI, a procedure for approved control changes, and whether the focused tier must run shared checks locally. They are recorded in the correction review as follow-ups and not changed here, because they widen policy beyond the four corrected findings.

## Coverage

S01-S12 all executed and independently graded. Requirements R1-R5 met per the grader except the R2 label defect now corrected. Untested: native behavior, dependency-manifest and Dockerfile edits beyond S09, a non-pinned axe digest, a missing or overlong out path, and an isolated unresolved-doubt case.

## Containment

Executor, designer and grader are read-only dispatches. The lead wrote only the three sandbox files under .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-2 (run-state.md, test-design.md, test-log.md, plus test-review.md). Pre-run status: four modified policy files, four untracked C1 research, plan, details and critique files, and ignored tools/__pycache__. No unexpected writes were reported by any dispatch; the lead's post-run status is recorded in the changes record.

## Satisfied-and-skipped

None.

## Human review

- [ ] Reviewed and validated by a qualified human reviewer
