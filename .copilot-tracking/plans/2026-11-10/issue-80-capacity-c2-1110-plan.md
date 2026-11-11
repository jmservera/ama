---
title: Issue 80 capacity browser check aftercare route, plan
description: Plan to add the aftercare manager route with an asserted read-only denial boundary (correction C2)
ms.date: 2026-11-10
---

Research: [research](../../research/2026-11-10/issue-80-capacity-c2-1110-research.md). Details: [details](../../details/2026-11-10/issue-80-capacity-c2-1110-details.md). Critique: [critique](issue-80-capacity-c2-1110-critique.md).

## Objective

Let the whole `capacity_browser_check --axe` pass the manager navigation loop at `#/aftercare` by covering the route and asserting its intended 403, so the empty-capacity assertion can be reached. Checker file only.

## Phases

* [ ] Phase 1: edit `capacity_browser_check.py` (route entry, expected-denial capture, route assertions).
* [ ] Phase 2: focused validation at exact head, then ONE whole browser run.
* [ ] Phase 3: reconcile records, native review, commit, new continuation handoff.

## Decisions

* The allowlist is a request listener adding a request to `expected_failures` only when scenario is `#/aftercare`, method GET, URL exactly `<base>/api/aftercare/form`. A response recorder stores the status of every such request.
* On the route: exactly one recorded response, status 403, JSON error equals "Your role cannot record a concern. Ask a colleague who can."; page shows the "cannot record" status line, no `#ac-form`, no submit button; no POST occurred during the route.
* A 200 or a missing denial fails the count/status assertion. All other statuses, paths, methods, page errors and console errors stay fatal.
* Route entry: heading "Aftercare concerns", endpoints `/api/aftercare/concerns` and `/api/aftercare/evaluator` (existing 200 GETs), content `#app section[aria-labelledby='ac-list-title']`.
* One run; failure or busy is reported as found; no retry, skip or weakening.

## Validation tier

Focused demo; checker-only change. Independent exact-head review still required.
