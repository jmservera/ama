# HVE Artifact Test Report: issue 1294 validation policy guides (run 4, correction C3)

- Tested profile(s): inferred Medium; actual model for every stage not selectable and not observable (host task tool has no model parameter). PROXY run; profile unresolved.
- Run type: full
- Behavior gate: Executed
- Fidelity: simulation
- Execution status: Complete
- Verdict: Pass
- Sandbox: retained at .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-4 (retain-sandbox requested)

## Summary

A fresh full run exercised src/README.md, .github/copilot-instructions.md, the coordinator agent file and the last two docs/reference/log.md entries with 12 scenario IDs (13 prompts): documentation-only with CI absent, complete direct employee-chat evidence including the direct acceptance command with its PYTHONPATH and three-test zero-skip contract, SQL, Bicep/security, focused+focused and focused+full mixes, impact-based workflow/tool/Dockerfile/dependency classification including unresolved impact, shared versus hosted-only versus local-only coverage, direct `--out` versus the runner's 58-byte limit, unpublished and skipped CI with a missing prerequisite, and log truthfulness about the tested revision. The independent grader returned Pass: all 13 prompts Pass, zero confirmed contract defects, and cosmetic or ambiguity observations recorded as nonblocking with no edit. This run tested the final candidate wording: no source edit followed grading.

## Fidelity and limitations

* Per-stage identity: designer = fresh general-purpose subagent (topic checklist only, no scenarios, no prior reports, told not to read .copilot-tracking); executor = hve-core-all:hve-artifact-tester (read-only); grader = fresh general-purpose subagent. Three distinct contexts separate from the lead. Actual models: not observable.
* Proxy, profile unresolved: this evidence does not establish behavior at an intended profile and makes no native claim. A higher-tier simulator may repair ambiguity a lower-tier run would expose.
* Tested revision: HEAD bd63b22c0b5405ae00f7cbe4d511db30446ab556 plus the uncommitted C3 working edits to src/README.md and docs/reference/log.md (patch: .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-4/target-diff-vs-bd63b22.patch). `git diff` of src/README.md sha256 6f33a32a5968d3c807833611a8f899799ef72189a9700f409861913a16f59333 and of docs/reference/log.md sha256 0874887823ad3e8c2e6a95a971eb65724c59fd9d9f6b54067ab17c9bdcbf8763 at grading time. The C3 outcome log entry and tracking records added afterwards are not guide wording and were not simulated.
* The grader did not re-verify the executor's containment; the lead re-checked git status after execution (only expected files).
* The test-log is a lead condensation of the executor return (disclosed in the log).
* Simulation is literal reading of the artifacts; no live agent session, real browser, hosted CI, receipt or runner was exercised.
* Reports 1-3 were not given to any stage and are not reused; run 3's Revise grades are not reused.

## Reuse eligibility

Not applicable (full run).

## Findings

| # | Action | Mapped dimension | Artifact | Profile | Evidence class | Severity | Evidence | Resolving change |
|---|--------|------------------|----------|---------|----------------|----------|----------|------------------|
| N1 | none (nonblocking) | clarity | .github/agents/ama-backlog-delivery-coordinator.agent.md:478 | proxy | simulated | Info | test-review.md (b) | None; consistent with the strictest-tier rule, which README and instructions state fully |
| N2 | none (nonblocking) | clarity | src/README.md:188 | proxy | simulated | Info | test-review.md (b) | None; generic commands are at lines 53-55 |
| N3 | none (nonblocking) | completeness | src/README.md axe location | proxy | simulated | Info | test-review.md (b) | None; not an issue-contract element |

No confirmed contract defects. Other cosmetic observations are listed in test-review.md.

## Coverage

Ran as intended: all 13 prompts. Untested: timing, --resume, receipt schema, branch/PR workflow, retention wording, a real browser run, a workflow-plus-docs mixed case, the coordinator's tier-reassessment rule, hosted CI behavior.

## Containment

Pre-run status: .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-4/pre-run-status.txt. Executor wrote no files and ran no shell command; no network, install, Docker, SQL, Azure or provider access. Post-run `git status --short --ignored` showed only the two expected modified files, the untracked C3 artifacts and tools/__pycache__/.

## Satisfied-and-skipped

None.

## Human review

- [ ] Human reviewer has read this report and accepts or rejects the findings and the proxy-profile limitation.
