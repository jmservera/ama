---
title: Plan for a fresh High-profile contained HVE simulation (issue 1204)
ms.date: 2026-11-06
---

Research: [research](../../research/2026-11-06/coordinator-hve-high-simulation-1204-research.md). Details: [details](../../details/2026-11-06/coordinator-hve-high-simulation-1204-details.md).

## Scope and tier

* One full fresh contained HVE simulation of the unchanged target blob acefb44a at inferred HIGH profile. No source edit, no native run, no harness, no schedule change, no reuse of the 25-case results.
* Validation tier FOCUSED (instruction/schedule validation; no runtime, infrastructure or security implementation). Checks: Markdown/diff, JSON state, link and evidence consistency, exact source/profile/containment readback. No SQL, browser, gate, scanner, image, build, install or deploy.
* Reassess upward only if a change touches runtime, infrastructure or security code (none planned).

## Phases

* [x] Phase 1: Research (committed before any dispatch).
* [x] Phase 2: Plan, details and one final-candidate critique, recorded in [critique](../../plans/2026-11-06/coordinator-hve-high-simulation-1204-critique.md). Committed before any dispatch.
* [ ] Phase 3: Implement the admitted validation: allocate new sandbox 2026-11-06-coordinator-behavior-005 and report 006 path; capture pre-run status; write run-state; dispatch designer; validate and persist design; execute every scenario through HVE Artifact Tester; write test-log; dispatch independent grader; persist review; write durable report; retain sandbox; write Changes; run focused checks.
* [ ] Phase 4: separate original author Review; commit the clean local frozen candidate.

## Stop and outcome rules

* A designer failure on gpt-5.6-sol: record the real error. Try the remaining canonical High models (Claude Opus 4.8, GPT-5.5) in order only if they are actual selectable options on the dispatch interface; do not guess model identifiers. If no High model runs, the skill proxy rule applies: a closest-available model labelled a proxy with no intended-profile claim, or else execution Deferred, verdict Not available, with a rerun condition. No repeated availability fishing.
* Executor profile check: before accepting executor evidence compare the returned model and profile with the passed High model; a mismatch or unresolved profile is recorded as a profile-resolution gap and the run is labelled proxy.
* Behavior or process failure: preserve, stop with Partial/Deferred/Blocked or a Revise verdict; no target repair and no extra correction cycle in this admission.
* Any out-of-sandbox write by a worker prevents Pass.
* Human-review checkbox is never ticked. No push, PR, merge, issue edit, history rewrite or cleanup.
