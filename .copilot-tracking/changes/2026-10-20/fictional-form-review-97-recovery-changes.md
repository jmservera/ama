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
