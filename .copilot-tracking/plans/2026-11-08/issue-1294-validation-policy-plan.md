<!-- markdownlint-disable-file -->
# RPI Plan: issue-1294-validation-policy

## Task Metadata

| Field         | Value                                                                                       |
|---------------|---------------------------------------------------------------------------------------------|
| Task ID       | issue-1294                                                                                  |
| Task slug     | issue-1294-validation-policy                                                                |
| Date          | 2026-11-08                                                                                  |
| Branch / base | docs/validation-policy-1294 on origin/main fa7ae0c9770e890f82482456bfcb8e97f1e05429         |
| Research      | .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md         |
| Details       | .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-phase-details.md           |
| Changes       | .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-changes.md                 |
| Local tier    | Focused (instruction and guide only). HVE classification Major (separate axis).             |

## Executive Summary

The plan reconciles the local-validation wording in four files so that small and documentation-only candidates run targeted local checks plus applicable hosted CI, while major features, SQL, infrastructure, deployment, security-sensitive changes and releases keep the full exact-head gate and verified external receipt. No workflow, tool, application or branch-protection change is planned.

### User Decisions and Requirements Highlights

* Owner highest priority: lighter policy that keeps relevant coverage and higher-risk safeguards.
* Mixed scope takes the strictest tier; independent exact-head review and human approvals remain.
* Absent, path-filtered or skipped CI is never a pass.

### What You May Not Know

* The guide and coordinator already described a focused tier; the real contradiction is in the repository instructions (blanket gate, `--changed` default) and one generic sentence in the retention policy.
* Hosted `src-api` runs the chat-panel selector but not the employee-chat axe harness, and has no exact-count zero-skip verification, so those stay local direct checks.
* A `src/**/*.md`-only PR triggers Source CI but selects no project; the jobs report success without running tests.
* The active ruleset currently lists no required status contexts (checked 2026-11-08); "required" hosted CI is therefore "applicable hosted CI that actually ran".

### Unresolved Decisions or Blockers

* None blocking. Deferred follow-ups: host the employee-chat harness in CI and add zero-skip verification to the hosted selector step (workflow changes need owner direction); #470 timing measurement stays open.

## User Decisions and Requirements

* Follow issue #1294 and the coordinator brief verbatim; research evidence in the retry research artifact is authoritative; the first nonconforming attempt is adverse evidence only.
* Change only files whose current wording must change. Do not change workflows, tools, application, security controls or branch protection.
* Add `.copilot-tracking/github-issues/issue-1294.md`.
* Use hve-builder improve mode (Major): baseline, static review, hve-builder-tester contained simulation, host validation.
* Final: clean committed frozen local candidate; no push, PR or merge.

## Goals

* One consistent, truthful tiered validation policy across instructions, guide, coordinator profile and retention policy.
* Named, testable examples for documentation-only, small employee-chat/browser, SQL, Bicep/security and mixed changes.

## Scope and Non-Goals

### In Scope

* `.github/copilot-instructions.md`, `src/README.md`, `.github/agents/ama-backlog-delivery-coordinator.agent.md`, `docs/reference/method/tracking-retention-policy.md`, `docs/reference/log.md`, `.copilot-tracking/github-issues/issue-1294.md` and this issue's RPI artifacts.

### Non-Goals

* Workflows, `tools/*`, application code, branch protection, rubric README step 3 (scoped lifecycle), #470 timing.

## Functional Requirements

* FR1 Instructions define the targeted/focused tier and the full tier, strictest wins, and drop the blanket `--changed` default.
* FR2 Guide holds a hosted-versus-local coverage reconciliation, the local-only list and the examples.
* FR3 Coordinator tiers reference the same rules without contradicting the guide.
* FR4 Retention policy no longer implies the complete gate is universal.

## Non-Functional Requirements

* Plain ASCII, `*` lists, no em dashes, relative links valid, claims cite repository evidence.
* Full tier text keeps: external full receipt, verify before push, fresh clean exact head, independent review, human approvals, no partial receipt for full tier, shared-resource admission.

