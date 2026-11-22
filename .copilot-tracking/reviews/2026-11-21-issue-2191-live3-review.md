---
title: Issue 2191 live pass 3 review
ms.date: 2026-11-21
---

Refs #2191. Review executed once after implementation. Outcome: conformant with open items routed to later work.

## Findings

* The cap change is one constant used in all four places; the new test fails without it and passes with it. No other caller depends on 100.
* `failureRate` defaults to `'0'`, so existing deployments are unchanged.
* Records match the live readbacks: 222 of 443, 111/111, hub slots 192, 207, 196.
* No credential, key or token appears in any artifact; temporary roles read back as 0 and throwaway jobs are gone.

## Routed follow-ups

1. Rebuild and push the image so the deployed code carries `MAX_CONTROLS` (registry window needed).
2. Observe a full receiver window at 222 homes (issue 2201).
3. Rebuild the cohort if the home count grows past 448 or the certificates reach 14 days.
