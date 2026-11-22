---
title: Issue 2202 deploy proof research
date: 2026-11-22
---

# Research

Goal: prove six merged fixes live on API revision ca-cutover-test-demo-api--0000051 and resident ca-resident-demo--0000023 (main a6c0910c9). Disposition: executed. Both revisions confirmed Running and Healthy (resident RunningAtMaxScale).

## Findings

* Hazard clocks (#2255): backfill already applied live; 22 hazard cases show hours elapsed, target and owner; the 23rd case is safeguarding with its own clock and named owner. No re-run needed.
* Safety count (#2254): tile 23, map 23 safety markers, list 23, API total 23.
* Chart (#2253): text and circles correct.
* Handoff waiting (#2256): 4 rows including ZF-2025-0030, due Unknown.
* Map: 443 markers in 3.3 s; sensor states fresh 58, stale 1.
* AI: employee chat answers by rules because an open all-scope suspension from 2026-11-18 ("Demo probe: negative test") holds AI work; the #2245 disclosure reports it. Resident app reports "AI usage limit was reached"; `resident_ai.reserve` allows 5 attempts per resident per hour and 2000 in total, so the hourly window is the probable cause. Polling for a window.

## Decisions

Lifting the suspension is a named-human governance restart (reject_automatic_restart); not done here.

Planning Readiness: Ready.
