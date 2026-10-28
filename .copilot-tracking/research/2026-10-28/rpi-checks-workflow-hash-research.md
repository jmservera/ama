---
title: Local gate workflow pin correction research
description: Focused evidence for refreshing reviewed workflow byte hashes
ms.date: 2026-10-28
---

## Brief and boundaries

Repair the stale local-gate workflow pins on main; inspect every WORKFLOWS
entry, preserve workflow files and fail-closed checks, extend only an existing
pin test, run existing tooling tests and preflight, and publish a topic PR
using Refs #500. No .env access, deployment or private-data access.
Focused convergence research prepares the explicitly requested light
Research/Plan/Implement/Review sequence.

## Extensions and participation

Repository instructions and src/README.md govern validation/publication.
The RPI phase skills govern evidence. No domain skill or research delegate is
needed for this tightly coupled, small trace. The owner supplied sufficient
scope; no clarification or automatic-mode transition is needed.
Branch fix/rpi-checks-workflow-hash is clean, has no prior PR, and starts at
origin/main 98b0bb98f2424dd23c00e386378f44892a7a79e0.

## Questions and initial research areas

1. How are workflow pins computed and enforced?
2. Which of all five workflows drift, and which merged changes justify them?
3. Which existing test and preflight interface cover this correction?

Initial areas: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md,
the five named workflow files and their Git history. External evidence is
limited to merged GitHub PR metadata.

## Cycle 1

1. Wider: inspected all five WORKFLOWS entries, runner/test surfaces, local
   gate policy and merged PR #500. Only src-deploy.yml drifts.
2. Deeper: digest() hashes raw bytes without YAML normalization. The old
   deployment pin matches the workflow at fa659cfd; the only subsequent
   deployment-workflow change is merged f183ba39 (#500): successful exact-main
   manual source CI prerequisite and retained per-image SPDX. These are
   legitimate already-merged release safeguards, not changes introduced here.
3. Contrarian: checked whether #480 also left stale CI pins. It changed
   src-ci.yml and mvp-ci.yml for AccountingSqlTests and updated both hashes
   and SQL_SELECTORS together. Both match now; mvp-validation.yml and
   infra-plan.yml also match. No wider refresh or workflow edit is justified.

## Evidence and findings

| ID | Source | Finding |
| --- | --- | --- |
| C1 | tools/rpi-checks.py:52-61,142-143 | Five explicit pins; SHA256 of read_bytes(). Comment requires intentional updates alongside native matrix changes. |
| C2 | tools/rpi-checks.py:1322-1341 | Real preflight checks tools/versions then fails closed on the first mismatched workflow. |
| C3 | tools/rpi-checks.py:1485-1529 | Deployment and infrastructure-plan steps are already classified as hosted-only; #500 needs no new local command mapping. |
| C4 | tools/test_rpi_checks.py:1217-1243 | Existing pin-drift test uses fixture workflows but only asserts some failure, missing actual repository pin consistency and per-name failure specificity. |
| C5 | src/README.md:62-137 | Documents small-task focused tier and full gate, external clean-commit receipts and required prerequisites. Standing repository instructions additionally require --all before publication. |
| C6 | tools/rpi-checks.py:2191-2210 | CLI has no preflight-only flag; Runner.preflight() is callable directly with real tools, without fabricating a full receipt. |
| W1 | https://github.com/jmservera/ama/pull/500 (retrieved 2026-10-28) | Merged f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc adds the release safeguards; no pin update. |
| C7 | Git history 864a5021, fa659cfd and f183ba39 | Confirms legitimate deployment delta and already-refreshed CI pins; all five actual files were hashed. |

| Workflow | Current raw-byte SHA256 | Before correction |
| --- | --- | --- |
| src-ci.yml | 843077a5d5ffc5fe0c9b6ce2933b6fb46393016e6ca7ece248235cf3229d3d7c | Match |
| mvp-ci.yml | 92178fff316a4cd8b4e619c47e96c0238106c311cad928263b6e795797a3a54e | Match |
| mvp-validation.yml | 94feeb7e0c6807a94dc2624eaf7c5e76c807a234e1777b593b169fd801e511cc | Match |
| src-deploy.yml | 3c2f1ed59b1486fc1316a48207cc4ef7d6a830bbba1dcad4152acab4bd2f1bbc | Drift |
| infra-plan.yml | 232e84f01559055bc2121379a44c6ac3121e66f9e398e92e6a571a26c8c00a88 | Match |

## Decision, readiness and self-check

Accept one explicit deployment hash refresh (C1-C3, C7, W1) and extend the
existing test (C4) to check real repository pins and deliberate per-file
fixture drift. Reject automatic hash generation or bypasses, which weaken
the intentional-review policy. Reject changing the four matching pins.
Baseline: all 30 runner tests passed (10.471s).

Research Complete; disposition executed; Planning Readiness Ready. No
unresolved research questions or further cycle needed: every named workflow
and material claim has evidence. No delegation, workflow/.env edits or source
edits occurred in Research. Parent may continue the explicitly requested Plan.
