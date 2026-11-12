---
title: Issue 149 UX parent integration plan details (2333)
description: Exact manifest, dependency graph, ownership, merge order, invariants and canonical checks for the prospective UX parent assembly; planning only
ms.date: 2026-11-12
---

## 1. Module and test manifest (exact pins)

| Input | Head | Modules touched | Tests that must pass at the assembled head |
| --- | --- | --- | --- |
| 1490c | `ff40e50c8` | `src/core/.../store.py`, `home_case.py`, `chat_case_answers.py`, `taskqueues.py`; `src/api/tests/test_home_case_api.py`, `test_mvp.py`; core tests `test_gates`, `test_home_case`, `test_chat_case_answers`, `test_sqlqueues`, `test_taskqueues` | `test_only_explicit_true_reads_as_confirmed_funding`, `test_only_explicit_true_reads_as_ready`, `test_unconfirmed_funding_reads_as_denied_with_reason`, `test_funding_confirmed_is_true_only_for_explicit_true`, `test_non_boolean_funding_refreshes_stale_revision_two_memberships`, `test_only_explicit_true_funding_clears_the_final_checks_blocker`, `test_absent_funding_reads_as_not_confirmed_not_missing_case`, `test_stale_advance_refusal_names_case_owner_and_next_action`, `test_advance_with_missing_funding_is_a_funding_conflict_not_a_missing_case` |
| 74 | `467a0cf5d` | `src/api/checks/home_case_browser_check.py`, `src/api/tests/test_home_case_api.py` | `test_non_finance_staff_get_no_cost_amounts_over_http`, `test_finance_staff_get_building_cost_and_own_home_allocation_over_http`, `home_case_browser_check` (24 PASS, pinned axe 4.10.3) rerun because `home_case.py` changed |
| 176 | `da436be3e` | `src/core/tests/test_generated_dataset.py`, runbook, retrofit-synthetic-data README, `log.md` | `test_runbook_five_home_table_parser_rejects_malformed_tables`, `test_runbook_five_home_cohort_is_reproduced_by_seed_and_as_of` |
| 134 | `cc7e3c3a9` | `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` (docs only) | none executable; namespace and static docs checks, link and diff review |
| 215 | `6eacb4953` | `src/api/README.md`, `regulatory_ux_check.py`, `chat.js` | `regulatory_ux_check` (21 states), chat.js and regulatory modules, `node --check` |
| 233 | `aebd381d9` | `log.md`, `atlas-screen-trace.md`, `programme_paging_browser_check.py`, `role-screens.js`, `test_programme_screen.py` | `test_every_queue_row_opens_its_connected_view_by_a_read_only_link`, `test_queue_page_two_links_use_the_scope_that_filtered_the_rows`, `programme_paging_browser_check`, `role_screens_browser_check 230` |
| 96 backend | `94760af7d` | `server.py`, `src/api/README.md`, `test_form_held_download_api.py`, `test_role_endpoint_inventory.py`, depends on main `form_export` (#98) | the ten Held-download methods named in the research file, `test_form_export`, `test_role_endpoint_inventory` |
| 96 UI | not frozen | `role-screens.js` (`fundingDraftPanel`, about line 1346), Held download browser check | defined by its own plan; accepted frozen head required |

## 2. Dependency graph (actual)

* main (`8e6e55457`) is merged first; every input is based on an older main commit and needs no content from siblings except as listed.
* 1490c depends on the parent (1487 squash). 74 depends only on main plus the shared test file (no code dependency on 1490c, but its tests exercise `home_case.py`, so they run after both).
* 134 has a text overlap with main (#1492) only.
* 96 backend depends on main #98 `form_export`; 96 UI depends on 96 backend (same parent).
* 233 depends on main #1492 (its base). 215, 176, 74 have no sibling dependency.
* No input depends on 1490c semantically except that every funding reader must stay strict.

## 3. Ownership and overlap

| Path | Owners | Rule |
| --- | --- | --- |
| `src/api/tests/test_home_case_api.py` | 1490c, 74 | keep all methods verbatim; contingency in plan |
| `src/api/README.md` | 215, 96 | hunk-disjoint, verify both text blocks survive |
| `docs/reference/log.md` | 176, 134, 233, 96 UI, native 440 | append-only, zero deleted lines |
| `cutover-evidence-pack.md`, `docs/reference/README.md` | main #1492, 134, native 440 | union only; 440 checkpoint is single writer afterwards |
| `role-screens.js` | 233, 96 UI | hunk-disjoint (programme versus `fundingDraftPanel`) |
| `chat.js` | 215 | sole owner |
| `store.py`, `test_mvp.py` | 1487, 1490c | already resolved |

## 4. Merge order

M0 main; M1 74; M2 176; M3 134 (union resolution); then optional wave B: M4 215; M5 233; M6 96 UI head (superset of backend) or backend only. After every merge: `git diff --check`, conflict markers absent, method-count assertions for touched test files. Each merge is `--no-ff` with a message naming the input head SHA and `Refs` issue numbers.

## 5. Invariant checks (run at the assembled head)

* Strict funding: grep shows `funding_ok` compared `is not True` / `is True` in the four readers and `MEMBERSHIP_REVISION = 3`; no truthiness test.
* `test_home_case_api.py` contains all 6 expected methods; `test_mvp.py` both 1487 and 1490 methods.
* 134 unpromoted: pack has the six partial and four deferred rows unchanged, "none passes", no new `Pass` claim for 1487, 1490, 74, 215, 233, 96; diff of the 134 section against `cc7e3c3a` is empty.
* Union: both #1492 and #134 section headings present exactly once.
* log.md: no deleted lines versus the parent plus main.

## 6. Required exact-candidate checks (publication gates beyond the full runner)

Commands run from `src/api` in the isolated venv with test-helper dirs only, each at the frozen candidate SHA, results stored externally with that SHA:

* Core units: `test_gates`, `test_home_case`, `test_chat_case_answers`, `test_sqlqueues`, `test_taskqueues`, `test_generated_dataset`, `test_form_export` (`python3 -m unittest discover -s tests -p '<module>.py' -q` from `src/core`).
* API units: `test_home_case_api`, `test_mvp`, `test_programme_screen`, `test_form_held_download_api`, `test_role_endpoint_inventory`, `test_role_screens_conformance` plus the regulatory and chat.js modules.
* Browser checks, required: `home_case_browser_check` (24 PASS), `regulatory_ux_check` (21 states), `programme_paging_browser_check`, `role_screens_browser_check 230`, the Held download check. Each records the pinned axe 4.10.3 file hash (`880970c0...a68bb`); a missing browser or axe blocks publication.
* Static: ruff 0.17.1, mypy 2.4.0, `node --check`, `git diff --check`, docs link review.

The 96 Held-download methods are exactly the 16 in `test_form_held_download_api.py` at `94760af7d` (6 original: `test_default_off_and_each_guard_condition_alone_serve_nothing`, `test_trusted_proxy_provider_never_serves_even_with_both_switches`, `test_served_body_equals_core_export_with_safe_headers`, `test_unauthorised_revoked_and_unknown_requests_get_no_artifact`, `test_unavailable_working_evidence_is_a_non_success_without_attachment`, `test_each_request_rechecks_current_state_not_the_screen_version`; 10 saved-check methods named in the research history). Every one must be present and pass, plus whatever the accepted 96 UI head adds. Exact full paths are the repository paths in Section 1 prefixed `src/core/` or `src/api/` as listed by `git diff --name-only <input-base>..<head>` at G3; that file list is frozen into the assembly manifest and any difference is a G3 failure. The 96 UI manifest rows are filled only from its accepted frozen head.

## 7. Full gate

`python3 tools/rpi-checks.py --all --jobs 3 --base <fetched origin/main> --out /tmp/rpi-149-ux`, on committed, clean source with evidence committed, under `/tmp/ama-rpi-heavy.lock`; then `--verify-receipt <receipt.json> --base <current origin/main>` just before push and assessment. Any later commit, rebase, base or tool change invalidates it. Missing SQL, browser or scanner prerequisite blocks publication; no cloud fallback, skip token or fabricated status. Hosted CI for the assembly head and the parent to main head is read, not assumed.

## 8. Not planned

No new issue, tick, approval, pool, spend, cloud, private data, shared cleanup, pack writer duplication or preflight matrix duplication.
