# Issue 79 live research, 2026-11-19

Research disposition: reused (prior 2026-11-18 live run with retained raw output) plus fresh local checks.
Planning Readiness: Ready (conclusion: no implementable-in-src criterion).

Unticked criteria:
* C3 named policy owner signs first rule order. Policy file `src/core/src/zava_forward/core/policies/` still has owner "to be named", status draft. A signature is a human act by a named person; synthetic signing would not satisfy it. Not provable for the demo.
* C4 snapshot publication scheduled and retained. Source already has the publisher (`core/ranking_publication.py`, `orchestrator/ranking_publish.py`), Blob archive and a Schedule-trigger job (`infra/modules/containerapps.bicep`, cron `30 2 * * *`), plus `rankingArchiveImmutabilityDays` (default 0). Remaining gaps are deployment: image carrying the module (ACR 403 on 2026-11-18), a deployed cron run, and a WORM policy with a Legal-decided retention. These are infrastructure/deployment items: FULL tier, forbidden by the brief to attempt under FOCUSED.
Fresh check: core ranking publication/runner/archive tests, 136 tests, OK (2026-11-19).
Evidence: docs/reference/research/issue-79-live-ranking-2026-11-18.md.
