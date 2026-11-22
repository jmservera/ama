---
title: Issue 1258 live changes
ms.date: 2026-11-22
---

No source change. Tier: focused. Added the research note `docs/reference/research/ranking-archive-ancestor-durability-evidence-2026-11-22.md` and RPI artifacts.

Validation: from `src/core`, `PYTHONPATH=src:tests python3 -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner -q` ran 110 tests, OK.

| Criterion | Status | Basis |
| --- | --- | --- |
| Pre-created archive or sync of new ancestors before confirming | Proven (already ticked) | `_confirmed` syncs the archive folder and opened parents; test at test_ranking_publication.py:320 |
| Post-link sync failure is `committed_unconfirmed`, record kept | Proven (already ticked) | test at :334; 110 tests pass |
| Syscall-order regression, failing before fix | Partly proven | Tests exist and pass; failure before the fix was not re-run here |
| Retry, private stage, audit, 409/503, original date intact | Proven (already ticked) | runner and publication suites pass |
| Original RPI | Proven | these artifacts |
| Current FULL receipt and verification | Unproven | no source change; full gate not run for the demo |
| Independent exact-head review | Unproven | needs a separate human or agent review of the pushed head |
| Hosted checks | Unproven | no push or PR permitted |
| No real crash or live filesystem claim | Upheld | mocked syscall tests only; nothing claimed |
