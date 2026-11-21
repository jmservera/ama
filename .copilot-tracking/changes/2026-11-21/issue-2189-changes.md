---
title: Issue 2189 changes
---

Changed: docs/reference/research/ci-critical-path-2189.md (new), docs/reference/README.md, docs/reference/log.md, plus RPI artifacts. No source or workflow change; tier: focused.

| Criterion | Status | Basis |
| --- | --- | --- |
| Source CI wall time under 15 min on a code PR | Unproven (not met today: 23.1 to 28.9 min) | Needs sharding and a hosted run after a push; push forbidden |
| No skipped test | Unproven | No change made; hosted skip count not retrieved; runtime skipTest calls exist |
| Required check names unchanged | Proven for current head | No workflow edit; names match observed runs |

Remaining work: implement 3-way api shard with aggregate `src-api` check and pip cache (full tier), then measure on a hosted PR.
