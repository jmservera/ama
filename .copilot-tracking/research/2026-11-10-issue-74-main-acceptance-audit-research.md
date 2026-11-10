# Issue 74 current-main acceptance audit: research

Date: 2026-11-10. Task: `issue-74-main-acceptance-audit`. Parent: #73.
Branch `docs/demo-home-separation-audit-74-1110`, worktree `issue-74-home-separation-audit-1110`.
Research disposition: executed. Planning Readiness: Ready.

## Scope and root direction

* Root selects a source-bound acceptance audit of the single unmet criterion of #74: "Building-level dependencies, holds, works and costs are shown apart from each home's evidence, decision, cost allocation and outcome". Criteria 1, 3 and 4 stay ticked and are not re-audited.
* Not in scope: feature reimplementation, source/test/fixture/criterion edits, a new five-cycle grant, a broad UI or conformance audit, runtime approval, any issue write, push or PR.
* Evidence classes are kept apart: constructed local fixture behaviour is not real customer, human, assistive-technology (AT) or live acceptance.

## Pinned identities (read-only, 2026-11-10)

| Item | Identity |
| --- | --- |
| Resolved current main | `c66370042eb08f07839d054433f4483078703cf2` (`chore(rubric): record score 78/100`, committed 2026-11-10T15:16:41Z); fetched `origin/main` equals local HEAD; HEAD is an ancestor of `origin/main` |
| Tree | `9f2e4cfbffa11b84ae3b0eb7b0fa1560b6a25137` |
| Candidate worktree | clean at research start; base equals current main |
| Home case core | `src/core/src/zava_forward/core/home_case.py` blob `00914209f8e5e4b890043b70cbcda12ceb9a757a` |
| Building core | `src/core/src/zava_forward/core/buildings.py` blob `7428f4d809dab5b78861f5f2bd1e3ec9f20cb6ea` |
| API server | `src/api/src/zava_forward/api/server.py` blob `b2435761c00d098352b061c913a5d78ee5a4e961` |
| Screen | `src/api/src/zava_forward/api/web/app.js` blob `c735acad6350f18353df80187e32ac1640a7c80f` (`homeCaseView`) |
| API test | `src/api/tests/test_home_case_api.py` blob `2ed3d4b8dc5b3c1842e5a004d4df5177f16fafe3` |
| Browser check | `src/api/checks/home_case_browser_check.py` blob `811d4b5222dfbc2243183418a36954a7825ec773` |
| Core test | `src/core/tests/test_home_case.py` blob `ebae688784964117ce76c3a735228d6ec4ab10fe` |
| Fixture | `src/core/tests/building_fixture.py` blob `12c522dc3be59664bd7a0546d37f52d1e44b40ff` |
| Browser runner | `src/api/checks/design_system_browser_check.py` blob `ffc6a7498446f105bff68a1924b200687ebd188a` |
| PRD | `docs/prds/zava-forward-retrofit-programme-demonstrator.md` v0.21.0, status `in-review`, ms.date 2026-10-25, blob `c788b917bafaede215f326f0efc71e071a687f1c`; FR-001, FR-002 (lines 1376-1377), AC-001/002/003/043 |
| BRD | `docs/brds/agentic-retrofit-programme-brd.md` v0.21.0, status `draft`, ms.date 2026-10-24, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; NFR-002 (line 1596, AC-049) |

PRD FR-002 is the literal source wording of the criterion: building-level shared systems, dependencies, holds, works and costs separately from each home's evidence, decision, cost allocation and outcome, and a shared building ID alone neither establishes package applicability nor transfers a home-specific gate. PRD and BRD are not approved baselines (`in-review`, `draft`), so they cannot by themselves establish human acceptance.

## Prior PR and issue history (gh read-only)

* #907 merged 2026-11-03 (`f13cb64c0`): core versioned home case, links, retained versions; `home_case.py`, store hooks, `test_home_case.py`.
* #1038 merged 2026-11-04 (`d9a8de2f1`): API `GET /api/cases/{id}/home-case`, `POST .../home-case-version`, `#/case-home/{id}` screen.
* #1177 merged 2026-11-04 (`deacc9f6e`): `home_case_browser_check.py` and screen tweaks.
* Issue comments: 2026-11-04 and 2026-11-05 audits; 2026-11-09 two session-local replays on `b46a9ad9a9619db535368d1b2cbbddec8110e122` (maintained check, then a separate populated two-home probe). Their raw logs were never independently archived and the probe script is session-local and not maintained. They are not re-used as evidence here; they define what this audit must confirm on a different pinned main.
* Backlog ready-refinement 1903 found the implementation in an unpinned primary source and could not prove current-main ancestry or complete cost/outcome semantics. This audit pins both.

## Parent #73 and durable store

* #73 (Epic: Home case and role-based workbench) is OPEN, `status:partially-delivered`. Open epic status is not evidence that the implementation is absent. The implementation is source-qualified here: `HISTORY = "home_case_versions"` is carried by the case record and the JSON `Store` and `SqlStore`; `test_home_case.py` replays both stores and a SQL reopen (`test_versions_survive_reopen`).
* The durable-store dependency in #74 is "platform epic": not asserted complete or approved here. Hosted SQL Server, Azure and live-store behaviour are out of scope and stay unknown.

## Source behaviour (static read at pinned blobs)

Projection `home_case.view` (staff roles only, else `PermissionError`) returns `home` and `building` as separate keys:

