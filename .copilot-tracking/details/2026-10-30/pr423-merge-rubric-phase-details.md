<!-- markdownlint-disable-file -->
# RPI Phase Details: PR423 merge and rubric diagnosis

## Metadata

* Task ID: pr423-merge-rubric-2026-10-30
* Task slug: pr423-merge-rubric
* Plan: .copilot-tracking/plans/2026-10-30/pr423-merge-rubric-plan.md
* Research: .copilot-tracking/research/2026-10-30/pr423-merge-rubric-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Preserve integration and improve evidence | Complete | P01-T01, P01-T02 |
| P02 | Validate and deliver local candidate | Complete execution; gate blocked | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Preserve integration and improve evidence

Owner permits merge; preserving ancestry is lower risk than rebase. No
application migration back to mvp, no Azure and no unrelated worktree access.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Merge and reconcile conflicts

* Evidence: research C1,C7-C10; merge-tree preview.
* Targets: evidence pack ms.date, KB index metadata, KB log, gate workflow hash.
* Use 2026-10-30 metadata and keep useful ms.topic. Both bodies survive.
* The log conflict is one appended range on each side: remove markers, retain
  both byte-identical entry sequences, add new entry only after both.
* Recompute SHA256 of actual auto-merged src-ci.yml. Keep main's other hashes
  and runner additions plus Blob lint/type group entries.
* Inspect infra README for dated supersession: newer main approvals/retirement
  coexist with older tag design marked historical and DN1-DN5 Blob decision.
* Verify both new IoT sender/receiver scopes and container-only Blob writer.
* Record two-parent preservation ledger against pinned original head and main:
  classify resulting differing paths, explain any deletion/function/assertion
  loss, verify old tracking evidence byte-identical, and verify both appended
  log sequences survive in order. Map each DN1-DN5 to retained authoritative
  text and code or explicit dated supersession. Tests alone are insufficient.
* Expected semantic selectors: RoleMatrixTests, storage/retired-tag/
  profile-bound credential/BuildContextTests in test_staff_azure, Bicep policy,
  gate matrix drift, rename-zava migration and namespace checks. Keep both
  Blob lint/type group entries and main's current gate matrix.
* Completion: no conflict markers, both ancestor histories, tests and docs intact.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add exact regression and honest evidence navigation

* Dependency: P01-T01.
* Test ownership locked in plan: two parameter cases, zero removals.
* Adapter malformed-details parameter: D1 extra evidence2 must raise exact error.
* jq parameter: same exact shape must fail; valid full card still unchanged.
* Infra README: concise implementation claim/evidence/rationale/change_reason
  matrix, alternatives and unverified outcomes, linked tests; already scored
  infrastructure artifact, not new scoring registry coverage.
* Rubric README: incident cause, schema-vs-grade distinction and existing
  preflight; no demand on scoring agent to award a grade.
* Evidence pack/index/log: record integration and honest scope boundary; main's
  later live/identity/retirement entries remain authoritative for their scope.
* Completion: source-backed references, no fabricated execution, all decisions kept.

<!-- rpi:phase id=P02 -->
## P02: Validate and deliver local candidate

Local-only bounded validation. Historical receipts do not validate new inputs.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run targeted local validation

* Dependency: P01.
* Run existing infra discovery with REQUIRE_AZ_BICEP=1 (offline compile only).
* Run rubric adapter, gate, prepare, record-workflow and tools gate tests.
* Run migration regression and relevant Ruff, mypy and native actionlint.
* Use installed src distributions. Do not read private datasets or real profiles.
* Capture command counts, skips and failures. Compare baseline only where
  necessary to distinguish inherited failures; do not fix unrelated debt.
* Missing dependencies: restore in task-owned external environment after the
  actual failure. No shared venv mutation.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile evidence, Review once, commit and attempt full gate

* Dependency: P02-T01.
* Reconcile plan markers and changes before Review. Independent Review writes
  only its dated artifact; keep human-review checkboxes unchecked.
* Classify each finding as blocking acceptance or a deferrable residual risk.
  Unresolved acceptance failures require Not accepted/Blocked handoff, never
  a successful acceptance claim. Retain the single original Review and route
  later work without repeating critique/Review or returning to implementation.
* Critique PC-002's claimed /tmp runtime prohibition does not exist in this
  parent's instructions; do not invent that blocker. Use ordinary local gate
  serialization and task-owned output, preserving actual failures.
* Commit local integration/evidence, privacy-safe identity and Copilot trailer,
  `Refs #360` only. No amend, force push, remote update or issue closure.
* Full gate: `python3 tools/rpi-checks.py --all --base 5634f9a077d175a931c15e3400114665d8c071ee --out <new-external-directory>`.
* Preserve failed gate evidence; only a successful receipt may be verified.
  Any later commit invalidates earlier gate evidence; coordinator must rerun
  if a final evidence-only commit is needed. No publication here.
* Completion: original Review, committed candidate, transparent gate disposition
  and coordinator handoff, not implied human/hosted approval.

Actual P02-T02 outcome: merge commit f74b270d7cd370173272b801ff3a93b434b37262
contains both pinned parents and original Review evidence, with privacy-safe
author/committer and required trailer. The first gate refused task-generated
ignored caches; 163 files in 16 exact cache/metadata directories were reversibly
externalized with verified archive/restore hashes and no tracked-file removal.
The clean retry then timed out on the shared heavy-resource lock after
600 seconds, before checks or receipt creation. Original adverse Review and
gate results remain; coordinator publication is blocked pending a new full
gate at the final clean commit/current reviewed main.
