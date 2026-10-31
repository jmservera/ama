<!-- markdownlint-disable-file -->
---
title: Resident AI telemetry schema correction phase details
ms.date: 2026-10-31
---

## Metadata

* Task ID: pr-585-telemetry-schema-correction-563-2026-10-31
* Task slug: resident-ai-telemetry-schema-563
* Plan: .copilot-tracking/plans/2026-10-31/resident-ai-telemetry-schema-563-plan.md
* Evidence: research C1-C5 under the same dated slug.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete: dated appendix added | P01-T01 |
| P02 | P02-T01 complete; local persistence pending | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Append schema correction

Context: C1/C4 contradict C3's future schema; C2 is a historical denied attempt.
Intent: one controlling dated appendix, no old-byte replacement.
Boundary: original changes file and new evidence only.
Dependency: one critique. No implementation uncertainty remains.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Append two corrected query variants

Target: .copilot-tracking/changes/2026-10-30/resident-ai-diagnosis-563-changes.md.
Map ContainerAppConsoleLogs_CL to ContainerAppConsoleLogs; ContainerAppName_s,
RevisionName_s and Log_s to their unsuffixed names. Preserve every other query
character/semantic. Include historical aggregate as an unexecuted equivalent.
Supersede future handoff and downstream references explicitly. Keep authorized
private-route, fixed-marker, no-raw-content and stage-attribution caveats.

Completion: appended note plus both exact query transformations; no other PR
artifact/doc carries a duplicate. Live execution remains unperformed.

<!-- rpi:phase id=P02 -->
## P02: Validate, review and persist

Intent: prove documentary correction and preservation, not runtime diagnosis.
Boundary: local-only checks and commit; no publication gate or Azure operations.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validate documentary invariants and perform one Review

Dependency: P01-T01. Compare original content from bbbd969b to working prefix;
compare six other original paths byte-for-byte. Extract four Kusto blocks and
assert corrected pair equals original pair after schema-only substitution.
Check fixed app/revision/windows, explicit unexecuted wording, unchanged
privacy/approval limits, frontmatter/fences/relative targets and git diff --check.
No test files, tooling or generated files added. One independent Review records
AC1-AC4 with exact assessed boundary and routes residual work; no second Review.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit locally and verify persistence

Dependency: P02-T01. Resolve gh api user immediately before commit, construct
id+login noreply address locally for both identities. Stage original appendix
and this dated artifact set only. Commit Refs #563 with exact Copilot trailer;
verify HEAD identities/message/paths and clean status. No amend or push.
Hash is available in Git history, not a self-referential committed receipt.

## Completion Evidence

P01-T01 completed: controlling dated appendix and both schema variants added.
P02-T01 completed: documentary assertions and independent original Review
Complete/Conformant, zero findings. P02-T02 local commit remains.
Original adverse records preserved; later full
publication gate, hosted checks and human approval remain coordinator-owned.
