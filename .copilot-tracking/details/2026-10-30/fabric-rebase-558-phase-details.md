<!-- markdownlint-disable-file -->
# RPI Phase Details: Fabric PR 558 reconciliation

## Metadata

Task ID: 558. Task slug: fabric-rebase-558. Date: 2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/fabric-rebase-558-plan.md.
Research: .copilot-tracking/research/2026-10-30/fabric-rebase-558-research.md.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Reconcile branch | Complete | P01-T01 |
| P02 | Validate and prepare Review | Complete | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Reconcile branch

Research establishes one original eight-file commit f009d37 and fetched main
91e890e07af036263316c153cbc7ceff780cdaa2. The worktree was clean before
task-owned tracking files. Only log/index changes overlap with main.
Preserve original snapshots; no automatic cleanup or historical rewriting.
This SHA is historical, not an execution constant. Fetch again, record the
resulting execution BASE_SHA and bounded drift, then use that immutable SHA for
rebase and all preservation assertions. Detect final origin/main movement and
report/reconcile before any current-main-ready claim.
Execution base: ffd8f35e63b24905b9aeb937dbf2a7fe9968747f. Rebased original
commit: 4f593aae9e30df5d28dd4b6ca8942b4e1fe471aa. Exact preservation,
upstream equality and ancestry assertions passed; sole log conflict resolved
with union. Index date and append-only reconciliation entry added afterward.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and preserve both documentation intents

Intent: execute the owner-authorized local rebase; resolve shared log by keeping
the upstream file intact and appending the original Fabric entry. Let Git merge
independent index entries; retain upstream duplicate-frontmatter repair.
Take fetched-main rubric/manifest content if any conflict touches those paths.
Append one dated reconciliation log entry and set index ms.date to 2026-10-30.

Targets: docs/reference/log.md and docs/reference/README.md; no source changes.
Dependencies: single critique finalized; original commit and base IDs retained.
Completion: no conflict stages, main ancestry, upstream log prefix, original
Fabric entry intact, original six standalone research files byte-identical,
upstream-owned files equal main. No unresolved decision.

<!-- rpi:phase id=P02 -->
## P02: Validate and prepare Review

Existing /tmp/mv tools are installed; do not mutate its editable installs.
Prepend each project's src/tests and sibling core/agents src/tests so direct
imports use this worktree. Check actual resolved __file__/__path__ before units.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run scoped checks and reconcile evidence

From each of src/core and src/api, use /tmp/mv/bin/ruff check .,
ruff format --check ., and mypy --cache-dir with distinct external directories.
Supply local source/test paths for type resolution where needed.
All generated validation output, TMPDIR and distinct mypy cache directories
belong beneath the finite task-owned external directory
/home/azureuser/.copilot/session-state/923145f6-b93f-43a3-8d95-aae33eec3177/files/fabric-558-validation.
Set PYTHONDONTWRITEBYTECODE=1 and RUFF_NO_CACHE=true; do not mutate /tmp/mv.
Retain this evidence externally; no historical cleanup or candidate-local
generated output is authorized or needed.
Core units: test_scenario_manifest and test_dependency_rule. API units:
test_dependency_rule. Run python tools/rename-zava-tests.py from root with local
source/test paths. No full API discovery, browser, SQL, Docker, cloud or model
run is selected for this documentation-only implementation.

Semantic assertions must compare actual preserved bytes, not just grep for
headings. Inspect new relative documentation links and frontmatter uniqueness.
Use git diff --check and prove final diff contains documentation/tracking only.
Record exact commands/exits/counts and adverse attempts in changes, and reconcile
all checklist status before the single independent Review.

Parent closeout: independent Review has read access and writes only its original
Review artifact. Preserve findings; route any remaining work honestly. Resolve
authenticated account's noreply identity before commit; use a new Conventional
Commit and required trailer, never amend or push. Verify clean status, ancestry,
commit metadata and remote branch unchanged. Publication remains coordinator-owned.

## 2026-10-31 Continuation Details

The owner selected a local rebase of the existing published topic, without a
force-push. Recovery ref `chore/fabric-558-pre-rebase-20261031` retains
`bde84d8b`. First execution main is `18602ae7`; first completed replay is
`97193264`. No prior execution or Review is rewritten by this continuation.

P03 is complete. Resolve shared index/log conflicts by union. For the duplicate
gate replay, retain main's exact implementation/tests and detailed guide, plus
the branch's hosted browser command and updated workflow hash. Keep upstream
rubric scores and scenario manifest, and retain later capstone registry edits.
The five conflict paths are the KB index/log, src guide, gate runner and scores.

For review feedback, document exact UTF-8 LF source hashing and Verify the actual
delivered PPTX in external scratch. Preserve the matching output bytes and all
earlier preview/native limits. Replace only the four unsupported finite guards;
exercise NaN and both infinity signs for every guard using the existing script.

All output belongs to the task-owned external directory:
`/home/jmservera/.copilot/session-state/684453ca-82ac-4b63-accd-515f3e4b285b/files/fabric-558-20261031`.
The original `/tmp/mv` environment is absent. Restore actually missing packages
with pip into this run's venv, not shared environments; use the existing pinned
project/capstone/migration manifests. Chromium is likewise run-owned.

P04 remains active: main advanced independently to `ec2d7842` with resident chat
and rubric evidence changes. Commit the validated correction, rebase cleanly,
recheck current-main byte ownership, rerun affected API/Chromium checks and
retain an independent continuation Review. The original 17 rubric failures
also occur on unchanged main; no success or publication receipt is fabricated.
