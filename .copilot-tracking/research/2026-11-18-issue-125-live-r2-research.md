---
title: Issue 125 live re-audit research (r2)
date: 2026-11-18
---

## Scope

Refs #125. Re-audit of the three unticked criteria against the repo at 4fc9ff025 and the live demo
(ca-cutover-test-demo-api, resource group ama). Demo only, desktop. Prior merged note:
docs/reference/research/issue-125-live-discovery-assistant-evidence-2026-11-18.md (PR #1953).

## Disposition

Research disposition: executed (fresh live probes, static scan, offline tests, CLI demo).

## Questions

1. Does the live API still expose any discovery assistant route, read or write?
2. Do the offline tests and discovery-demo still behave as the prior note says, including the one environment failure?
3. Which criteria can the demo prove?

## Findings

* Live: every discovery path GET returns 403 and POST 404, identical to an unrelated control path; UI has no mention.
* Offline: 47 tests, 46 pass in user-site Python; 47 of 47 in a clean venv with `pip install -e src/core`. The earlier failure was an uninstalled package.
* CLI demo: DENY, deny-by-default, model_used false, comparison criterion_met false.
* All three criteria stay unproven for the demo; each is production-only.
Evidence: .copilot-tracking/evidence/2026-11-18/issue-125-live-r2/ and docs/reference/research/issue-125-live-r2-discovery-assistant-2026-11-18.md.

## Planning Readiness

Ready: plan is a docs-only evidence note, no src change, Tier FOCUSED.
