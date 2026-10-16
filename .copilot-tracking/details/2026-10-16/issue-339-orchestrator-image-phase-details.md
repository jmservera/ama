---
title: Issue 339 phase details
description: Bounded implementation and evidence expectations for image normalization
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-339
* Task slug: issue-339-orchestrator-image
* Plan: .copilot-tracking/plans/2026-10-16/issue-339-orchestrator-image-plan.md
* Evidence: .copilot-tracking/research/2026-10-16/issue-339-orchestrator-image-research.md

<!-- rpi:phase id=P01 -->
## P01: Normalize and verify the deployment CLI

Status: implementation validated; review and publication pending.
P01-T01 complete; P01-T02 documentation/validation complete, publication pending.
No unresolved product decisions.
Scope is explicit input only; do not normalize discovery outputs or change
authentication, Bicep or setup-entra. Do not invoke live Azure.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add regression coverage and normalize input

Use `DeployTests.run_deploy` with isolated fake az. Expand empty-image test
to empty, spaces and tabs/newlines, both actions and both current-job and
no-image outcomes. Assert exact forwarded image, discovery command sequence,
source and warning presence/absence. Expand explicit-image test with padded
tag/digest/placeholder inputs. Keep harness ownership and test budget in plan.
Run the new tests before the change to establish the regression signal.
Then strip the parsed explicit option once before image selection and rerun
the entire deploy test module, including existing guard and error regressions.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Document, validate and publish

Document trimming and blank resolution in `infra/README.md`; append a dated
entry to `docs/reference/log.md`. No synthesis or index routing changes needed
for an infra CLI contract clarification. Run scoped isolated Ruff lint/format,
mypy check-untyped-defs, local `deploy.py --help` and `git diff --check`.
Record exact counts, red/green behavior, criterion results and unperformed live
checks in changes/review artifacts. Preserve issue body. Authenticate commit
identity locally, use required trailer, push branch and open PR against main.
Completion evidence includes PR URL and published branch commit.

### Observed Completion Evidence

Expanded tests failed on unfixed CLI: 19 methods, 11 failing subcases (eight
whitespace-resolution and three padded explicit-image cases). After trimming:
19 methods passed, including all 12 blank-resolution and six explicit-image
subcases. Scoped Ruff lint/format and mypy passed. CLI help and diff check passed.
README and append-only log updated. Full commands in changes artifact.
