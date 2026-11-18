---
title: Issue 202 live audit research
description: Research record for the archive tag and mvp/prototype deletion audit
ms.date: 2026-11-18
---

Research disposition: executed. Planning Readiness: Ready.

Scope: audit issue #202 unticked criteria (registry PR first, old workflows removed and required checks updated) against the repository, GitHub workflow state and rulesets. Demo only, desktop only. No Azure resource is relevant; none was touched. Raw outputs are in `docs/reference/research/issue-202-live-20261118T1643Z-evidence/`.

## Findings

* `mvp/` and `prototype/` have 0 tracked files; tag `v0.21.0` is published; registry has no legacy glob (#302, 2026-10-15) before deletion (#499, 2026-10-27).
* `mvp-ci.yml` and `mvp-validation.yml` remain, dispatch-only and `disabled_manually`; active ruleset `mainprotect` requires no status checks.
* Canonical note: `docs/reference/research/issue-202-live-20261118T1643Z-2026-11-18.md`.
