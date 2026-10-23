---
title: Issue 350 AI item uniqueness phase details
description: Task-level evidence, boundaries and exact validation commands
ms.date: 2026-10-23
---

## Metadata and Initial Direction

Task ID/slug: issue-350-ai-item-uniqueness. Date: 2026-10-23.
Plan: .copilot-tracking/plans/2026-10-23/issue-350-ai-item-uniqueness-plan.md.
Research: .copilot-tracking/research/2026-10-23/issue-350-ai-item-uniqueness-research.md.
Research C1-C5 is adequate. Plan checklist precedes all source changes.
Publication is blocked by ancestry; no local implementation decision is open.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Real red then uniqueness-only green | Complete |
| P02 | One original Review then commit | Review complete, commit pending |
| P03 | One gate and receipt verification | Pending clean committed P02 |

<!-- rpi:phase id=P01 -->
## P01: Red-first bounded implementation

Context: checker validates shapes but accepts duplicate IDs; runtime uses raw
set equality. Only two tools files may change; previous artifacts are immutable.
No new runtime import, network, write, AI, semantic rule or count cap.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Uniqueness regression and genuine red

Owner: parent implementer. Canonical target: AiEvidence in
tools/test_check_demo_feedback.py. Maximum two added methods, no removals or
generated targets. Duplicate matrix: identical items, same ID/different reason
and cites, nonadjacent repetition. Assert component fail, explicit duplicate-ID
reason and not-accepted. Distinct matrix: synthetic runtime-shaped IDs,
including raw string distinctions without lookup/normalization, assert pass
and unchanged blocked/not-run/not-accepted residuals. Existing runtime-validator
positive continues to demonstrate authentic runtime output shape.

Use the already verified installed venv, from repo root:

```bash
PYTHONDONTWRITEBYTECODE=1 /tmp/ama-350-ai-item-shape-20261023-0752-venv/bin/python -B -m unittest tools.test_check_demo_feedback.AiEvidence -q
```

Capture stdout/stderr and exit status in a unique external task-evidence folder.
Do not edit checker until duplicate failures are observed and recorded.
Completed: 18 AiEvidence methods ran before checker edits, six expected
duplicate subtest failures (three payload/position variants, both origins).
Distinct-ID matrix and existing 16 methods passed. Red exit 1.
Log: /tmp/ama-350-ai-item-uniqueness-20261023-evidence-wZJWUQhM/red.log.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Shape-guarded uniqueness and focused green

Owner: parent implementer. Existing shape validation proves IDs are strings
before hashing. Add an `elif` set-cardinality check and append
`duplicate case IDs`; preserve existing FAIL aggregation. Clarify module docs
with unique case IDs; no general refactor.

```bash
PYTHONDONTWRITEBYTECODE=1 /tmp/ama-350-ai-item-shape-20261023-0752-venv/bin/python -B -m unittest tools.test_check_demo_feedback -q
PYTHONDONTWRITEBYTECODE=1 /tmp/ama-350-ai-item-shape-20261023-0752-venv/bin/python -B -m ruff check --isolated --no-cache --select E,F,W,B,BLE,I --ignore E501 tools/check-demo-feedback.py tools/test_check_demo_feedback.py
PYTHONDONTWRITEBYTECODE=1 /tmp/ama-350-ai-item-shape-20261023-0752-venv/bin/python -B -m ruff format --isolated --no-cache --check tools/check-demo-feedback.py tools/test_check_demo_feedback.py
git diff --check
```

Full focused suite must pass with prior tests retained. Check actual diagnostic
and each residual boundary, not a proxy overall status. Reconcile plan markers,
details and changes evidence before Review. No known blocker.
Completed: shape-guarded two-line uniqueness check and module-description
clarification only. Both new methods retained. Full suite: 72 tests passed;
Ruff lint passed, first format check required one assertion-line reflow,
formatter applied, final focused run/lint/format/diff checks all passed.
Final log: /tmp/ama-350-ai-item-uniqueness-20261023-evidence-wZJWUQhM/green-final.log.

<!-- rpi:phase id=P02 -->
## P02: One original Review and committed candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Original RPI Review

Activate rpi-review once after P01; compare FR1-FR3/NFR1-NFR3/AC1-AC5 and
critique dispositions to actual diff/logs. Only the new Review artifact is
review-writable. No source changes, repeated Review or claim of independent
coordinator/human approval. Any in-scope blocker stops commit/gate and routes
later work. Expected outcome can retain pending delivery as residual work.
Completed: one original Review executed, Complete / Residual work, no in-scope
blocking defect. RV-001 is pending authorized delivery, RV-002 separate
lineage/independent/live acceptance. Original Review will not be edited again.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Identity and commit

Resolve `gh api user` id/login; repository-local name/email
`{id}+{login}@users.noreply.github.com`, used for author and committer.
Conventional Commit: `fix(tools): reject duplicate captured AI case IDs`.
Required trailer: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
Stage only the two tools and seven newly dated correction artifacts.
Read-only fetch main confirms caller base. No push, remote mutation, rebase,
merge, rewrite, amend or PR/issue edits.

Review and commit/gate sequence creates an evidence snapshot with downstream
delivery pending. Record actual commit/gate completion externally rather than
making a second evidence commit or modifying a receipt-bound worktree.
Actual gh identity resolved: id 8036360 / login jmservera. Fetched origin/main
matches exact caller base. Pre-existing generated bytecode (08:34 UTC, before
intake) must be archived externally, then only the inspected .pyc files and
empty cache directories removed before gate. No authored work is discarded.

<!-- rpi:phase id=P03 -->
## P03: Exactly one complete gate

<!-- rpi:task id=P03-T01 -->
### P03-T01: Gate, verifier, hash and closeout

Caller base is fixed; if fetched main differs, record discrepancy without
changing base/ancestry. Use one unique new external gate directory:

```bash
python3 tools/rpi-checks.py --all --base 140d8f494482c78e84d15f3d46b9223d3c487af0 --out /tmp/ama-350-ai-item-uniqueness-UNIQUE-gate --lock-timeout 86400
python3 tools/rpi-checks.py --verify-receipt /tmp/ama-350-ai-item-uniqueness-UNIQUE-gate/receipt.json --base 140d8f494482c78e84d15f3d46b9223d3c487af0
sha256sum /tmp/ama-350-ai-item-uniqueness-UNIQUE-gate/receipt.json
```

UNIQUE is resolved once to a fresh directory before invocation, not overwritten.
Do not duplicate/interfere with another gate; wait for shared lock as needed.
Record exact head/base, official verifier output and hash externally. Required
failures remain blocked, not fabricated acceptance; no cloud fallback.
Stop after validation per caller, leaving lineage and independent review to
coordinator. No source/state/plan edits after exact-head gate begins.
