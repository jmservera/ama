# Research: issue 80 entrypoint runtime check (diagnostic admission)

* Date: 2026-11-10
* Task: `issue-80-entrypoint-runtime-1110` (parent `issue-80-qualified-audit-1110`)
* Worktree and branch: `issue-80-export-entrypoints-runtime-1110`, `test/demo-export-entrypoints-80-1110`
* Pinned source: `583d4fbd58662e7ac9be71f5f2a8ae3021cd8078` (current main, clean at start)
* Research disposition: executed (partial runtime result, see Outcome)
* Planning Readiness: Ready for a plan that proposes, but does not implement, a driver correction and the Root decision
* Scope: bounded diagnostic admission. Not a source-correction allowance, not deployed, user or assistive-technology acceptance, and not a reset of earlier cycles. Criterion 2 ("Every list offers an Excel or CSV export; Excel stays one-way read-only"), criterion 4 (owner thresholds) and parent #73 stay open. The every-list criterion stays UNPROVEN.

## Questions

The merged supplement (`.copilot-tracking/audits/2026-11-10/issue-80-qualified-audit-1110-supplement.md`) lists nine located controls and three not located by static search: `packages.csv`, `workorders.csv` and `cases.csv?report=progress`. Grep absence is not UI absence. Root authorised one bounded local browser session for exactly:

1. Does the seeded staff capacity or packages experience offer a contextual reachable `packages.csv` export?
2. Same for the seeded staff work orders experience and `workorders.csv`.
3. Can server-seeded defaults or any rendered progress control produce `cases.csv?report=progress`?

## Source trace used to set up and read the checks

| Fact | Source at the pin |
| --- | --- |
| Both CSV routes exist and are registered list exports | `src/api/src/zava_forward/api/server.py:172-173` (`LIST_EXPORTS`), dispatch at 183-186 |
| `cases.csv?report=progress` is a server variant; only the keys `report`, `as_of`, `start`, `view`, `ready`, `capacity`, `duration`, `weeks` are accepted; `report` must equal `progress` | `server.py:528-552` |
| Server-seeded list defaults have no `report` key: `DEFAULT = dict(view="mine", q="", stage="", area="", flag="", sort="urgent", wave="", owner="", queue="")` | `src/core/src/zava_forward/core/taskqueues.py:11-13`, delivered as `me.work_queues.default` (`server.py:639`) |
| `listState` is seeded from that default minus `view`, written elsewhere only by the filter controls and the overview jump | `web/app.js:461-467`, 855, 863, 875, 1930 |
| The one `cases.csv` anchor is built from `view` plus `qs(listState)`; its `href` is assigned after the list loads | `web/app.js:807` (anchor), 845 (`csv.href = ...`) |
| The capacity screen is manager-only (`isManager()`: Retrofit Programme Manager or Programme Support Officer), reads `/api/packages` and `/api/workorders` through `pagedPath`, and renders create, capacity, work-order and pager controls | `web/ops.js` `capacityView` (352 onward), `web/app.js:444, 478` |
| The Package queue role screen reads `/api/packages` and `/api/workorders?case=` and is read-only | `web/role-screens.js:1058-1075` |
| The existing seeded fixture (one package, committed capacity, one work order WO-0001) | `src/api/checks/procurement_screens_browser_check.py` `procurement_data()` (WO id format `procurement.py:424`) |

The static trace therefore predicts: no `report` input exists in the default state and the only `cases.csv` anchor carries `view` plus filters. It does not predict what the capacity or Package queue screens render at run time, which is what the check was for.

## Execution record

