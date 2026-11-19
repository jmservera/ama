---
title: Research for issue 73 live run (2026-11-19)
description: First unmet child criterion of epic 73 and its evidence
---

## Scope

Refs #73. Synthetic demo, desktop only. Epic criteria 1 to 3 are unticked; 1 and 2 are owner/checkpoint decisions (children 76, 79, 80 open), 3 is traceability.
Unticked child criteria: #76 hazard and safeguarding clock and named owner; #79 policy owner signature and scheduled snapshot publication; #80 owner-set thresholds.
Earlier passes ([r3](../../docs/reference/research/issue-76-live-r3-2026-11-18.md)) left #76 unproven: the live demo has 1 hazard case with unknown timestamps and no safeguarding item, and seeding would write demo data. #79 and #80 need named owner decisions, not code.

## Selected criterion

#76 "Hazard and safeguarding items show a clock and named owner".

## Finding

Local probe against the real server (`App` plus `make_handler`) on a synthetic dataset with one hazard (aware_at set) and one safeguarding item: `/api/cases` list rows and `/api/cases/{id}` carry `work.hazard_clocks` and `work.safeguarding_clocks` with named owner, elapsed hours and response state. No existing test asserts this on the list payload over HTTP (existing tests cover detail, Node rendering and core). Planning Readiness: Ready. Research disposition: executed.