* `home`: `decision`, `stage`, `closed`, `funding_confirmed`, `documents` (id, name, kind), `quality` (measure, state), `cost_allocation` (null plus `cost_allocation_restricted` for roles outside `FINANCE_VIEW`).
* `building`: `buildings.view` output with `homes` removed: `systems`, `dependencies`, `holds`, `works`, `costs` (removed and `costs_restricted` set outside `FINANCE_VIEW`), `version`, `source`, `notice`. Missing or invalid building record yields `{id, status: Unknown}`.
* Staff roles: Retrofit Coordinator, Resident Liaison Officer, Building Safety Liaison, Grants and Evidence Officer, Quality Inspector, Retrofit Programme Manager, Programme Support Officer. Finance view: Grants and Evidence Officer, Retrofit Programme Manager, Programme Support Officer. Contractor and anonymous are refused (403/401 at the API).
* Per-home "outcome" has no single field. The screen renders `stage`, `closed`, `funding_confirmed`, and `quality` states. This is a semantic mapping to confirm, not assume.

Screen `homeCaseView` renders two labelled `section` regions: `hc-home` ("This home only: evidence, decision, cost allocation and outcome") with Evidence documents, Quality outcomes, Decision, Cost allocation; `hc-building` ("Shared at building level, not this home's evidence") with Shared systems, Dependencies, "Work stopped pending review" (holds), Shared works, Shared building costs. Building items are rendered as `id: label`, status, source. Items are not filtered by their `case_ids`/`package_ids`; applicability scoping is not displayed on this screen (applicability is enforced in `buildings.blockers`, not here).

## Maintained coverage and static gap hypotheses

| Check | Fields and roles it can positively observe |
| --- | --- |
| `test_home_case.py` (core, JSON and SQL stores) | ZF-3 populated: building `costs[0]` 12000.00 and home `cost_allocation[0]` 6000.00; building has no documents, quality, decision or cost_allocation keys; sibling document and quality absent from ZF-2 links; finance restriction for Resident Liaison Officer; Contractor refused. No systems, dependencies, holds, works values (fixture has empty dependencies and holds). |
| `test_home_case_api.py` (HTTP) | Retrofit Programme Manager only for 200s: `home.decision.status`, `links.building_id`, no `homes` key, notice. Contractor 403/401. Not asserted over HTTP: cost allocation or building costs values, non-finance restriction, building systems/dependencies/holds/works. Source-text test for static strings in `app.js`, not rendering. |
| `home_case_browser_check.py` (Playwright, ZF-2, Retrofit Programme Manager only) | Region tokens: DEP-1, HOLD-1, WORK-1, GBP 12000.00 only in building region; "Decision: Accepted", "Stage:", "GBP 6000.00" in home region; sibling tokens absent from `main`; read-only; reflow; optional axe; no writes. Not asserted: SYS-1 or "Shared ventilation" (systems) placement, home evidence document and quality outcome populated (ZF-2 has no quality; ZF-3 never opened), restricted-cost rendering for a non-finance role, building version. |

Hypothesised gaps (to be confirmed by the actual runs, not fixed): (G1) shared systems not asserted in either region; (G2) home evidence documents and quality outcome never positively asserted in maintained browser coverage; (G3) non-finance restricted-cost rendering not covered in browser or HTTP; (G4) HTTP does not assert building or home cost values; (G5) no maintained coverage opens a second home view in the browser to show the per-home split on the same building; (G6) region tokens prove containment of listed tokens only, not that each building item type is a separate semantic heading.

## Execution constraints discovered

* Runner `checks.home_case_browser_check` imports `checks.design_system_browser_check.main`, which derives `ROOT` from its own file path (`parents[3]`), adds `src/core/tests` to `sys.path`, and builds `PYTHONPATH` for the server from `ROOT/src/*/src`. It accepts `ZF_BROWSER_SCRATCH` (absolute, outside the checkout) so a short, task-owned scratch path avoids the known Unix-socket length issue and the legacy `.venv` write in the checkout. It must run from `src/api` (`python -m checks...`). Server env passes only PATH, HOME, LANG and bytecode variables, no credentials. Data is built from `home_case_data()` into a temporary synthetic JSON, never the default `ZF_DATA`.
* `playwright` is not importable in the system Python; Chromium revision 1248 is cached under `~/.cache/ms-playwright`. `src/api/pyproject.toml` declares `playwright==1.64.0` as a dev extra. Install into a task-owned venv only (actual missing dependency).
* Heavy-lane lock: `/tmp/ama-rpi-heavy.lock` with non-queued `flock -n`; a busy lock stops the browser check, with no wait, queue, spin or kill.
* Witness helper `issue-1300-phase-1110/tools/rpi_phase_witness.py` has seven events (launch, research-open, plan-done, implement-start, implement-done, review-done, commit-complete); `launch` is recorded (seq 1) with an external evidence directory.

## Planning readiness

Ready. Remaining unknowns (to be resolved by execution, not by assumption): whether pinned-main API and browser checks pass in an owned environment; which gaps G1-G6 are confirmed; the status of each field (local-observed, implemented-unverified, blocked, unknown).

## Follow-ups (current)

1. If gaps are confirmed, a separate user-selected issue/PR to add maintained assertions (out of scope here).
2. Manual keyboard and screen-reader review of `#/case-home/{id}` by a human (not performed here).
3. Source-qualified durable-store (SQL Server) acceptance, owned by the platform epic.