Setup, all reusing existing patterns: owned venv `/tmp/ama-80-audit-venv-1110` (Playwright, Chromium 156.0.8078.4), existing harness `checks.design_system_browser_check.main` (owned scratch `ZF_BROWSER_SCRATCH=/tmp/ama-80-ep-scratch-1110`, `ZF_DATA` under it, `ZF_STORE=json`, loopback ephemeral port, password auth, no inherited credentials) and the existing `procurement_data()` fixture. The driver asserted before server start that `ZF_DATA` was inside the owned scratch and not under `~/.zava-forward`, and that the imported `zava_forward.api.server` was this worktree. Heavy admission: `flock -n /tmp/ama-rpi-heavy.lock`, no queue and no other holder touched. No dependency install was needed. The scratch directory was removed; no owned helper process remains.

Evidence directory: `ROOT/phase80-entrypoint-runtime-evidence-1110/` (driver, two run logs, observations).

| Run | Command exit | Outcome |
| --- | --- | --- |
| run1 (driver v1, `driver/entrypoint_driver.v1-failed.py`) | 1 | Driver defect: my `subprocess.Popen` guard also intercepted Playwright's own node launcher and raised `KeyError: 'ZF_DATA'`. The owned server had started and passed the loopback check. No page was opened. |
| run2 (driver v2, the one allowed disclosed repair: guard applies only to the server command) | 1 | Driver defect: after the first scan I read `href` immediately and got `None`, because `app.js:845` assigns it after the list loads. `TypeError` at my own `check(...)`. Stages after `T3-my-cases` did not run. |

The one allowed driver repair was used on run1. I did not make a second repair or a third run (no retry-until-green). Both failures are driver, not source or harness, failures, and both logs and drivers are preserved unmodified apart from the disclosed v2 edit.

## Observations (run2, partial, synthetic, owned, pam@example.test)

* Role `Retrofit Programme Manager`; `/api/me` `work_queues.default` keys are exactly `view,q,stage,area,flag,sort,wave,owner,queue` with no `report` (check PASS). This confirms the server-seeded default for the staff role in this scenario.
* `#/` (My cases today): one `a[download="cases.csv"]` ("Download for Excel"). Clicking it started a download of `http://127.0.0.1:<port>/api/cases.csv?view=mine&sort=urgent`, filename `cases.csv`, no `report` parameter. The scan read `href=null` because the attribute is assigned after load; the click ran after assignment and the captured request URL is the authoritative value.
* Page errors and non-GET requests after sign-in were not saved before the failure and are unknown.

## Outcome by target

| Target | Status | Basis |
| --- | --- | --- |
| 3 `cases.csv?report=progress` | Partial. In the default "My cases" state the server default has no `report` and the only `cases.csv` control downloads `view=mine&sort=urgent`. Not observed: `#/all`, the progress dashboard (with and without filters), the URL probes `?report=progress`, the overview, or the server route for the variant. | run2 above |
| 1 `packages.csv` | Not observed at run time. Static trace only: the capacity screen and Package queue screen read JSON; no CSV anchor located by static search; generic or dynamic construction is not ruled out. | no page for these screens was opened |
| 2 `workorders.csv` | Not observed at run time. Same static position. | same |

No UI defect is asserted, no UI absence is established, and no export control is shown to be reachable for targets 1 and 2. The three candidates remain unresolved. This is not a finding that the controls exist or are missing.

## Disclosures and skips

* Skipped by design: axe and accessibility review, any design change, Docker, SQL, the full gate, other browsers, other roles, and every register outside the three targets. The web guidelines review required for UI changes did not apply because no web file was reviewed or edited.
* `gh api user` was used read-only to resolve the commit identity. No GitHub mutation, push or fetch.
* Not run: the `server_routes` direct GET comparison and the `#/capacity`, `#/screens`, Package queue and `#/case/ZF-1` scans. These would only be interpretation aids (a direct GET does not prove UI reachability).

## Follow-ups (candidates, ranked)

1. Root decision: admit one further bounded run with the driver corrected at the exact points below, since the instrument, not the application, failed.
2. Only after real observations: if a control is absent in the observed scenario, propose the smallest fix through the existing route, role and data contract (see the plan).
