---
title: "Plan: issue 521 resident authority end"
ms.date: 2026-11-01
---

1. Replace the browser-check fixture constant with `rs.AUTHORITY_END` (single source).
2. Update `test_resident_demo_check.py` to prove 2027-02-01 applies and 2026-11-01 does not.
3. Add coordinator SQL/redeploy steps to `infra/README.md`.
4. Validate with focused tests, ruff, mypy. No Azure/SQL apply.

Critique (one pass): compatible; keep AI tariff expiry unchanged per "existing owner approvals unchanged". No divergence.

## Correction cycle 2026-11-01 (PR 690)

* Plan: git rm tracked egg-info (gitignore covers), fix apply command, require validated post-#590 image digest. Critique not repeated.

## Correction cycle 2 (PR 690, 2026-11-01)

* Merged origin/main (log.md kept both sides). Copilot thread: generated .ruff_cache, .mypy_cache and __pycache__ files were tracked; untracked them (already gitignored). ruff check, ruff format --check and the resident demo tests pass; mypy on touched files is clean (other errors are untouched, missing-stub/environment).
