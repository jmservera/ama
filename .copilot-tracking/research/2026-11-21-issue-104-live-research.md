---
title: Issue 104 live research (2026-11-21)
ms.date: 2026-11-21
---

Refs #104. Research disposition: executed. Planning Readiness: Ready.
Scope: synthetic demo, desktop only, head 981aa6aaf. Unticked: C1 (#440 stabilization checkpoint), C2 (all child features closed or deferred). The invariant criterion and both tokenomics criteria are ticked.

Findings (REST reads, 2026-11-21):

* Children #105, #106, #432 CLOSED. #164 and #216 (the other 2026-11-19 gaps) are now CLOSED. #107 OPEN with no unticked criteria. #108 OPEN with one unticked criterion (model names, versions and quotas in the chosen region). #435 OPEN, a story with three owner decisions, not a child feature.
* #440 OPEN with two unticked criteria (triage with owner approval; delivered PR artifacts and HVE Builder validation). No open `bug` issue.
* Azure read-only: revision ca-cutover-test-demo-api--0000038, digest prefix bc5cb9ae. Foundry account aif-cutover-test-rzsrg (uksouth, S0) holds deployments `standard` (gpt-4.1-nano 2025-04-14, GlobalStandard, capacity 10) and `resident-mini` (gpt-4.1-mini 2025-04-14, Standard, capacity 1), both Succeeded. The quota usages API (CLI and REST) returns an empty list for uksouth, as in #2014.
* Offline: 59 tests OK (epic 104 invariants, candidate comparison, held-out freeze).
* No defect found, so no src change.

Evidence folder: .copilot-tracking/evidence/2026-11-21/issue-104-live-20261121T081349Z/.
