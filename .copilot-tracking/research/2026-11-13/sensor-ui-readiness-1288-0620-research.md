# Research: retained sensor value and Quality UI grounding readiness (2026-11-13, Refs #1288 #111 #110)

Disposition: executed (bounded, about six minutes). Docs-only; no source, test, runtime, SQL, cloud, provider, Docker, .env, private data, issue, push or AC change. Branch `research/demo-sensor-ui-readiness-0620`, base `origin/main` `15bfee2d7`.

## Pin and inputs read

* HEAD `15bfee2d7`, clean worktree. Live issue bodies and the last six #1288 comments read 2026-11-13.
* Source and tests read only for the literal #1288 ACs: `src/core/src/zava_forward/core/sensor_view.py`, `src/api/src/zava_forward/api/web/ops.js` (retrofit text), `src/api/tests/test_quality_sensors.py`, `test_quality_sensors_e1.py`, `test_quality_sensors_e2.py`, `test_quality_sensors_c7.py`, `src/api/checks/quality_sensors_browser_check.py`; prior `.copilot-tracking/research/2026-11-10-sensor-actual-main-440-1110-research.md`.
* Not found: ROOT `demo-run-ledger.md` is not present under `/home/azureuser/source/ama`, `/home/azureuser/source/ama-demo-wt` or this worktree (searched to depth 4). The ledger was therefore not read; this is a reading limit, not a finding.
* Out of scope and not reopened: B1 delivery (`1473`/`bbb1d20cc`), unmerged minute-v2 five-home `e904`, `44bd` disposition, `74` scoped parent `b9`, `184`, c71/H4.

## AC mapping for #1288 (source and test evidence, not acceptance)

| AC | Finding |
| --- | --- |
| 1 bounded read model, IDs, units, UTC, freshness, provenance | Implemented (#1331): `sensor_view.py`; tests for bounds, units, UTC, key reads, no generation, role matrix. Implemented-unverified on real SQL Server for skips. |
| 2 UI shows values and pre/post context or states it is missing | Implemented. Values shown; missing context stated explicitly (`retrofit_context.available` false, "No installation date", `before_absent`/`after_absent`). AC allows the missing statement. |
| 3 AI snapshot consumes identical IDs and values | Implemented: `test_same_ids_and_values_reach_model_and_proactive_flag`, citation and invalidation tests. |
| 4 durable deduplicated model-attributed proactive flag, bounded | Implemented: bucket, throttle, restart, A-B-A, in-flight tests (c7, e2). |
| 5 employee sees finding, cited IDs, time, model, unapproved status | Implemented locally; browser check exists (fixture, local engineering evidence). |
| 6 explicit insufficient/blocked/unavailable states | Implemented: fail-closed, consent, unavailable-model tests. |
| 7 focused SQL/API/browser tests | Implemented; SQL partially qualified (H0 one FAIL, H1 context unproven per #1288 history). Not a new local slice. |
| 8 separately admitted live walkthrough | Pending cloud, release, cost and owner admission. Not local. |
| 9 #91 controls and Fluent/native semantics intact | Implemented-unverified; human WCAG acceptance pending. |

#111: reproducibility and R1 to R3 research remain open and are method and human approval gated. #110: real Hub identities and live acceptance remain open (cloud, owner decisions). Neither has a local initial slice that is not already delivered or blocked.

## Candidate considered and rejected

* Retained pre/post-retrofit context. No installation date or marker exists anywhere in `src/core/src` or `src/api/src` (grep of installation date, installed on/at returned only the explicit "not recorded" wording). Supplying one needs a new retained data field and schema/SQL decision, which is outside the allowed local-only, no-SQL lane and is not required by the AC because explicit "missing" is acceptable.

## Determination

No independent INITIAL local retained-value or UI-grounding increment is genuinely missing. Everything local is delivered or implemented-unverified; the rest is qualified pending input (owner/human, cloud, SQL execution via #1297/#1298, dependency #184/#185/#188/#189). No ready slice, so no plan, tests, or surface is proposed. Reusing prior identical pin evidence, this lane stops; historical repeat is not authorised without a new pin, an owner-supplied retrofit marker source, or cloud/SQL admission.

Planning Readiness: Not ready (no slice). Next action: none locally; wait for one of the three triggers above.

## Limits

* Roughly six minutes; ledger not located; no tests run; backlog-manager route and independent Review not executed within budget (see state record). Unknown history is not zero.
