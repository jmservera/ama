---
title: Resident manifest verification correction phase details
description: Fail-closed manifest contract and caller-level regression boundary
ms.date: 2026-10-24
---

Task jmservera/ama#441, same native59f31558. Research Complete/Ready,
implementation pending independent critique. Entryf902/basef1e2d830/
remote816eea7a, verified single score-only direct-child commit.

<!-- rpi:phase id=P01 -->
## P01 - Correcting manifest enforcement

<!-- rpi:task id=P01-T01 -->
### P01-T01 - Preserving bot history

Recheck current main/topic and complete diff/parent before ff-only merge.
Only known run-created untracked tracking files exist; do not stash/discard.
Remote score JSON must remain exact bot bytes, no manual generated change.
Do not broaden clean integration into rebase/cherry-pick/force or sibling work.
If refs differ, stop and report. Preserve previous receipts/environments.

<!-- rpi:task id=P01-T02 -->
### P01-T02 - Normalization and explicit verification

Add small task-local production helper(s), no abstraction framework/dependency.
Dictionary items already path keyed; ADR list entries carry path field.
Reject non-dict/list, empty inventory, invalid entry/path (nonempty relative
normalized path), sha256 not lowercase64hex, bytes not nonnegative integer,
duplicate list path. Require actual fields, not silent defaults.
Normalize once per manifest. Compare matching selected source hashes and
source bytes with explicit contextual ValueError. Missing selected entry fails
except exact self manifest and ADR capstone-review-boundary.md, a legacy output.
The self manifests are independently pinned; capstone remains mapping-checked,
not falsely claimed authenticated by new reconciliation-output manifest.
If listed, even an exception is checked. Manifest shape only, no source edits.

<!-- rpi:task id=P01-T03 -->
### P01-T03 - Focused evidence

Existing ten methods retained, at most five new unittest methods. Include
ADR list hash mismatch/size mismatch and positive PRD dictionary, malformed/
duplicate/badentry/missing cases using real-shaped fixtures. Actual main
caller test uses real pinned manifests and in-memory source-map injection:
append SOURCE newline, recompute reversible source patch/hash/bytes while
actual integrated bytes and manifest unchanged. Assert contextual hash failure
before any expensive lint, no downstream quality/pin proxy. Existing source
reconstruction must pass independently first. Research external script run
again should now fail at manifest mismatch; preserve both before/after logs.
Run combined test_validate*.py once after coherent batch, both existing
validator CLIs with existing external markdownlint and unique external reports.
Run links/lint on new artifacts, hash/diff preservation vsbot/product baseline.
Report12archived FAILED whitespace diagnostics explicitly, never repair or
mislabel all-branch diff check PASS. No heavy gate.

<!-- rpi:phase id=P02 -->
## P02 - Reviewing and handing off

<!-- rpi:task id=P02-T01 -->
### P02-T01 - One Review

Reconcile P01 markers/changes/details/results, preserve old adverse reports.
Read actual correction diff/tests/caller behavior and record complete
prospective Review execution/outcome, original limitations/current residuals.
If defect remains, route and stop, no post-Review edit/repeat cycle.

<!-- rpi:task id=P02-T02 -->
### P02-T02 - Commit and exact handoff

gh api user, repository-local privacy-safe author/committer identity and trailer.
Commit only correction files/new artifacts; bot already ancestor. Postcommit
focused results external, final tracked/untracked/ignored clean. Fresh refs,
head/tree/base/remote lease and actual commands/report hashes in session
handoff. P02 commit completion cannot be pre-claimed in committed artifact;
final state/evidence external. No push/PR edit/heavy gate or extra work.

## Implemented State for Review

P01-T01/T02/T03 Complete. Bot fast-forward is real, exact score hash retained.
Production helpers normalize both contracts, reject malformed/duplicate entries
and unknown selected omissions, compare source hash and byte count. Five added
methods retain all10originals;15total pass. Actual main reproduction now raises
ValueError identifying ADR requirement-map-reconciled.json hash mismatch.
Both actual validators pass. No product/evidence/score/old-test change.
Research and critic new tables needed only Markdown reflow before Review;
all original critic text/Pass/no-findings retained. Exact original critic is
external SHA9b892dd531e5ab898507ee4e7fccf9b9e4c760c1a09fb07c25a5610dc8770eb0.
No significant divergence/decision/second critique. Full-branch diff check
FAILED52historical diagnostics including12refinement, unchanged before/after;
correction-only whitespace passes. Review assesses these actual limits.