## Acceptance Criteria

* AC1 No current file says every candidate needs a local gate or that `--changed` is the default.
* AC2 Policy examples exist and the selection facts they state are reproduced by `changed_groups` and `ci-affected.select` (read-only check).
* AC3 `git diff --name-only` contains only in-scope files.
* AC4 HVE static verdict Pass, behavior simulation Pass, host validation Pass, or an honestly recorded deferral.
* AC5 Candidate is committed, clean, with Conventional Commit and Copilot trailer.

## Implementation Context Record

* Standalone native session; parent is this RPI run. Next stage after critique: implement.

## Sources

* .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md (C1 to C23, W1)

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Baseline and edit the policy files

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Record HVE baseline of the four target passages

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Rewrite the instruction gate paragraph (copilot-instructions.md)

<!-- rpi:task id=P01-T03 -->
#### [ ] P01-T03: Add coverage reconciliation and examples to src/README.md

<!-- rpi:task id=P01-T04 -->
#### [ ] P01-T04: Align coordinator tiers and retention policy wording

<!-- rpi:task id=P01-T05 -->
#### [ ] P01-T05: Add issue record and knowledge-base log entry

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and freeze

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Reproduce example selections read-only and run link/diff/stale-wording checks

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: HVE static review, hve-builder-tester simulation, host validation

<!-- rpi:task id=P02-T03 -->
#### [ ] P02-T03: Changes record, original review, commit and freeze

## Dependencies

* P02 depends on P01. Review (separate phase) depends on both.

## Critique Disposition

Critique executed once: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-plan-critique.md. Verdict Revise (0 Critical, 2 High, 5 Medium, 2 Low). All nine findings were planner-applicable; no user decision was needed. No second critique runs.

| Finding | Disposition |
|---------|-------------|
| PC-001 | Accepted. Tier by change category, never by diff size or `--changed` selection: full for major features, SQL, infrastructure (Bicep, `infra/`), deployment, security-sensitive changes, releases, and any workflow, `tools/rpi-checks.py`, dependency manifest or Dockerfile change; any doubt takes the full tier. Added to P01-T02 and P01-T03. |
| PC-002 | Accepted. Direct commands documented from src/api/README.md (unit modules, `employee_acceptance_check`, chat-panel selector with `ZF_BROWSER_TESTS=1` requiring exactly one test and zero skips, `employee_chat_browser_check` with the SHA-256-pinned axe). The absence of a single-command wrapper and of hosted zero-skip verification is recorded as a follow-up, not a tool change. |
| PC-003 | Accepted. Text states `--changed` (and any partial receipt) never satisfies the full tier. |
| PC-004 | Accepted. P02-T01 uses concrete path lists and records expected `changed_groups` and `ci-affected.select` output, plus grep reproduction of hosted claims. |
| PC-005 | Accepted. The sentence that hosted CI remains required is kept; added that absent, path-filtered, skipped or unobserved CI is not evidence and that CI is unobserved for an unpushed candidate. |
| PC-006 | Accepted. The first-attempt research file is committed byte-identical (SHA-256 7305e775...bf12d) as adverse evidence so the candidate is clean; its /tmp log stays outside. |
| PC-007 | Accepted. Pass criteria: all five scenarios return the expected tier and refuse the forbidden claim; a Deferred simulation maps to AC4 Deferred. Critique disposition is recorded here; original review is written before the commit. |
| PC-008 | Accepted. P02-T01 greps `rpi-checks.py --changed`, "every final RPI candidate", "complete local" across `.github`, `src`, `docs/reference/method`, `docs/reference/README.md`; hits that are intentionally unchanged (rubric README step 3, historical logs) are recorded. |
| PC-009 | Accepted. Policy wording does not depend on the ruleset observation; it is dated evidence only and rechecked in P02-T03. |

## Follow-Up Items

* Host the employee-chat axe harness in CI; add zero-skip verification to the hosted chat-panel step (owner direction needed).
* Measure full-gate timing (#470).

## Handoff

Run implementation with the changes record at .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-changes.md.
