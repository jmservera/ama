---
title: Issue 202 live changes
description: Changes record with per-criterion proven and unproven table
ms.date: 2026-11-18
---

Tier: focused (documentation and evidence only). Refs #202; no closing keyword.

## Files

* Added `docs/reference/research/issue-202-live-20261118T1643Z-2026-11-18.md` and its two evidence files.
* Edited `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).
* No `src/`, workflow, ruleset, Azure or GitHub-setting change; no throwaway resource created.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Rubric registry PR dropping `mvp/` globs merged first; dip recorded | Proven (ordering: #302 on 2026-10-15 before #499 on 2026-10-27; no dip recorded, 47 to 79); no measured score on the deletion commit | research note |
| `mvp-ci` and `mvp-validation` removed or replaced; required checks updated | Unproven in full: replaced by `src-ci`, files remain dispatch-only and disabled; active ruleset requires no checks; file removal is a full-tier workflow change not made | research note |
| Already-ticked criteria (prototype removed, tag, no tracked `mvp/` files) | Consistent with live repo and origin | research note |
| GitHub release (open owner decision, not a criterion) | Not published | `gh release list` empty |

Production-only items: none for the demo; the GitHub release and any repository-setting change are owner actions.
