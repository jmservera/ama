---
title: Issue 165 criteria audit changes
ms.date: 2026-11-13
---

## Summary

Read-only audit of the literal acceptance criteria of issue #165 against commit 34b11967b93df40b653d384ab3b136bb1fb842f9. No source, test or documentation outside `.copilot-tracking/` changed. Verdict: epic #165 is NOT ready to close; 0 of 5 criteria are fully proven.

Scope mismatch: the brief describes an "EPC conflict / stock discrepancy" audit. Issue #165 is "Epic: Synthetic data programme: needs, generator and sensor simulator" and has no EPC-conflict criterion. The EPC and stock tests were run as instructed and are cited where they bear on the synthetic-data criteria.

Evidence kinds: commit-pinned file:line evidence, and live GitHub issue state retrieved with `gh` on 2026-11-13 (not pinned to the commit).

## Tests run

Environment: `/tmp/venv-165-1531` (`--system-site-packages`, pip only; removed before commit).

| Suite | Command | Result |
| --- | --- | --- |
| src/core | from `src/core`: `PYTHONPATH=tests python -m unittest test_needs_inventory test_stock_register test_stock_fabric test_sensor_stock test_stock_reconciliation test_synthetic_provenance test_generator_coverage test_scenario_manifest test_generated_dataset` | 123 tests, OK |
| src/api | from `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_stock_reconciliation_api` | 6 tests, OK, 1 skipped (opt-in Playwright rendered check) |

A first core run without `PYTHONPATH=tests` failed to import `dataset` (`src/core/tests/dataset.py`); this was an invocation error, not a product failure.

Not run: the full synthetic-data suites (sensor backfill, stream, device, climate), the complete local gate, hosted CI and any browser check. These tests prove generator behaviour only; they cannot satisfy the human, owner and Azure gates below.

## Per-criterion proof table

| # | Literal criterion | Verdict | Evidence | Missing gate |
| --- | --- | --- | --- | --- |
| 1 | #440 stabilization checkpoint completed before epic closure | NOT FULLY PROVEN | Live: epic comment of 2026-11-04 states #440 is human-blocked and that merged children cannot satisfy it; `gh issue view 440` listed its criteria on 2026-11-13. No checkpoint record for #165 exists in this commit. | Executed #440 checkpoint covering #165 with BRD/PRD/ADR reconciliation, regression disposition, authorized Azure-only residuals and an owner-approved pivot or defer decision |
| 2 | Needs inventory and phase gate approved by the owner | NOT FULLY PROVEN | `docs/reference/research/retrofit-synthetic-data/needs-inventory.json:5` status `draft-awaiting-owner-review`; `:320` open item (`open_items` at `:319`) "Owner approval of this inventory and of each row owner (all owners are proposed)"; `:3` version 1.3.0. The gate rule is recorded at `:9` and structurally tested at `src/core/tests/test_needs_inventory.py:36-42`. Child #166 is closed, but closure is not owner approval. | Named owner approval of the inventory, row owners and the volume decisions for SN-03, SN-08, SN-09 (`:321`) |
| 3 | Every need has a recorded coverage status: covered, partial or missing | PROVEN for recorded rows SN-01..SN-13 only | `needs-inventory.json:11-15` (values covered, partial, missing); a `coverage` field on all 13 rows (lines 28, 51, 75, 99, 122, 145, 168, 190, 213, 236, 258, 281, 304; 11 partial, 2 covered); enforced by `src/core/tests/test_needs_inventory.py:21-28` (tests passed). Qualification: the inventory is a draft and open item `:323` says the first matrix was unavailable and the inventory was rebuilt, so completeness of the need list rests on the owner review of criterion 2. | None for the literal wording; completeness of the need list depends on criterion 2 |
| 4 | All child features closed or deferred | NOT FULLY PROVEN | Live `gh api repos/jmservera/ama/issues/165/sub_issues` 2026-11-13: registered children #166, #167, #175, #177, #190 CLOSED; #176 (determinism, seeds, refresh policy) and #184 (live IoT Hub streaming) OPEN with no recorded deferral. Grandchildren #168-#174 and #178-#183 are CLOSED; #185 (device identity, child of #184) is OPEN. The 2026-11-04 epic comment is stale for #190 (now CLOSED) and attributes #176 to the absent original OSM stock generator and pinned inputs and #184 to owner decisions OD-43, IoT Hub provisioning and credential assurance. `docs/reference/research/retrofit-synthetic-data/README.md:128` and `:333` confirm the original generator is absent and determinism is "Unmet overall". | Close or owner-defer #176 and #184 (with its open child #185); Azure-only residuals need authority and cost headroom |
| 5 | All generated data labelled synthetic with no real personal data beyond documented OSM map anchors | NOT FULLY PROVEN | Labelling is shown for the stock register: `src/core/src/zava_forward/core/synthetic/stock_register.py:68-69` (`source_type` SYNTHETIC and `synthetic_label`), with `:1` stating synthetic only. Bounded offline checks exist (`src/core/src/zava_forward/core/synthetic/privacy.py:1` states they are "never a universal personal-data guarantee"; label/pattern tests at `src/core/tests/test_synthetic_provenance.py:141,172,282`). `docs/reference/research/retrofit-synthetic-data/README.md:128` records that the register samples real OpenStreetMap anchors and its generator is absent, so the 60,000-home register cannot be regenerated or scanned here. The repository tests passed (123/6) but cover the fictional fixtures. | Owner-accepted privacy review across all generated datasets (including private 60,000-home register and chat/sensor data), and the original generator and pinned OSM inputs |

## EPC and stock tests relevant to the brief

* `src/core/tests/test_generated_dataset.py:155` (`test_epc_and_survey_fields_reconcile_to_fabric_and_conflicts_are_manifested`) passed; EPC records are seeded, reproducible and conflicts are manifested for the fictional fabric.
* `test_stock_register`, `test_stock_fabric`, `test_sensor_stock` passed; they exercise the fictional register and fabric (SN-01, #168).
* `test_stock_reconciliation` (core) and `tests/test_stock_reconciliation_api.py` (API) passed; they cover EPC conflict comparison with human sign-off. They do not map to any #165 criterion.

## Recommendation

Leave #165 open. Do not tick any criterion except criterion 3, and only for the recorded rows with the qualification above. Next actions are human or owner decisions: approve the inventory, run the #440 checkpoint, close or defer #176 and #184, and accept a privacy review. No GitHub issue was edited.
