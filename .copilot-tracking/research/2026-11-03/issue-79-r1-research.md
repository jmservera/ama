---
title: Issue 79 research, deterministic home ranking
ms.date: 2026-11-03
---

## Research disposition: executed. Planning readiness: Ready

Evidence (repository at origin/main b855aec86):

* Delivered by earlier merged work (#36, #41, #697): `src/core/.../ranking.py` (pure `rank`, `snapshot`, hash-checked `load_policy`, registry of versions), `policies/ranking-v1.json`, `/api/ranking/snapshot`, reasons on cards, golden tests in `src/api/tests/test_ranking_policy.py`. No merged PR names #79 directly.
* Criteria 1 and 2 are met and tested. Criterion 3 needs a named human owner: not creatable by an agent. `ranking-v1.json` says owner "to be named".
* Criterion 4 gap (ADR 0002 snapshot table, status row line 1077): snapshot is one overwritten file per version, no dated retained archive, no schedule contract.
* Retention period is a Legal decision (ADR 0002 line 440), so it must not be set here.

Slice 1 (this PR): retained, verifiable snapshot archive plus schedule contract. Later slices: wire a scheduler (deployment, gate tier), SQL `ranking_snapshot` table (SQL, gate tier), owner sign-off (human).
