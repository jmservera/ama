<!-- markdownlint-disable-file -->
# Changes: issue-74-building-separation-0400 V2 documentary criterion mapping

Date 2026-11-13. Continues the same task after [V1 unit changes](issue-74-building-separation-0400-v1-unit-changes.md). Documentary only: no product, test or configuration edit, and nothing executed in this step. Original research, plan, details, critique (CR-001 High applicability, CR-002 Med unknown funding, CR-003 Med buildingView/heading wording) and the V1 records are unchanged and still stand. Not a release Pass, not closure, no criterion 2 tick.

## Attestation

* Worktree clean at 74daa587e; `origin/main` fetched 6f2918011d55d63ffc52865073ef45bd7ea9197c, equal to the product source. No product divergence.
* Unit outcomes quoted below come from the V1 run in the owned output directory `/home/azureuser/.copilot/session-state/2cbb371d-27a6-4609-9dc4-d25e657ce8fc/files/74-unit-verification-0408/` (core.log: 8 OK; api.log: 6 OK; zero skips; editables import this checkout; module hashes in the V1 changes record). The first API selector error and the pip missing-dependency recovery are preserved there.
* Browser worker rpi-74-browser-verification-0410 runs in a different worktree. Its work was not read or reviewed, and no pending outcome is inferred.

## Status vocabulary

* Executed-unit: a named maintained assertion that passed in the V1 run (payload or served script text; no rendering).
* Source-read: seen in source only, not run in this lineage.
* Rendered-executed: observed in a browser. None is claimed here; the original author-reported 24 stays historical and unverified by this lineage.
* Unobserved: neither read-confirmed nor run.
* Decision-gated: needs an owner decision or admission before any change.

## Criterion-term mapping

Source refs: `src/core/src/zava_forward/core/home_case.py` `view` (lines 119-175), `src/api/src/zava_forward/api/web/app.js` `homeCaseView` (about 1330-1360) and `buildingView` (1370-1411), server route `/api/buildings/` (server.py about 589).

| Criterion term | Side | Source | Named maintained assertion | Unit outcome | Status |
| --- | --- | --- | --- | --- | --- |
| Shared dependencies, holds, works | building | `view` returns `building` from `buildings.view` with `homes` removed; `buildingView` h2 Dependencies, Work stopped pending review, Shared works | core `test_shared_building_id_never_transfers_evidence_between_homes` (no `homes`, no home keys in `building`) | pass | Executed-unit for payload; panel and screen rendering Source-read, Rendered unobserved |
| Dependencies, holds, works absent from the home side | home | `home` block holds only decision, stage, closed, funding_confirmed, documents, quality, cost_allocation | same core test; API `test_view_separates_home_and_building_and_denies_unauthorised` | pass | Executed-unit (payload); home-panel DOM absence Unobserved here |
| Shared costs (building) | building | `building.costs`, `costs_restricted` | core same test (`12000.00`); `test_roles_and_finance_restriction`; API `test_finance_staff_get_building_cost_and_own_home_allocation_over_http`, `test_non_finance_staff_get_no_cost_amounts_over_http` | pass | Executed-unit for payload and restriction; buildingView cost section Source-read only |
| Home allocation | home | `home.cost_allocation`, `cost_allocation_restricted` | core same test (`6000.00`), `test_roles_and_finance_restriction`; API finance and non-finance tests (no amounts in body for non-finance) | pass | Executed-unit |
| Home evidence (documents, quality) | home | `home.documents`, `home.quality`, `links` | core `test_shared_building_id_never_transfers_evidence_between_homes` (sibling evidence and quality not shared), `test_version_starts_unrecorded_and_links_are_explicit` | pass | Executed-unit |
| Home decision | home | `home.decision`, `home.stage`, `home.closed` | API view test (`decision.status == Accepted`) | pass | Executed-unit |
| Funding | home | `funding_confirmed` is `True` only for explicit True | core `test_funding_confirmed_is_true_only_for_explicit_true`; API `test_absent_funding_reads_as_not_confirmed_not_missing_case` | pass | Executed-unit. The pass confirms the current mapping, which is the CR-002 limitation (missing or null reads as not confirmed). Unknown-funding display is Decision-gated |
| Outcome | home | no outcome field in `view` | none | n/a | Unobserved and Decision-gated: the outcome tuple has no approved definition; none is inferred |
| Home version history, notice, manual path | home | `versions`, `notice`; script strings | core versions tests; API `test_version_recorded_through_http_and_retained`, `test_screen_is_wired_with_manual_path` (script text only) | pass | Executed-unit |
| Per-home applicability of shared items | building | payload items carry `case_ids`, `package_ids`; `homeCaseView` does not render them, `buildingView` does | none in the two files | n/a | Decision-gated (CR-001 High, G5). Not repaired |
| Unknown vs known-empty shared categories | building | `buildingView` `category()` | none in the two files; core tests in `test_buildings.py` exist but were not run in this lineage | not run | Source-read |

## Limits kept

* The 14 passing unit tests cover payload and served script strings. They do not render the home or building screens, so the rendered separation is not established by this lineage.
* The original author-reported 24 browser PASS lines remain historical. This record does not confirm or deny them.
* buildingView execution, AT, axe, SQL, human acceptance, criterion 2 and the outcome definition are unobserved or gated. CR-001, CR-002 and CR-003 are not resolved.

## Proposal only: smallest future buildingView-route check

Need: the literal terms dependencies, holds and works on the building side are only rendered by `buildingView` at `#/building/<id>`. The home-case check navigates to `#/case-home/<id>` and reaches the building via a link but, per CR-003, no run observed `buildingView`.

Reusable by source, no new framework: `home_case_data()` and `run_browser(base)` in `src/api/checks/home_case_browser_check.py` and its `check` and `main` from `checks.design_system_browser_check` (synthetic dataset, loopback server, login, Playwright page); `building_fixture.fixture/open_store` and `App`/`make_handler` as used in `tests/test_home_case_api.py` (`login` via `/api/login` with `synthetic-only`); the existing `/api/buildings/SYN-B1` route; and `tests/test_buildings.py` for the payload.

Smallest option, read-only: one new navigation in that existing harness to `base + "/app#/building/SYN-B1"` as a Programme Manager, asserting the h2 text Shared systems, Dependencies, Work stopped pending review, Shared works, Shared building costs, and the Linked home cases links. No writes, no SQL, no provider or model.

Limitation, stated exactly: this cannot be done without adding at least one new assertion block to a browser check, which is new check source and needs a source grant. No existing check performs it. Existing `tests/test_buildings.py` can show the payload and cost restriction only if run, which is optional and already largely covered by the unit tests above. No defect or requirement is claimed; the check is needed only if the owner wants the criterion terms rendered-executed on the building screen. Admission is for the root to decide after the browser worker finishes.
