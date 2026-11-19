---
description: Research for issue 202, first unticked criterion (remove mvp-ci and mvp-validation, update required checks)
ms.date: 2026-11-19
---

Disposition: executed. Planning Readiness: Ready (outcome is a stop, not a build).

* Only unticked criterion: "Old workflows (`mvp-ci`, `mvp-validation`) removed or replaced, and branch protection required checks updated".
* Raw evidence: docs/reference/research/issue-202-live-20261119T154854Z-evidence/workflows-and-protection.txt.
* Both files exist, `workflow_dispatch` only, `disabled_manually`; active ruleset `mainprotect` requires no checks; classic protection 404.
* Removal touches 13 files including pinned SHA-256 workflow hashes in `tools/rpi-checks.py`, `src-ci.yml` paths and actionlint step, and `src/core` cutover audit. That is a gate-semantics and workflow change: FULL tier, which this run cannot satisfy (no `--all`).
