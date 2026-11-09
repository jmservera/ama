# HVE Builder behavior, static and host report: issue #1294 validation policy

* Date: 2026-11-08. Classification: Major (policy mutation). Local gate tier: focused (separate axis).
* Targets: .github/copilot-instructions.md, src/README.md (Hosted CI versus local gate coverage section), .github/agents/ama-backlog-delivery-coordinator.agent.md, docs/reference/method/tracking-retention-policy.md (wording only).
* Tested revision: commit 8a5cab9f9cde3cc29d97a7b07faf12a338392ad9 (base fa7ae0c9770e890f82482456bfcb8e97f1e05429).

## Baseline

* Pre-change contradiction: copilot-instructions lines 72-75 required the complete gate or `--changed` for every candidate while the issue required a lighter tier. Recorded in the retry research artifact (C1-C23).

## Static review (lead, hve-builder rubric, self-assessed; independent planning critique PC-001..PC-009 already applied)

* Consistency across the four files: tier names, "strictest tier for mixed", "partial receipt never full", "absent/path-filtered/skipped/unobserved CI is not a pass" agree (confirmed by the independent grader).
* No workflow, tool, application, security-control or branch-protection change; ASCII-only added text; no em dashes; relative links resolve.
* Result: no open static findings. This review was by the lead, not an independent reviewer; the independent element is the behavior grader and the plan critique.

## Behavior test (hve-builder-tester, contained simulation)

* Fidelity: simulation, read-only executor (hve-core-all:hve-artifact-tester). Profile: PROXY. The task tool accepted no profile for the executor and the lead did not pin one, so the executor ran on the session model. The evidence does not establish behavior at an intended profile.
* Deviations: the black-box scenarios (S1-S6) were authored by the lead rather than a separate design subagent, and scenario S1-S6 prompts named files in the executor wrapper. Grader was an independent general-purpose subagent.
* Execution: Complete. Verdict: Pass (independent grader). Plan PC-007 pass criteria met: all five required cases (doc-only, small employee chat, SQL, Bicep/security, mixed) returned the expected tier and refused the forbidden claim; S5 refused an interrupted partial receipt as full; S6 refused to report absent CI as passed.
* Findings: 0 fix. F1 low miss (untested: interrupted/resume path, workflow-change tier, native fidelity). F2 low note (optional pointer to src-ci.yml paths). Executor gaps G1-G11 triaged: G1, G5, G6, G9 out of scope or pre-existing, G2, G8 acceptable, G3, G7, G10 notes, G4 miss folded into F1, G11 limitation.
* Caveat: the grader did not read the policy examples table.
* Sandbox: .copilot-tracking/sandbox/2026-11-08-issue-1294-policy-1 (run-state.md, test-log.md) contained only lead-written files; removed after this report.

## Host validation

* `git diff --check` exit 0. Relative-link scan of the four changed guides: no broken links. Anchor `#hosted-ci-versus-local-gate-coverage-issue-1294` present as heading at src/README.md. Added lines contain no non-ASCII characters. No stale default-`--changed` phrasing remains in .github, src/README.md, docs/reference/method.
* Not run: native fidelity, markdownlint (no repository-wide documentation lint), hosted CI (nothing pushed).

- [ ] Human review of this behavior report (left unchecked)
