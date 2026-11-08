---
title: Infrastructure integration topic 136 plan
description: Plan for the planning-only kickoff of the issue 136 Bicep and platform parent integration topic
ms.date: 2026-11-08
---

## Scope and tier

Task `infrastructure-integration-136`. Worktree `/home/azureuser/source/ama-wt/issue-136-integration`, branch `feat/infrastructure-integration-136`, declared PR target `main`, start HEAD `0f05e9aae70768def8d1d9c300215f9ee2f11638`. Local frozen handoff only: no push, PR, merge, issue write, tick or closing keyword. Commits use `Refs #136` only.

Tier FOCUSED. Rationale: Markdown and JSON tracking records only. No source, Bicep, config, workflow, requirement, ADR, README, new epic, feature issue or scope change. Owner direction of 2026-11-08 08:15 is CI-first: no blanket local full gate, no tests, build, install, Python, SQL, Docker, browser, lock, probe, scan or queued work. Validation is Markdown and link review plus the Git diff, then independent exact-head assessment and fresh selected CI by the coordinator before publication.

Research source: `.copilot-tracking/research/2026-11-08-infrastructure-integration-136-research.md` (disposition executed, Planning Readiness Ready).

## Phase 1. Currency and pins (read-only)

* [ ] 1.1 Immediately before the topic record and again before freezing, `git fetch origin main`; if `origin/main` differs from `0f05e9aae70768def8d1d9c300215f9ee2f11638`, record the new SHA as a currency finding and stop for proper re-planning; no merge, rebase or silent update.
* [ ] 1.2 Re-read the live state of 136, its 12 sub-issues, 144, 107, 118, 440 and PR 1141 with `gh` before writing the topic record and again before freezing; record any change from the research table and revise the affected claims.

## Phase 2. Topic record (implementation of the scoped planning record, after the planning commit)

Create one record `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-topic-record.md` containing, with plain-text workspace-relative paths and no Markdown links:

* [ ] 2.1 Provenance: base SHA and tree, `origin/main` currency, ADR 0001, 0002, 0003 and 0006 blobs with status and ms.date, `infra/README.md` and `infra/main.bicep` blobs, case study and reference-index blobs, and the status of each source (Proposed, accepted, owner-amended). Draft, in-review and Proposed documents are recorded as not approved.
* [ ] 2.2 Integration boundaries: what the topic is (a planning anchor on the parent) and is not (no children integrated, no unmerged sibling branches, no 136 criterion met, no 144 acceptance). Name each excluded sibling by number and state.
* [ ] 2.3 Hierarchy and dependency map: 136 with its 12 sub-issues and open or closed state, related parents 113, 195, 201 and 440, 144 depends on 107 and 118 (body text, no API edge), 138 depends on 137 and 118, with the unproven source prerequisites listed.
* [ ] 2.4 Module coverage and honest status: one row per Bicep module and top-level unit with the status classes delivered code (static), observed local, authorized Azure observed, planned and unknown, plus delivered, missing and intentionally manual rows with owner, approver and unknown. Use current files, not the outdated 136 status paragraph. Carry the README register as a documentation record, not machine-checked.
* [ ] 2.5 Contradictions C1 to C8 from research, each as a review item with the affected issue or document and the human who resolves it.
* [ ] 2.6 Per-criterion status of the five 136 acceptance criteria, all unmet, with the exact missing evidence; no tick.
* [ ] 2.7 144 stacking rule. This topic performs none of the steps below and authorizes none. Ordered future gates, each owned by the coordinator or the owner: (a) independent exact-head assessment of this topic head; (b) fresh selected CI on that head; (c) coordinator exposure as a draft parent PR to `main`; (d) a separate decision and new RPI task for 144 that pins the reviewed parent commit SHA as its base. In that task, 107 and 118 source prerequisites are verified in the proposed 144 base first; if any prerequisite is missing, stop and record the blocker, do not rebase or recreate. PR 1141 stays on `main` at `1a9616d4` unchanged and unpushed until separately authorized. 144 stays paused for this parent topic and the demo priority. Candidate lineage is recorded as observed in research C5; `0bd489d3` stays unverified. The topic never claims 144 is unblocked, accepted or integrated.
* [ ] 2.8 Human decision register: Policy and Defender activation and cost (Juan Manuel Servera, pending), manual resources and their owners, real deployment, tenant, subscription and OIDC items; each remains named human and is not decided by an agent.
* [ ] 2.9 Gates and resume points: independent exact-head assessment, fresh selected CI, 440 scoped checkpoint, 107 and 118 verification, 144 live acceptance and from-empty reproduction.

## Phase 3. Validation (documentation only)

* [ ] 3.1 `git diff --check`; ASCII scan of added lines; relative references and frontmatter present; ignored-inclusive status shows only intended paths. Repeat the scope check after the last write (Changes, Review, state, ticks) in Phase 4: `git diff --name-status 0f05e9aae70768def8d1d9c300215f9ee2f11638..HEAD` and the working tree must list only added files under `.copilot-tracking/research/`, `plans/`, `details/`, `changes/`, `reviews/` and `rpi-sessions/2026-11-08/` that carry the `infrastructure-integration-136` name, with no modified or deleted tracked file.
* [ ] 3.2 Scan added lines and commit messages for closing keywords (including negated forms), checkbox ticks and approval wording applied to 136, 144, 107, 118, 440 or any ADR; only `Refs` is allowed.
* [ ] 3.3 No script, test or gate is run. Record "not run, by owner CI-first direction" in the Changes record.

## Phase 4. Changes, Review and handoff

* [ ] 4.1 Write the Changes record from actual diffs.
* [ ] 4.2 One author Review (`rpi-review`) in a later completed step; record execution separately from outcome; it is not independent assessment.
* [ ] 4.3 One state JSON write under `.copilot-tracking/rpi-sessions/2026-11-08/` and plan ticks after Review; one final commit.
* [ ] 4.4 Freeze: ignored-inclusive status clean, return exact HEAD, tree, fresh `origin/main`, phase outputs, boundaries, gaps and review result.

## Commit sequence

1. Planning commit: research, plan, details and critique, before the topic record exists. Author and committer use `8036360+jmservera@users.noreply.github.com` (repository-local), Conventional message, Copilot trailer, `Refs #136`.
2. Topic record commit.
3. Final commit: Changes, Review, state and plan ticks. No amend; explicit staging paths.

## Critique Disposition

One independent critique executed (verdict Revise, 2 High, 3 Medium, 0 Critical), recorded in `.copilot-tracking/plans/2026-11-08-infrastructure-integration-136-critique.md`. All findings are compatible with confirmed owner direction and applied directly: stacking rule made ordered and non-authorizing (2.7), final base-to-HEAD scope check (3.1), publication gates ordered consistently (Follow-Up Items), 144 candidate lineage recorded (research C5), and sub-issue and 440 currency refresh (1.2). No user decision is needed and no critique is repeated.

## Follow-Up Items

* Coordinator, in order and not authorized here: independent exact-head assessment, fresh selected CI, then exposure as a draft parent PR to `main`.
* Owner: confirm manual-row ownership, Defender cost approval, 118 Policy and Defender criterion, 136 body refresh, 144 body identity.
* 144 child task: verify 107 and 118 source prerequisites in its base before engineering.
* Not proposed: any new issue, epic or scope.
