---
title: Research for issue 2243 live re-verification on resident revision 0000026
ms.date: 2026-11-22
---

## Disposition and readiness

Research disposition: executed (live read-only probes). Planning Readiness: Ready.

## Evidence

* Resident `ca-resident-demo--0000026` (23:14 UTC, Healthy, 100%) and API `--0000054`; resident env `ZF_DEMO_EXPIRES_AT=2028-01-01T00:00:00Z`.
* Playwright probe at 1440x900: both model-eligible questions return HTTP 200 with label "AI usage limit was reached"; console shows `reason=usage_limit` at 23:34:40 and 23:34:42 UTC.
* The label is the generic reason, so the guard refusal reasons are not visible: procedure not applied or image predates it (indistinguishable; registry firewalled, SQL private).
* Employee chat on API 0000054: model calls 0 (SUS-1 hold, issue 2245).
* Full findings: `docs/reference/research/issue-2243-rev26-2026-11-22.md`.

## Selected approach

Docs-only re-verification: note, probes, index and log. No source change, so the focused tier applies.
