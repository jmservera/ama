<!-- markdownlint-disable-file -->
---
title: Resident AI fallback diagnosis phase details
description: Bounded evidence packaging, validation and local persistence, Refs #563
ms.date: 2026-10-30
---

# RPI Phase Details: Resident AI diagnosis

## Metadata

* Task ID: 563
* Task slug: resident-ai-diagnosis-563
* Related plan: .copilot-tracking/plans/2026-10-30/resident-ai-diagnosis-563-plan.md
* Research: .copilot-tracking/research/2026-10-30/resident-ai-diagnosis-563-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|---|---|---|---|
| P01 | Preserve diagnosis and validate | Complete; all four commands passed after dependency restoration | P01-T01,P01-T02 |
| P02 | Review and local persistence | Complete, original candidate locally committed and verified | P02-T01,P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Preserve bounded diagnosis and validate locally

* Context: correct enabled settings are retained in a stopped revision; historical telemetry is inaccessible and source collapses all failure stages.
* Intent: record the strongest supported result, not a fabricated SQL/model/config diagnosis.
* Boundaries: tracking-only writes; zero source/test additions/removals; no Azure changes or live requests.
* Likely targets: task changes record and existing API commands.
* Dependencies: Research C2-C8/W1-W7 and one critique.
* Completion evidence: safe coordinator handoff, actual validation outcomes, B1 preserved.
* Unresolved: exact enabled failure and model dispatch/spend.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Write diagnosis and coordinator handoff

* Context: C3 separates disabled from unavailable labels; W1 proves the actual enabled settings.
* Intent: answer what is known and identify the exact next evidence acquisition.
* Included: verified settings, hypothesis matrix, safe aggregate/classified KQL for revision recover-ai-180649 and interval 18:07:45Z-18:08:20Z.
* Excluded: re-enabling, arbitrary timeout/role/endpoint fixes and source changes without proof.
* Target: .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md.
* Validation: no unsupported root-cause claim; no raw logs/tokens/case content; C/W references resolve.
* Completion: report records current disabled reason and blocked exact enabled cause separately.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute requested local validation

* Context: caller explicitly requires full API discovery and all existing local lint/type commands, even for this evidence-only candidate.
* Intent: preserve measured local outcomes, with existing opt-in skips distinguished from execution.
* Included: exact source/test PYTHONPATH and four commands from src/api, serialized by `flock -w 600 /tmp/ama-rpi-heavy.lock`.
* Excluded: uv, private/cloud SQL, inference, site browser runs, bypasses, foreign lock interruption.
* Targets: external session validation log and changes summary; zero test/source edits.
* Dependencies: existing installed tooling; restore only on an actual missing dependency.
* Validation: all command exits captured even if an earlier command fails. A 600-second admission failure is Blocked, not tests passing.
* Completion: command results and actual skips/failures recorded; no full-publication gate claim.
* Actual evidence: initial system-runtime setup failed (1343 tests, two missing-dependency/metadata errors, 318 skips; tools absent). After external pinned pip restoration,1370 tests/480.249s passed with318 skips, Ruff lint/format and mypy passed. Both attempts used the shared lock. Original and rerun logs remain external and hashed in changes.

<!-- rpi:phase id=P02 -->
## P02: Independent Review and local persistence

* Context: root cause remains unresolved; evidence may be internally accurate without satisfying the caller's full diagnostic objective.
* Intent: one independent assessment, followed by locally persistent artifacts.
* Boundaries: reviewer reads supplied artifacts/source/diff only; no Azure queries, credentials or runtime changes.
* Dependencies: P01 completion and reconciled markers.
* Completion evidence: original Review retained and local commit inspected.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run one independent Review

* Intent: assess whether conclusions match evidence and scope/prohibitions were respected.
* Targets: original review artifact under .copilot-tracking/reviews/logs/2026-10-30/.
* Requirements: distinguish Review execution from outcome; B1 means not an accepted causal diagnosis.
* Dependencies: P01-T01/P01-T02, current changes evidence.
* Completion: exactly one Review with findings routed to later coordinator work; no fix/re-review loop.
* Human/live approval: not performed and not inferred.
* Actual evidence: one independent Review Complete / Not accepted as causal diagnosis; RV-001 High causal gap routed to later research, RV-002 Low scheduled closeout to parent. Original RV-003 Medium lock-path claim retained but not adopted by parent: caller expressly prescribed the exact shared lock, and no conflicting restriction is evidenced in this execution context. No second Review or runtime fix.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit artifacts locally and verify boundaries

* Intent: preserve all seven dated task artifacts and the original review.
* Included: freshly resolve `gh api user` id/login; use `{id}+{login}@users.noreply.github.com` for local author and committer, required Copilot trailer, Refs #563.
* Excluded: push, PR/issue edits, closing keywords, commit amend, source changes or original evidence rewrites.
* Targets: only this task's research/plan/details/critique/changes/review/state paths.
* Validation: `git diff --check`, exact staged paths, commit message/identity, clean final status.
* Publication: no push authorized, so no publication gate/receipt claimed. A later coordinator publication needs a fresh complete exact-head gate.
* Completion: local commit hash exists and seven-path boundary is verified; root-cause blocker retained.
* Actual evidence: candidate d3fa9b9e2f10dfd0b8890c4756a1a7b2543f6c7c committed all seven task artifacts with freshly resolved privacy-safe author/committer identity and requested trailer. Post-commit status clean; src/infra/docs unchanged against requested base. This evidence-only closeout preserves original Review and records completion; no push, second Review or publication gate.
