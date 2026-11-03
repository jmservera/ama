---
title: Issue 93 R1 RULE-010 boundary research
ms.date: 2026-11-03
---

Disposition: executed. Planning Readiness: Ready.

## Prior delivery checked first (do not redo)

* #94 and #95 are closed. Merged PRs #383 (record-only finance matching, independent approval), #386 (grant lifecycle evidence, scoped human authority), #510 (working form reviews, held authority), #377 (form schemas, staging), #657/#785/#862 (finance screens) already delivered `finance.py`, `grants.py`, `funding_step` and the finance screens in `src/`.
* Open children: #96 (open PR #902), #98 (open PR #888), #99 (open PR #885). Not touched here.
* #440 (stabilization checkpoint) is open; its triage and artifact criteria are unmet. Not claimed here.

## Epic criteria status

* Criterion 1 (checkpoint #440 before closure): unmet.
* Criterion 2 (all children closed or deferred): unmet; #96, #98, #99 open.
* Criterion 3 (no automated path submits a bid, approves match funding, certifies a claim or records cash): existing per-feature tests prove human authority for each path, but no single boundary test covers RULE-010 / AC-035 across callers.

## Evidence for the slice

* BRD RULE-010 and AC-035; CON-006 (Finance submits applications).
* `grants.py`: state flow ends at Cash received; approval needs a different human and `grant:<state>` designation. `store.funding_step`: approve, submit, confirm need `application:<action>` designation.
* The only caller of `grant_action`, `finance_action` and `funding_step` is the authenticated route in `api/server.py`. `funding_draft` (AI) only writes a draft and moves status to "Draft ready".
* No match-funding approval action exists in `src/`.

## Smallest coherent slice

A focused boundary test in `src/core/tests` that ties the four RULE-010 actions to proof: per-state designation matrix, AI draft cannot advance the application, agent and automation code cannot reach the gated methods, finance and grant modules have no outbound client. No production code change.
