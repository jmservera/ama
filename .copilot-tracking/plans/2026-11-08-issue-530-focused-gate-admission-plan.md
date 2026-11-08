---
title: Issue 530 focused-gate admission plan (supersedes Phase 4 wording)
ms.date: 2026-11-08
---

* Research: [.copilot-tracking/research/2026-11-08-issue-530-focused-gate-admission-research.md](../research/2026-11-08-issue-530-focused-gate-admission-research.md)
* Details: [.copilot-tracking/details/2026-11-08-issue-530-focused-gate-admission-details.md](../details/2026-11-08-issue-530-focused-gate-admission-details.md)
* Original plan [.copilot-tracking/plans/2026-11-08-issue-530-chat-local-unit-plan.md](2026-11-08-issue-530-chat-local-unit-plan.md) is unchanged; its Phase 4 remains blocked and not executed. This plan supersedes only its admission wording.
* Tier: FOCUSED, tracking-only. No gate, probe, test or install runs in this continuation.

## Phases

* [x] Phase 1: critique this admission plan once before implementation.
* [x] Phase 2: write admission changes, state and review records; prove executable inputs byte-identical to `ed19cb94`.
* [x] Phase 3: commit, freeze clean, stop. Future gate admission is a separate later step and is not admitted now.

## Admission rule (replaces the unsatisfiable condition)

Focused gate admission is allowed only when all hold at that later time: the canonical lock is free (no polling or queueing now; `--lock-timeout 0` fails fast otherwise); Main is fetched; HEAD is clean ignored-inclusive and its executable inputs equal `ed19cb94`; BEFORE invocation, `git diff --name-only --no-renames <fetched-main>...HEAD` lists only inert paths (`.copilot-tracking/`, `docs/`, `support/`, `*.md`), otherwise stop and report without running; the runner's printed `groups=` line must then be exactly `preflight,namespace,static`. Docker daemon access, Docker/Trivy/other version probes, the namespace and static pip installs, ruff/mypy, actionlint and the runner's own unit tests are maintained behaviour and allowed. Services, image builds, scans, SQL and browser are not allowed and must not be selected.
