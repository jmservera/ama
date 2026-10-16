---
title: Issue 339 image normalization research
description: Reused repository evidence for the explicit image whitespace defect
ms.date: 2026-10-16
---

## Task and Disposition

Task ID: issue-339. Slug: issue-339-orchestrator-image.
Research disposition: reused. Planning Readiness: Ready.

Issue #339 requests stripping explicit `--orchestrator-image` and resolving
an empty result (or rejecting it), with regression coverage. It has no
checkbox acceptance list. The existing empty-string resolution contract makes
normal discovery the least surprising choice.

## Evidence

* `infra/scripts/deploy.py`: the explicit option is tested for truthiness
  without stripping; discovered blank job images already fail explicitly.
* `infra/tests/test_deploy.py`: subprocess CLI tests install an isolated fake
  `az` on PATH, recording calls and replies. Existing tests cover empty input,
  explicit tags/digests/placeholder, precedence, errors and authentication guards.
* `infra/README.md`: Orchestrator image selection documents empty input as
  normal resolution, explicit overrides and placeholder warnings.
* Issue #339 and merged PR #337 establish this as a small follow-up to #322.
  Clean branch `fix/orchestrator-image-whitespace-339` has no PR.
* Required case studies, reference index/memory and ADR 0006 were consulted.
  No regulatory interpretation or operational approval is involved.

## Boundary and Adequacy

Normalize only the explicit CLI option before branching. Preserve discovery,
authentication guarding, deployment parameter forwarding and exit behavior.
Cover empty, spaces, tabs/newlines; preserved current image; warned placeholder;
padded valid explicit tag/digest/placeholder; both what-if and apply.
No Azure calls, private data, setup-entra edits, legacy-path changes or web edits
are needed. No further research or unresolved product decision is required.
