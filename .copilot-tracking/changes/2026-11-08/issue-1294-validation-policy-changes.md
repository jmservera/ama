<!-- markdownlint-disable-file -->
# RPI Changes: issue-1294-validation-policy

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-plan.md

## Status

Implementation complete. P01 and P02 done. Tier: focused (instruction and guide wording only). HVE classification: Major.

Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-phase-details.md
Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md
Critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-plan-critique.md

## Baseline (P01-T01)

* .github/copilot-instructions.md:72-90 required a local gate for every candidate, including documentation-only, and named `--changed` the default focused tier.
* src/README.md:61-67 and the coordinator file (449-471) already described a focused tier of planned tests; tracking-retention-policy.md:14 said "complete local publication gate" generically.

## Changes

* .github/copilot-instructions.md: two-tier policy (targeted/focused with optional `--changed`; full gate with verified external receipt for major, SQL, infrastructure, deployment, security-sensitive, release, workflow, gate-tool, dependency-manifest and Dockerfile changes); mixed takes strictest; doubt takes full; partial receipt never full; absent, path-filtered, skipped or unobserved CI is not a pass; link to new guide section.
* src/README.md: reworded Local RPI gate lead; `--changed` is an optional aid; new section "Hosted CI versus local gate coverage (issue #1294)" with triggers, selection, local-only checks, shared and hosted-only checks, CI truthfulness, direct employee-chat commands and a policy examples table.
* .github/agents/ama-backlog-delivery-coordinator.agent.md: focused tier bullet and classify-by-category paragraph.
* docs/reference/method/tracking-retention-policy.md: "selected-tier local publication gate".
* docs/reference/log.md: appended 2026-11-08 entry.
* .copilot-tracking/github-issues/issue-1294.md: issue record (created 2026-11-08T21:33:27Z; no template, labels, assignees, milestone).
* Committed unchanged (SHA-256 7305e77590ee0c7d4cc1920cb91de4bcf97d9099fdf913b24932d3bfecfbf12d): first-attempt research file .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-research.md. Its log /tmp/rpi-1294-validation-policy-1108.log (SHA-256 7f074748d5b4f333720ca312f987065b810f4590cd375f5cc8bd8efb5125c0e9) stays outside the worktree; ignored tools/__pycache__ untouched.

## Not changed

* No workflow, gate tool, application, security control or branch-protection change. Follow-ups: host the employee-chat harness in CI; add zero-skip verification to the hosted chat selector; measure full-gate timing (#470 stays open).

## Validation

* `git diff --check` exit 0; relative-link scan no broken links; no non-ASCII added; no stale default-`--changed` wording.
* Read-only selection reproduction (`changed_groups`, `ci-affected.select`) matched the examples table.
* HVE behavior (contained simulation, proxy profile) Pass; static and host: .copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-1.md.
* Hosted CI not observed (nothing pushed). Full gate and receipt not applicable to the focused tier.

## Divergences

* Commit 8a5cab9 fixed the revision for behavior testing before this record and the review; evidence files and the first-attempt research file follow in a second commit.
* Scenarios were authored by the lead, not a design subagent; executor profile was a proxy.
