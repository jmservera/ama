---
title: Issue 1837 live demo, second pass research (2026-11-19)
ms.date: 2026-11-19
---

## Disposition

Reused. Prior evidence: `docs/reference/research/issue-1837-live-demo-evidence-2026-11-19.md` (target-size repair merged as 814789e9a). Base `adb10ae6d`.

## Findings

* Criteria 1 to 4 are already proven on source with real code and tests; nothing buildable remains.
* Criterion 2 live write: the demo API runs image digest `sha256:5368f4e4...` (revision 0000033). Whether it contains the fix cannot be shown without a redeploy, which is a production change the owner excluded.
* Criteria 5 and 6 need an independent exact-head reviewer, hosted CI and a full external receipt; `rpi-checks.py --all` is barred for this run.

Planning readiness: Ready (no source work).
