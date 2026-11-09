<!-- markdownlint-disable-file -->
# Plan: issue-1294-validation-policy-priority-e1

* Task ID: issue-1294-validation-policy-priority-e1 (owner-authorized extra correction E1 of at most two; parent: issue-1294-validation-policy-correction-c4)
* Base: HEAD b085d7d3c (C4); origin/main b46a9ad9a9619db535368d1b2cbbddec8110e122 (merged locally, uncommitted at plan time)
* Research: .copilot-tracking/research/2026-11-09/issue-1294-validation-policy-priority-e1-research.md
* Details: .copilot-tracking/details/2026-11-09/issue-1294-validation-policy-priority-e1-phase-details.md
* Changes record (implementation owns): .copilot-tracking/changes/2026-11-09/issue-1294-validation-policy-priority-e1-changes.md

## Summary

Merge current main (clean), then make narrow wording corrections: retained sensor MSSQL local-only coverage and SQL-selection guidance in src/README.md, selected-tier wording in the rubric runbook, non-gate tooling in the instructions, append-only log. Then an independent static review of ALL current policy targets, a fresh proxy behavior simulation, final-head focused local checks, one Review, local commit(s). Focused tier: instruction and guide edits only, no workflow, tool, dependency, Dockerfile, permission, secret, deployment or security-control change (basis recorded; no blanket `--changed`).

## Decisions

* Tier classification: focused. Basis: only Markdown guides and instructions change; the merge brings main's tool change unmodified and is not authored here.
* Proxy labelling retained everywhere; no native or intended-profile claim.
* Never edit C1-C4 artifacts, retained sandboxes or earlier log entries.
* Cap: this cycle is E1; a defect that survives it may use E2, then stop.

## Phases

* P01 Merge origin/main into the topic (no conflicts expected; preserve both intents); verify tool/test diff is main's only.
* P02 Edit targets (G1, G4, G5; G2 only if a defect is found while editing).
* P03 Independent fresh-context static review of all current targets (G3); targeted closure when Revise.
* P04 Fresh proxy behavior simulation on the final state (G7) with finite cases.
* P05 Final-head local checks (G6), changes record, log append (G8), one Review, local commit; freeze clean.

## Acceptance

* AC-A Guide states retained sensor MSSQL suite is local-only with its exact contract and local selection rule, matching tools/rpi-checks.py and src-ci.yml.
* AC-B No current wording requires a blanket `--changed` run for small or documentation candidates; full tier retained for major, SQL, infra, deployment, security and releases; mixed takes stricter.
* AC-C Independent static review covers every target file; behavior simulation passes labelled proxy.
* AC-D Final-head checks recorded with commands, counts and exits; hosted CI recorded as unobserved.
* AC-E Original adverse evidence preserved; supersession recorded by append.

## Critique amendments (2026-11-09, after the single critique)

* P02 adds: coordinator step 8 sentence for focused candidates (PC-2); rubric steps 1 and 3 qualified by tier (PC-3); sensor selection stated for non-inert paths with a Markdown sensor-path probe (PC-4).
* P05 reordered (PC-1): commit the candidate and evidence, then run final-head checks, the one Review and the independent exact-head review on that SHA; a later edit invalidates and repeats them. The static review (P03) and behavior (P04) run on the edited tree before that commit and are re-bound by hash to the final head.
