# HVE Artifact Test Report: issue 1294 validation policy guides (run 3, correction C2)

- Tested profile(s): inferred Medium; actual model for every stage not selectable and not observable (host task tool has no model parameter). PROXY run; profile unresolved.
- Run type: full
- Behavior gate: Executed
- Fidelity: simulation
- Execution status: Complete
- Verdict: Revise
- Sandbox: retained at .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3 (retain-sandbox requested)

## Summary

A fresh full run exercised src/README.md, .github/copilot-instructions.md and the coordinator agent file with 12 scenarios (S01-S12): documentation-only with CI absent, direct employee-chat evidence, SQL, Bicep/security, both mixed cases, impact-based workflow/Dockerfile classification including unresolved impact, shared versus hosted-only coverage, direct `--out` versus the runner limit, skipped CI with a missing prerequisite, and unpublished CI. The independent grader returned Revise: 9 scenarios Pass, 3 Revise, four wording findings (F1 Low, F2 Medium, F3 Low, F4 Low). The F2 and F3 defects were in the examples table and F1 in the direct-check text; the mixed-tier rule (F2 of the earlier review), the 58-byte attribution and the direct browser contract were recovered correctly by the simulation.

## Fidelity and limitations

* Per-stage identity: designer = fresh general-purpose subagent; executor = hve-core-all:hve-artifact-tester (read-only); grader = fresh general-purpose subagent. Three distinct contexts separate from the lead. Actual models: not observable.
* Proxy, profile unresolved: this evidence does not establish behavior at an intended profile and makes no native claim. A higher-tier simulator may repair ambiguity a lower-tier run would expose.
* The designer received a required-topics checklist, not scenarios or expected answers, and no prior reports; it did not read the tool or workflow files. Reports 1 and 2 were not given to any stage and are not reused.
* Post-grade edits: the four findings were corrected once in one batch (src/README.md; patch .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3/post-grade-final-diff-readme.patch). These edits were NOT re-simulated and no self-reuse is claimed. The verdict stays Revise; the corrected wording is flagged for the independent exact-head reviewer and the owner.
* Hosted CI, a real runner and Chromium TMPDIR behavior were not exercised.

## Reuse eligibility

Not applicable (full run).

## Findings

| # | Action | Mapped dimension | Artifact | Profile | Evidence class | Severity | Evidence | Resolving change |
|---|--------|------------------|----------|---------|----------------|----------|----------|------------------|
| F2 | correction | clarity | src/README.md examples table | proxy | simulated | Medium | S05 trace; test-review.md | Reworded to "That a full receipt is required, or that hosted CI covers the harness" (post-grade, unsimulated) |
| F1 | correction | clarity | src/README.md direct-check list | proxy | simulated | Low | S10 trace | Unset and set cases stated separately (post-grade, unsimulated) |
| F3 | correction | accuracy | src/README.md examples table | proxy | simulated | Low | S02 trace; src-ci.yml:102-119 | Named the acceptance check and three browser checks (post-grade, unsimulated) |
| F4 | adjustment | clarity | src/README.md examples table | proxy | simulated | Low | S01 trace | Named the hve-builder static, behavior and host gates (post-grade, unsimulated) |

## Coverage

Ran as intended: S01, S03, S04, S06-S09, S11, S12 and, apart from the findings, S02, S05, S10. Untested or only touched: a chat change plus an unresolved workflow edit mixed case; `--verify-receipt` currency; the coordinator agent's mixed-tier sentence not directly targeted; hosted CI behavior.

## Containment

Pre-run status: .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-3/pre-run-status.txt. Executor wrote no files; no network, install, Docker, SQL, Azure or provider access. Post-run status recorded in the changes record.

## Satisfied-and-skipped

None.

## Human review

- [ ] Human reviewer has read this report and accepts or rejects the findings and the unsimulated post-grade edits.
