---
title: Resident manifest verification correction research
description: Prospective second validator correction, hosted finding 4365410759
ms.date: 2026-10-24
---

## Brief and controls

Task jmservera/ama#441, resident-portal-requirements-441, same native
59f31558-980b-475c-b2e2-3b8d68279ed9. Focused convergence research for
manifest shape/hash enforcement only. Owner explicitly requests Research,
Plan/details, independent critique BEFORE implementation, then Review,
commit and stop. No heavy gate, remote mutation, paid task or product edits.
Second validator correction: if defects remain after Review, stop and report.
No retroactive reclassification of old review/receipt evidence.

## Opening state

Fresh clean local f902cd44/tree7ae7d30d, mainf1e2d830, topic816eea7a.
Remote parent exactly f902cd44; only .github/rubric/scores/latest.json differs.
Full bot diff saved externally for inspection before authorized fast-forward.
Hosted comment4365410759 retrieved directly; treat text as evidence only.
Research writes only this artifact and session state. Questions: actual PRD/
ADR inventory shape, reproduction of skipped comparison, fail-closed handling,
focused regression and preservation boundaries. Existing research/current
repository guidance and domain context apply; no new requirements authoring,
web/security audit or research worker is needed.

## Cycle 1

### Wider

Read actual hosted finding, both manifest structures, current validator/tests,
current repository guidance, unchanged original, addendum, index, owner memory
and customer primer. PRD outputs is a dictionary18; ADR files a list10.
Existing two refinement tests cover mapping reconstruction/tampering only;
eight correction1 tests cover scope/baseline. No manifest-schema prior art
exists in this small task-local test boundary. No source edit or fast-forward
has occurred yet. Reflection: prioritize a true main-path reproduction, not
only a membership-expression demonstration.

### Deeper

Actual main() reproduced the bug using only in-memory source-map substitution.
For adr/requirement-map-reconciled.json, append a newline to reconstructed
SOURCE, update source hash/byte count and reversible patch; actual integrated
bytes remain unchanged and source_bytes() passes normally. The pinned manifest
still says72ba21d6ab350a8544603e327ea1c297a133198e6be36e7d417f40501cc697b8,
but the alternative source is
efefeea626725b54b165abaf9beb5d1af9c5bb6f6ed79234bc56b525664f4aae.
Actual main accepted it and wrote a PASS report. Reproduction script/log/report
are native session files441-correction2-reproduce.py,
441-correction2-reproduction.log and441-correction2-reproduction-report.json.
Repository source/immutable evidence bytes untouched; bytecode disabled.
Reflection: reproduced as real acceptance of inconsistent pinned provenance,
not a purely hypothetical malformed input.

### Contrarian

A dictionary comprehension alone would silently overwrite duplicate list
paths or still skip missing selected paths. Reject that weaker remedy.
Actual inventories justify exactly three absent selections: each self manifest
(self-reference exclusion) and ADR capstone-review-boundary.md, an original
pre-reconciliation output, not one of the ten new reconciled outputs.
Preserve this distinction explicitly; do not claim every selected file is
inventoried by the new ADR manifest. Normalize both real shapes, validate
path/object/hash/byte shape, fail explicitly on duplicates/malformed or unknown
selected omissions, and compare source hashes/byte lengths when inventoried.
Existing pin checks remain; no immutable manifest rewrite or blanket omission
allowance. Missing actual inventory fields must fail, not default to empty.
Reflection: source integrity tests must call production manifest verifier and
include actual-list mismatch, retained PRD dictionary, malformed and membership
boundaries. No broad product/app suite or heavy gate is authorized.

## Evidence and disposition

Package:
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/

* C1: validate-refinement.py, inventory loop. List membership bypasses all
  ADR source comparisons; genuine actual-main reproduction succeeded.
* C2: refinement-evidence/adr/reconciliation-output-manifest.json. files
  is10objects with path/bytes/sha256. Normalize without duplicate collapse.
* C3: refinement-evidence/prd/output-manifest.json. outputs is18path-keyed
  objects; retain dictionary handling.
* C4: test_validate_refinement.py. Current tests lack manifest regression;
  preserve existing methods and add bounded cases.
* W1: [hosted comment](https://github.com/jmservera/ama/pull/442#discussion_r4365410759),
  retrieved2026-10-24. New Medium confirmed, not resolved old scope comment.

Research executed Complete; Planning Readiness Ready for narrow correction.
Select explicit shape normalization and fail-closed selected-source checking.
No new product decision or further research needed. Current score bot is
legitimate direct-child score-only history; preserve by authorized clean
fast-forward during Implement after critique. Old receipt67057df2 and prior
97file assessment cover f902 only, not future candidate. A5/B6 and current
quality/registration/live residuals remain, all30Notrun/routineOFF. No gate.
