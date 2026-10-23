---
title: Offline feedback AI item shape phase details
description: Evidence and completion expectations for bounded correction
ms.date: 2026-10-23
---

## Metadata

Task ID/slug: issue-350-ai-item-shape.
Plan: .copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md.
Research: .copilot-tracking/research/2026-10-23/issue-350-ai-item-shape-research.md,
C1-C8. All work confined to caller worktree; no blockers to bounded implementation.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | P02-T01 complete; P02-T02 pending | P02-T01, P02-T02 |
| P03 | Pending committed P02 | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Red-first tests and bounded checker correction

Runtime `priority_items` and `_rec_view` establish output field types. Only
captured shape can be checked without source labels. Keep all other guards.
Tests own synthetic fixtures; no model, network or store writes required.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add focused tests and record red

Target AiEvidence in tools/test_check_demo_feedback.py. At most six new methods,
no removals. Exercise missing keys, null/bool/number/list/object and empty/
whitespace strings for case_id/reason; cites container missing/wrong/empty,
and element null/bool/number/list/object/empty/whitespace, including mixed
valid/invalid entries and both supplied minimal repros. Assert component FAIL
and diagnostic, not aggregate blocked as a proxy.

Use runtime `priority_items` with synthetic source labels to produce positive
item shape without inference; retain enriched fixture positive. Assert unchanged
durability/spend/admin/acceptance boundaries for valid evidence.

Run new negative selectors with:
`PYTHONDONTWRITEBYTECODE=1 /tmp/ama-350-ai-item-shape-20261023-0752-venv/bin/python -B -m unittest tools.test_check_demo_feedback.AiEvidence -q`.
Save actual red output externally, before editing the checker.

Completion: six new methods, no removals; existing misleading positive method
renamed to runtime-shaped capture. Genuine red: 16 AiEvidence tests run, 44
failing subtests, exit 1 before checker edits. Log:
`/tmp/ama-350-ai-item-shape-20261023-evidence-0752/red.log`.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Guard, docs and focused green

Extend the existing `all` predicate using `nonempty_str` for case_id/reason and
each cites element, retaining list/object checks and existing FAIL diagnostic.
Update checker module documentation to distinguish shape validation from
self-reported runtime provenance. No source membership/semantic check,
cardinality cap, exact item key set or other guard changes.

Run full `tools.test_check_demo_feedback` with installed distributions and -B.
Run isolated Ruff lint (E,F,W,B,BLE,I; E501 ignored) and format check without cache
on both files, then git diff --check. Evidence records actual test counts,
failures and scope. Remove only bytecode created by the initial failed probe.

Completion: item predicate now uses existing nonempty_str helper for all three
field classes; checker module docs state shape/provenance boundary. Full focused
module: 70 tests pass. Ruff 0.17.1 lint and format pass on both files; diff check
passes. Green log:
`/tmp/ama-350-ai-item-shape-20261023-evidence-0752/green.log`.
Package installation also created ignored egg-info in the three installed
project source paths; remove only these task-created directories before gate.

<!-- rpi:phase id=P02 -->
## P02: One Review and clean candidate commit

<!-- rpi:task id=P02-T01 -->
### P02-T01: One original RPI Review

Reconcile current checklist, details, changes and critique dispositions first.
Activate rpi-review once after P01, assessing complete bounded task and runtime
contract with focused evidence. This is not independent coordinator review or
hosted/human acceptance. Route any finding to later work, not another Review.
Full gate is pending until commit; do not invent or retroactively change history.
Review execution and outcome are separate. An unresolved in-scope blocking
finding stops the full gate and publication, even when focused tests pass.
Known excluded live/coordinator residuals remain explicit, not local acceptance.

Completion: one original self-review, execution Complete / outcome Residual work.
No in-scope blocking defect. RV-001 routes commit/gate/publication to parent;
RV-002 routes independent coordinator and excluded live acceptance separately.
No second Review or claim of independent assessment.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Privacy-safe candidate commit

Resolve `gh api user`; set repository-local user.email to returned numeric ID
and login at users.noreply.github.com. Use it for author and committer and
Conventional Commit with required Copilot co-author trailer. Commit all intended
correction source and dated original RPI evidence, preserving old files.
Mark P01/Review truthfully complete; commit/gate/delivery markers are pending in
committed snapshot, with later status external to avoid receipt self-reference.

<!-- rpi:phase id=P03 -->
## P03: Exact-head gate and delivery

<!-- rpi:task id=P03-T01 -->
### P03-T01: One complete gate and verifier

Fetch main, require caller base
`140d8f494482c78e84d15f3d46b9223d3c487af0`, and clean candidate including
ignored inputs. Run exactly once:

```bash
python3 tools/rpi-checks.py --all --base 140d8f494482c78e84d15f3d46b9223d3c487af0 --out /tmp/ama-350-ai-item-shape-20261023-final-unique --lock-timeout 86400
```

The output path is a planned new unique external directory (verify absent).
Prerequisites include no unresolved in-scope blocking Review finding.
Wait for lock; never duplicate. Then fetch main again; verify immediately before
push using `--verify-receipt <receipt.json> --base 140d8f494482c78e84d15f3d46b9223d3c487af0`.
Record receipt SHA-256, exact head/tree/base, verifier exit/output externally.
Gate failure/base movement blocks publication without rerun or cloud fallback.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Authorized normal push and draft PR update

Normal push existing branch only after passes; update PR #436 with exact head/base,
scope, focused/full-gate evidence, receipt path/hash/verifier and explicit open
acceptance. Keep draft and issue #350 open/unticked. Do not use closure keywords.
Coordinator independently reviews afterward; no merge or claim of that review.

## Remaining Acceptance Boundaries

case_write_reload blocked, spend_bound/admin_account not-run; overall not-accepted.
No deployed/paid AI task, SQL durability, Azure/tenant change, private data,
whole-issue acceptance, coordinator review or merge. No unresolved coding decision.

## Critique Dispositions

PC-001 is rejected as inapplicable to parent execution: /tmp is permitted by the
caller and documented gate guide. Worker-local temporary-path restrictions do
not extend parent authority. PC-002 is applied in P02-T01/P03-T01 before source
edits. The original critique remains unchanged; no second critique is needed.
