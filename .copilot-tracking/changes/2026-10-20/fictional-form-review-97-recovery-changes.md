<!-- markdownlint-disable-file -->
# RPI Changes: Fictional Finance form/template review pack (#97), recovery

## Metadata

* Task ID: 97-recovery
* Related plan: .copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md
* Phase details: .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md
* Implementation date: 2026-10-20

## Execution Status

* Status: Complete (local, unreviewed until the single Review)
* Declared invocation scope: full plan
* Completed scope markers: P01, P02, P03
* All remaining active-plan markers: none
* Status basis: rpi-implement skill invoked 2026-10-20 after plan and one critique

## Execution Summary

Implementation began from an unverified pre-RPI draft (uncommitted pack, test, register entry). Starting-state hashes of the preserved hand-authored draft artifacts are in /tmp/ama-97-base/SHA256 and reproduced under Validation Record when finalized.

## Changes

* Added: src/core/evals/fictional_form_review_pack.json (fictional pack, 16 fields, 9 stale triggers, FD-01..FD-14 null); src/core/tests/test_form_review_pack.py (8 tests, incl. PC-001 stale-trigger mapping, PC-003 staging-contract lineage and human-only refusal, PC-002/005 labels); docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md (reviewer guide).
* Modified: provenance-register.json (DS-FICT-FORM-REVIEW-PACK), data-dictionary.md, src/core/README.md, docs/reference/README.md, docs/reference/log.md (append-only entry).
* Appended dated disclosure clarifications to the four preserved pre-RPI draft artifacts; original bytes verified as exact prefix.
* No change under src/core/src, no excluded doc touched.

## Validation Record

* unittest test_form_review_pack, test_synthetic_provenance, test_form_staging: 37 tests OK.
* ruff check, ruff format --check, mypy in src/core: clean (before the doc-only edits that followed).
* Pre-append SHA-256 of preserved drafts: details 5375e5f4..., critique 700272f5..., plan 6505bf4d..., research ed13d97a... (full values in /tmp/ama-97-base/SHA256).
* Full gate: run after commit with an external receipt; not part of this record.

## Reconciliation and Review Readiness

* Plan markers P01-P03 checked; critique PC-001..PC-007 applied; no divergence from plan.
* Remaining human gates: actual Finance authority and binding (FD-01..FD-14), criterion 1 unmet, no approved-template status. Criterion 2 delivered by PR 377.

## Correction after failed local gate (rpi-implement continuation 2026-10-20)

* Trigger: the complete local gate failed at 106fbc96 in the agents test test_eval_registry (test_every_eval_file_is_registered_with_matching_version): the new eval file was absent from the evaluation registry. Failed receipt /tmp/ama-serial-2150-97/receipt.json and log 0021-project-agents.log are retained unchanged. Classified as a directly coupled fixture integration defect, not waived.
* Fix: registered fictional-form-review-pack in src/agents/evals/registry.json (contains_real_data false, owner unassigned, purpose states fictional and not approved) and added the top-level version key fictional-form-review-pack-v1 to the pack so the registry version invariant holds. The invariant and runtime are unchanged. No Finance approval is implied; FD-01..FD-14 stay null.
* Validation: test_eval_registry 8 tests OK; test_form_review_pack and test_synthetic_provenance 20 tests OK. Full gate not run here; coordinator reruns serially.
* Original Review, critique and process-defect disclosure are unchanged; no new Review.

## Hosted dependency-advisory correction (rpi-implement continuation 2026-10-21)

* Trigger: hosted Source CI run 39529698651 on draft PR 424 failed the image scans for api, importer and orchestrator on fixable CRITICAL GHSA-6q48-6c7w-9gw2 (certifi 2026.7.22, fixed 2026.10.19). Reports retained at /tmp/ama-pr424-trivy-0157 and /tmp/ama-pr424-trivy-api-0159. Prior complete-gate Pass at be31f2b8 is historical after this new commit.
* Change: reused ONLY the existing native #119 correction a3257c71f4963d98a88c501d040b3d07eada4392, applying its exact four lockfile blobs (src/core, src/api, src/importer, src/orchestrator requirements.txt; certifi 2026.7.22 to 2026.10.19 with matching hashes). Blob ids match that commit. No independent solution, other pins, digests, ignores, baselines or controls, and no #119 tracking or map edits. The #119 gate that passed with this change: /tmp/ama-map-fixed-followon-0223-119/receipt.json.
* Validation: blob equality and hash-line comparison only; no heavy gate or build here. A fresh full gate and hosted rerun are pending the coordinator.
* Separate unresolved hosted blocker: the external rubric/score check fails (details must contain exactly 20 criterion IDs) although workflow 39529698552 overall succeeded. Not fixed here: no manual scores, no rubric change, no bypass, no paid scorer. Coordinator requests fresh hosted scoring after verified publication.
* Unchanged: original Review (Residual work), critique, disclosures, failed and passed gate evidence. Finance FD-01..FD-14, template authority, binding and OQ-015 stay unresolved; no approved schema or Finance activation; Refs #97 only, no closure.
