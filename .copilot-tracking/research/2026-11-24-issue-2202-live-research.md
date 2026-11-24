---
title: Issue 2202 live research, 2026-11-24
description: Research for the remaining #2202 demo criteria on API 0000068 and resident 0000030
ms.date: 2026-11-24
---

## Disposition

Research executed. Planning Readiness: Ready.

## Evidence

* Issue #2202 has four unticked criteria; the 2026-11-22 comment records that generative AI answers are unproven (owner actions SUS-1 and budget expiry).
* Live apps on 2026-11-24: API `ca-cutover-test-demo-api--0000068`, resident `ca-resident-demo--0000030`, agents `--0000004`, all latest revision equals latest ready.
* Prior notes under `docs/reference/research/issue-2202-*` prove coverage (58.9% of 443 homes with readings, rev 0000058), consent checkbox, hardening, and earlier chat routing, chart and gauge probes on older revisions.
* Gaps to re-prove on current revisions: revisions Healthy, hardening on 0000068/0000030, sensor charts, map gauges, consent checkbox, chat routing, coverage. Image provenance and rollback exercise stay unproven (no drills).

## Plan input

Run read-only live probes with existing scripts, record a note with a per-criterion table, fix only a real defect found.
