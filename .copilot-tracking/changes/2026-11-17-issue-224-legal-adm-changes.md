---
title: Changes for issue 224 evidence pack update
ms.date: 2026-11-17
---

## Changes

* `docs/reference/regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md`: added a dated 2026-11-17 readings section (reg. 5, AI Act as made, Regulation (EU) 2026/1744, ICO 403, remaining Unknown); earlier rows kept; ms.date updated.
* `docs/reference/research/rai/legal-briefing-adm-ai-act.md`: EU section, recommendation 5 and gaps updated; ms.date updated.
* `tools/test_adm_evidence_pack.py`: regression test (2 of 3 cases fail at baseline, all pass now).
* `docs/reference/README.md` index row and `docs/reference/log.md` entry.

## Validation (FOCUSED tier)

| Command | Result |
| --- | --- |
| `python3 tools/test_adm_evidence_pack.py` | 3 tests OK after; 2 failures with docs reverted (baseline measurement) |
| `ruff format --isolated --line-length 100 --check tools/test_adm_evidence_pack.py` | already formatted |
| `python3 tools/test_check_legacy_references.py` | 1 failure (`test_repository_has_no_violations`) identical with the change stashed; pre-existing, unrelated files |
| Link and diff review | relative links checked by reading; diff is docs plus one tool test |

Not run: `rpi-checks.py --all` (FULL tier not required; heavy lock held), mypy (no `src/` change), src test suites (no `src/` change).

## Amendments and divergences

None. Scope is not SQL, security, infrastructure or deployment.
