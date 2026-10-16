---
title: Issue 339 implementation evidence
description: Changes and validation for explicit orchestrator image normalization
ms.date: 2026-10-16
---

## Scope and State

Task ID: issue-339. Slug: issue-339-orchestrator-image.
Full plan scope: P01-T01 and P01-T02.
Plan: .copilot-tracking/plans/2026-10-16/issue-339-orchestrator-image-plan.md.
Implementation validated; P01-T01 complete. P01-T02 documentation and validation
complete, publication pending. One critique complete, PC-001 disposed by parent
in plan. No product blockers or significant divergences.

## Validation Preparation

`python3 -m ruff --version` and `python3 -m mypy --version` both failed with
missing modules. Created /tmp/ama-339-validation and installed ruff 0.17.1 and
mypy 2.4.0 with pip. This is tooling restoration, not an Azure command.
No project dependency or persistent environment configuration changed.

## P01-T01: Explicit Image Normalization

Added one strip operation immediately after argument parsing, before image
selection. Discovery and authentication guards remain unchanged.
Expanded existing tests only: 19 methods remain, no methods added or removed.
Blank matrix: three inputs (empty, spaces, tabs/newline), two actions and two
resolution outcomes = 12 subcases. Explicit-image matrix: tag, digest and
placeholder, each plain/padded = six subcases.

Regression signal: expanded tests against unfixed code ran 19 methods and
reported 11 failing subcases (eight whitespace-resolution and three padded
overrides). After fix all 19 methods passed.

## P01-T02: Documentation and Validation

Updated infra README contract and appended reference log. No synthesis or
reference routing changed, so the index is unchanged. No unrelated files edited.

Commands from repository root:

```bash
PYTHONPATH=/home/azureuser/source/ama-wt/issue-339/infra/scripts python3 -m unittest discover -s infra/tests -p test_deploy.py -q
/tmp/ama-339-validation/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/deploy.py infra/tests/test_deploy.py
/tmp/ama-339-validation/bin/ruff format --isolated --line-length 100 --check infra/scripts/deploy.py infra/tests/test_deploy.py
/tmp/ama-339-validation/bin/mypy --check-untyped-defs infra/scripts/deploy.py infra/tests/test_deploy.py
python3 infra/scripts/deploy.py --help
git diff --check
```

Results: 19 tests passed; Ruff passed; two files already formatted; mypy no
issues in two files; local CLI help and diff check passed. The subprocess tests
run the real local deployment CLI against fake az; no HTTP application changed,
so unrelated application startup is not needed. No Azure commands or live
deployment validation performed; no live acceptance claimed.

## Acceptance Audit Before Publication

| Criterion | Result | Evidence |
| --- | --- | --- |
| AC1 blank input resolves | Pass | All 12 blank-input subcases, exact forwarded image and discovery sequence |
| AC2 current image / warned placeholder | Pass | Both resolution outcomes for each blank input/action; warning presence/absence |
| AC3 padded explicit images | Pass | All six tag/digest/placeholder subcases; one deployment call, no discovery |
| AC4 both actions / existing behavior | Pass | What-if/create exact command and image assertions; all 19 deploy regressions |
| AC5 documentation / artifacts / PR | Partial | README/log/research/plan/changes present; Review and publication pending |

Issue #339 contains prose rather than a checkbox list. These criteria decompose
that request plus caller constraints; no issue body changes were made.

## Remaining Work and Review Handoff

Execute one post-implementation review of current CLI/tests/docs and evidence.
Then commit/push/open PR with `Refs #339`; publication evidence completes AC5.
No implementation blockers, open defects or routed follow-ups currently known.
