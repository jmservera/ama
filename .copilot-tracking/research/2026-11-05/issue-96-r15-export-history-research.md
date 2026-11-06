---
title: Issue 96 r15 export review-history research
description: Prospective research for carrying per-field review history into the Held draft export, with checkpoint gate assessment
ms.date: 2026-11-05
---

## Scope and identities

* Objective: carry the recorded per-field review history into the integrity-covered Held draft export (bounded PRD FR-042 provenance increment). Not a reviewed pack, approval, schema registration, rule engine, endpoint or UI.
* Branch `feat/form-export-review-history-96`, started at parent commit `0472fd5d5625bb610b5ac65ad177026953802830` (tree `268ead3a098f2320c0fba1a16aed14dd68a7fbe2`, equal to the c738 tree). Reviewed main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`. Parent topic integration head and main are pinned separately: the parent head has not reached main.
* Starting status: clean including ignored files. Issue #96 OPEN; C1/C5/C6 unchecked.
* Validation tier: FULL (finance-sensitive evidence, privacy and integrity contract). This continuation is light only. The c738 receipt `07ae...` does not cover any new candidate.

## Source observations confirmed independently

The external refinement (`96-residual-readiness-20261105.md`) is a proposal. These observations were re-read in source.

* `form_export.draft_export` builds a body from `BODY_KEYS` (11 keys, no `history`) and hashes it with SHA-256 over canonical JSON. `_report` already returns `history=deepcopy(draft["history"])`, so the data exists and the export omits it.
* Event shape (`form_review.py` review action): `field_id`, `input_version`, `prior`, `new`, `decision`, `reviewer`, `reason`, `at`. `prior`/`new` carry value, state and evidence.
* `_report` evidence preflight (`_document` availability check) raises `DocumentUnavailable` for unreadable cited evidence, and `draft_export` returns `Unavailable`. The preflight already walks history sources for the `attachments` set, so history evidence is covered by existing visibility checks.
* `export_freshness` rebuilds `body = {key: saved[key] for key in BODY_KEYS}`. A saved copy missing a key raises `KeyError`, which already yields `Invalid` with the regenerate-Held action. Adding `history` to `BODY_KEYS` therefore makes every legacy copy Invalid without any backfill.
* No API, web or other module calls `form_export`; only `src/core/README.md` documents it. No saved copy is persisted by the store; callers hold copies.
* `test_form_export.py` has 7 tests using the JSON and SQLite fixtures. `test_form_review.py` fixtures are reusable.
* AI registry dependency #105 is CLOSED (2026-10-15). It supplies no personal, Legal or Finance authority. This slice adds no AI dispatch.

## Contract compatibility assessment

* Adding a required key to the integrity-covered body is a persisted-contract change. Every previously saved Held copy becomes `Invalid`. The README documents `Invalid` as "incomplete or hash no longer matches", so the recovery path exists, but the meaning of the existing manifest changes.
* An optional-history alternative (legacy copies stay Current-capable) was considered. It would leave an integrity manifest that does not cover provenance and would silently call incomplete manifests current. The brief forbids silently downgrading the manifest change to avoid a checkpoint, so this alternative is rejected.
* Legacy Held-copy behavior today: copies from before this change lack `history`. Under the proposed adoption they are Invalid with action "Create a new held export from the working review." No backfill or rewrite.

## Stabilization checkpoint gate

* The coordinator rules (`ama-backlog-delivery-coordinator.agent.md`, Stabilization checkpoints) require a checkpoint "earlier when a material BRD/PRD, architecture or contract change ... is detected", and for stacked children merged into a declared parent topic, assessment of the pinned parent-topic integration head before dependent work starts.
* The latest checkpoint record in `docs/architecture/cutover-evidence-pack.md` is the fourth local checkpoint (2026-11-04) on main `fab02307`. A search found no record covering `feat/finance-integration-93`, parent head `0472fd5d5` or the Held export manifest contract. Issue #440 is OPEN; its latest comment concerns #123 and states it is not #96 acceptance.
* The manifest change is material under that rule. I cannot consume or manufacture the checkpoint: the coordinator selects scope and the work executes through its own RPI route, not in this session.

## Conclusion

* Feasibility: confirmed. The bounded behavior is small (one `BODY_KEYS` entry, one body field, tests, README) and reuses existing data and legacy-invalid recovery.
* Planning readiness: Ready for the design; NOT ready to implement. The implementation is blocked by an unresolved checkpoint disposition for the integrity-manifest contract change on the pinned parent head.
* Stop condition and owner: coordinator selects/consumes a checkpoint (existing #440 route or a scoped checkpoint issue) covering parent head `0472fd5d5` and the export manifest contract, with an explicit disposition of the legacy Invalid compatibility decision. Resume condition: that record exists in the cut-over evidence pack and the coordinator releases this lane.
