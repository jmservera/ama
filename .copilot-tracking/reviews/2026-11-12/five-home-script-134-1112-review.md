<!-- markdownlint-disable-file -->
# Review: five synthetic demo homes (2026-11-12, Refs #134 #184)

Task `five-home-script-134-1112`. Executed once, by the author (not independent). Boundary: the diff against base `d288b2a89` plus tracking artifacts. Independent exact-head Readiness review is still required.

* Execution: complete. Outcome: candidate complete with open items; no blocking defect found by the author.

## Assessment

| Area | Finding |
| --- | --- |
| Scope | Only runbook, index, log and tracking changed; no source, route, guard, telemetry or permission change |
| Ids | Five ids from a recorded local replay, rule stated, count match 980/443 reproduced; attributed as replay-selected, not independently verified, not deployed |
| Links | Route and tab verified against `app.js` line 412 and `case-workspace.js`; origin is the documented 2026-10-31 host; availability and sign-in limits stated |
| Honesty | Cadence, five-home scope, manual analysis, start/stop labelled OWNER-SELECTED TARGET; eight-hour limit a later recommendation; source scope noted as unchanged |
| Conventions | ASCII, `*` lists, no bold prefixes; frontmatter dates updated |
| Critique | One pass; PC-001..PC-004 applied |

## Open items (routed to later work, not corrected here)

* RV-001. Independent exact-head review, human approvals and hosted CI not yet done; hosted CI for this docs-only head unobserved.
* RV-002. Preflight needed on the chosen build: ids exist and are open, sensors exist, cohort lists them, effective AI scope is five homes.
* RV-003. Home 5 is at Funding check (weak Quality fit); the owner may prefer a different fifth home.
* RV-004. `src/api/README.md` still states every open case and hourly refresh; updating it belongs to the source lane.
* RV-005. The author used a Python text-replace for the index and log edits and ran two local replays before critique; disclosed in the changes record.
* RV-006. Log file has 17 pre-existing broken relative links in older entries, untouched.
