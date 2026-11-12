<!-- markdownlint-disable-file -->
# Details: five synthetic demo homes (2026-11-12, Refs #134 #184)

Task `five-home-script-134-1112`. Plan: [plan](../../plans/2026-11-12/five-home-script-134-1112-plan.md).

## Phase 1: runbook section

* Frontmatter `ms.date` to 2026-11-12; description extended with the five homes.
* New section "Demo Operating Mode And Five Homes (Owner-Selected Target, 2026-11-12)" after "Choose The Route Beforehand" so route choice precedes it:
  * Target-mode table: simulator start/stop, five homes, one reading per minute, Quality AI restricted to the same five, deterministic eligibility separate from paid analysis, operator-triggered analysis, eight-hour limit recommendation. Status column: OWNER-SELECTED TARGET or RECOMMENDATION; evidence column states source today (every open case, hourly home refresh; unverified).
  * Table of five homes: id, archetype, type, seeded stage, direct link to `<origin>/app#/case/<id>?tab=quality`.
  * Provenance paragraph: seed 20260901, as-of 2026-10-13, 980/443 match, selection rule, files.
  * Preflight list: ids exist, open, sensor readings exist, cohort lists them, effective AI scope evidenced as the five homes only before any trigger (else route E), sign-in/role, link opens the right tab; record Pass/Fail/Blocked/Not run.
  * Limits: not deployed acceptance; origin documented from 2026-10-31 observation, availability not claimed; link opens only after sign-in; the existing observed and blocked histories remain; no activation, model or spend grant.
* Route-L opening row unchanged.

## Phase 2: index, log, handoff

* Index: one pointer sentence after the demo-runbook mention in the capstone paragraph.
* Log: append entry; earlier entries untouched.
* Handoff JSON in the coordinator session files folder `files/134-five-home-script-1112/selected-five.json`: ids, provenance, links, status labels, limits.

## Validation (docs tier)

Relative link existence check, route regex check against app.js, `git diff --check`, forbidden-character scan (em dash), sensitive-content scan, `git status` clean after commit. No further generator replay (critique PC-002); no runtime or gate.
