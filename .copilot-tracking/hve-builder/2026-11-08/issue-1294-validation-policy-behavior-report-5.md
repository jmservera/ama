# HVE Artifact Test Report: issue 1294 validation policy guides (run 5, correction C4)

- Tested profile(s): inferred Medium; actual model for every stage not selectable and not observable (host task tool has no model parameter). PROXY run; profile unresolved.
- Run type: full
- Behavior gate: Executed
- Fidelity: simulation
- Execution status: Complete
- Verdict: Pass
- Sandbox: retained at .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5 (retain-sandbox requested)

## Summary

A fresh full run exercised src/README.md, .github/copilot-instructions.md, the coordinator agent file and the appended docs/reference/log.md entries with 16 scenarios (design VTIER-BB-001): focused+focused and focused+full mixes, documentation-only with CI absent, impact-based workflow/tool/Dockerfile/dependency classification including unresolved doubt, complete direct employee-chat evidence, the acceptance command with its PYTHONPATH and three-test zero-skip contract, hosted selection for a README-only change versus widened paths with the unconditional data guard, the real SQL path, partial-receipt BASE RELAXED versus full exact-base, the self-contained focused command with failed-run-only resume, the shared/hosted-only/local-only comparison, the 58-byte limit, refusal of a CI-passed claim and a partial-receipt downgrade, and log truthfulness. The independent grader returned Pass: 16 of 16 scenarios Pass, zero confirmed contract defects; eight executor-reported gaps and three Low observations are nonblocking and no edit was made.

## Fidelity and limitations

* Per-stage identity: designer = fresh general-purpose subagent (topic checklist only, told not to read .copilot-tracking or the targets); executor = hve-core-all:hve-artifact-tester (read-only); grader = fresh general-purpose subagent. Actual models not observable. Static review before this run was a separate proxy independent assessment (.copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-static-review-c4-log.md), which is not a behavior result.
* Proxy, profile unresolved: this evidence does not establish behavior at an intended profile and makes no native claim.
* Tested revision: HEAD 2f1aa2e4d42b79364b95622d6198975203c1417e plus the uncommitted C4 working-tree edits (patch .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5/target-diff-vs-2f1aa2e.patch, sha256 d635bb3f3c82f2168510e11c63c342959160fbefd0aa7b90755bf1aa8294de1c). Identities before dispatch and after grading are identical (source-identities-pre-dispatch.txt, source-identities-post-grade.txt): src/README.md blob b6f456731b56fe11fa58c291b62eed2a105e6662, .github/copilot-instructions.md blob dd8c0b20f44b1c98db9aad327302f64da008c5e8, coordinator agent blob 3a46e98a42e477ce2d9928dd495f53a4e1cde570, docs/reference/log.md blob c930d1bdf725dd75ff0e81924cb8ec7eef67ca6b. The C4 log entries were already present when tested. The C4 tracking records (changes record, review) and this report are created after grading and were not simulated.
* The grader did not re-verify the executor's containment, which is self-reported; the lead re-checked git status. The test-log is a lead summary around the raw executor return retained verbatim (test-log-executor-trace.md, sha256 91ce2ac07d712d09ee04c576c0ed5eb31f291ee499d21a7ae7c4d5d68ca776b1).
* Simulation is literal reading; no live agent session, real browser, hosted CI, receipt, resume or runner was exercised. Reports 1-4 were not given to any stage and no earlier grade is reused.

## Reuse eligibility

Not applicable (full run; report 4 targeted an earlier source boundary and the guide hunks changed).

## Findings

| # | Action | Mapped dimension | Artifact | Profile | Evidence class | Severity | Evidence | Resolving change |
|---|--------|------------------|----------|---------|----------------|----------|----------|------------------|
| N1 | none (nonblocking) | completeness | src/README.md SQL row | proxy | simulated | Low | test-review.md | None; importer paths do not select mssql and the row does not promise it |
| N2 | none (nonblocking) | clarity | src/README.md resume example | proxy | simulated | Low | test-review.md | None; base source is stated as the failed receipt's recorded base |
| N3 | none (nonblocking) | completeness | src/README.md acceptance command | proxy | simulated | Low | test-review.md | None; Chromium prerequisite is in src/api/README.md |

No confirmed contract defects.

## Coverage

Ran as intended: all 16 scenarios. Untested: timing, resume execution, receipt schema, real browser run, hosted CI behavior, native runtime.

## Containment

Pre-run status: .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-5/pre-run-status.txt (captured at the freeze before dispatch, so it is dirty, not clean: it lists the modified src/README.md and docs/reference/log.md, the untracked C4 research, plan, details, critique, changes, static-review log and sandbox, and the ignored tools/__pycache__/; the earlier clean-tree snapshot from the start of C4 was overwritten by this freeze capture). Executor wrote no files and ran no commands; no network, install, Docker, SQL, Azure or provider access.

## Satisfied-and-skipped

None.

## Human review

- [ ] Human reviewer has read this report and accepts or rejects the findings and the proxy-profile limitation.
