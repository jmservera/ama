---
title: Issue 203 guard live changes
ms.date: 2026-11-19
---

Refs #203. Focused tier: tooling only (`tools/check-legacy-references.py` exemption regex, `tools/test_check_legacy_references.py` two cases); no `src/`, workflow or gate change.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | `mvp/` and `prototype/` search returns only intentional references | Proven again: checker had regressed to 3 violations (date-first #202 note); fixed, checker exit 0 and 8 tests pass |
| 2 | Relative links resolve | Ticked; checker links 0 violations |
| 3 | Index and log updated | Ticked; no knowledge-base file changed here |
| 4 | Rubric comparison | Ticked |
| 5 | Deployed app and CI green from `src/` | Unproven: needs digest provenance and a `main` push CI run (owner action, see `issue-203-live-recheck-2026-11-19.md`); no new live evidence gathered |

Validation: `python3 tools/check-legacy-references.py` exit 0; `python3 -m unittest tools.test_check_legacy_references` OK (8); `ruff format --isolated --line-length 100 --check` and `ruff check` clean. mypy not applicable (tools are not a `src/<project>`).
