---
title: Changes for issue 195 live demo proof
ms.date: 2026-11-18
---

Refs #195. Tier: FOCUSED (documentation only). FULL tier is needed for triage draft D1 (SQL time status 500), which is not fixed here.

## Files

* docs/reference/research/issue-195-live-epic-evidence-2026-11-18.md, docs/reference/README.md, docs/reference/log.md.
* Dropped at independent review: the tools change for triage draft D2 (`tools/check-legacy-references.py` allowlist plus three `tools/test_*.py` edits). It changes gate semantics, so it needs the FULL tier and a separate candidate.

## Per-criterion table (issue 195)

| Unticked criterion | Result | Evidence |
| --- | --- | --- |
| Stabilization checkpoint (#440) completed | Partly proven | Triage note exists; D2 blocker has a candidate fix, held back as FULL tier; owner pivot or defer decision and issue filing not agent-provable |
| All child issues closed or deferred | Unproven | 4 of 11 closed, 7 open with unticked criteria, no owner deferral recorded |
| Deployed image rebuilt from `src/` and verified running | Running proven; provenance unproven | Revision `--0000031` Healthy and Running, `/healthz` 200; registry unreadable, ACR runs all Failed, no `src-deploy` runs; runtime banner exists only in `src/` |

## Validation

* Link and diff review of the documentation. No source or tools file changes in this commit, so unit tests, ruff and mypy do not apply.
* Before the tools change was dropped, `python3 tools/check-legacy-references.py` went from 30 to 19 violations on the working tree (observed; raw output not retained). At head of this commit the guard is unchanged and still reports the 30.
* Azure: read-only only; nothing created. Not run: `rpi-checks.py --all`, hosted CI (no push by instruction).
