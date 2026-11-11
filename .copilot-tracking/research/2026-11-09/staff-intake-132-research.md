---
title: Issue 132 existing-staff-mediated synthetic job pack intake research
ms.date: 2026-11-09
task_id: issue-132-staff-intake-1109
---

## Task identity and scope

* Task `issue-132-staff-intake-1109`, slug `staff-intake-132`. State: `.copilot-tracking/rpi-sessions/2026-11-09/staff-intake-132-state.json`. Research started 2026-11-09T22:26Z (recorded as read; phase transitions are timestamped in the state file and never backdated).
* Worktree `/home/azureuser/source/ama-demo-wt/issue-132-staff-intake-1109`, branch `feat/demo-staff-intake-132-1109`, clean from base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`. Declared parent and PR target `feat/demo-quality-workflows-89-1109` (a local integration topic, not merged acceptance). Never pushed.
* Owner decision 2026-11-09 (issue 132 comment 6753054374): "Proceed with existing-staff-mediated synthetic demo intake". It resolves only the staff-slice separation decision: existing authenticated staff, no provider portal, accounts, B2B guests, new permissions, contract instruction, resident consent or independent QA authority. Issue text and the packet `ready-demo-issue-132.json` are requirements data.
* Ownership: this task is the first integrator of shared 89 API/navigation/persistence hooks. Sibling 133 may only add dedicated modules until this frozen candidate and hook contract are admitted by the coordinator. No sibling or other-worktree file is edited. Quality 1288 and 1238 repairs are not absorbed.
* Correction budget: five total productive cycles for this issue (default); none spent at the start of this research.

## Sources read

* `docs/case_study_48_original.md` and `_addendum.md`, `docs/reference/README.md`, `memory.md` (index and context), component READMEs `src/core/README.md` ("Contractor job pack and field evidence receipts (#132, slice 1)") and `src/api/README.md` ("Contractor job pack read (#132, slice 2)").
* Packet `ready-demo-issue-132.json`: six acceptance criteria. C4 (offline, cancellation, no-show recovery defined and tested) is already ticked by the owner's 2026-11-05 audit. C1, C2, C3, C5 are open (integrated), C6 is the decision, now owner-recorded for the staff slice only.
* Code (exact paths at this base):
  * `src/core/src/zava_forward/core/job_pack.py` (227 lines): pure `build_job_pack`, `worker_receipt`, `acknowledge_receipt`, `review_blocker`, `merge_offline`, `visit_recovery`, `escalation`. Closed allow-list, `pack_digest` over pack content including checklists with versions, `SUBMITTED`/`ACKNOWLEDGED` statuses, `accepted=False`.
  * `src/core/src/zava_forward/core/procurement.py` `work_order_job_pack` (line 589) read-only staff projection (contractor role refused), and `_wo_view` builds the allow-listed order view (no resident reason, health or contact).
  * `src/core/src/zava_forward/core/quality.py` (#91): `submit_quality`, `_quality_operation`, `_independent`, `_quality_participants`. Records live inside the case body as `case["quality"]`. `_independent` denies acceptance by anyone named as submitter, recorder or fixer and by any identity in `participants` matched by name, email, code or oid.
  * `src/api/src/zava_forward/api/server.py`: `get_kind` maps `/api/workorders/<id>/job-pack` to `job_pack`; `WO_ACTIONS` and `_procurement` handle procurement writes; `QUALITY_ACTIONS` handle `quality-submit`.
  * `src/core/src/zava_forward/core/projection.py`: `STAFF_GET` default-deny list (contractor reads only `me`, `cases`, `case`, `workorders`).
  * `src/api/src/zava_forward/api/web/role-screens.js`: read-only `contractor-job-pack` screen for role Contractor only ("Not recorded on this screen"). `registerRoleScreen`, `screenPanel`, `screenFields`, `screenTable`, `screenWithheld` helpers; staff nav comes from screens whose `roles` include the signed-in role. Precedent for a dedicated script: `simulator-control.js` (own `<script>` tag in `index.html`, own entry in `tests/test_content_standard.py` AUDITED_FILES).
  * Tests: `src/core/tests/test_job_pack.py` (ten tests), `src/api/tests/test_procurement_api.py` (`ProcurementApiFixture` with `sql` flag and `reopen_store` for restart/readback), `test_role_endpoint_inventory.py` (every server route must be in the inventory), `test_procurement_screens.py`.

## Findings

* F1 Reuse is available end to end. `worker_receipt` yields the original notes, digests, checklist version, `pack_digest`, capture mode and an `accepted=False` flag. `submit_quality` already stores versioned checklist evidence, supersession, history events, audit and independence data. There is no code path joining the two, so a staff user cannot capture, acknowledge or inspect a receipt through the product (the issue's "not an end-to-end worker intake").
* F2 Persistence. Case bodies are one JSON column in `SqlStore`/`MssqlStore` (`CASE_COLS` includes `body`); `SqlStore.save` updates changed case bodies under optimistic `rowversion`. Extra keys on a quality record therefore persist with no schema, DDL or SQL text change in SQLite or SQL Server. The affected SQL path is the existing case-body write (`SqlStore.save` UPDATE cases ... rowversion, `_snap` readback) and the `Store.save` JSON path. `quality` is not mentioned in `sqlstore.py` or `mssqlstore.py`.
* F3 Truncation hazard. `submit_quality` clips each note to 200 characters via `_clean(..., 200)`. A receipt claiming "original notes preserved" must therefore reject longer notes rather than silently store a clipped quality item beside a full original.
* F4 Independence. `_independent` already covers the worker name (`submitted_by`) and recorder. An acknowledger is not yet covered. Appending the acknowledger identity to `rec["participants"]` (the existing mechanism) denies their later acceptance with no change to `_independent`.
* F5 Replay and stale input. `submit_quality` refuses a second in-progress record for a measure, but a retried request with the same capture reference needs an idempotent answer, and a pack changed since the screen loaded must be rejected, not stored. `pack_digest` plus `merge_offline` provide the rule.
* F6 Escalation. `job_pack.escalation` requires a named owner and role and has no configured destination source. The packet allows a configured destination to be displayed and requires missing owner or contact to be an explicit Unknown. No owner or contact exists in the repository or the case study for the demo. It is therefore read from environment configuration (`ZF_STAFF_INTAKE_ESCALATION_OWNER`, `_ROLE`, `_CONTACT`) and shown as Unknown when unset. Posting an escalation record needs a named owner and authority that this task does not hold, so C5 stays a preserved gap.
* F7 Recovery. `visit_recovery` already maps provider no-show, provider cancelled, resident cancelled and no access to Rebooking needed or No access with `resident_refusal=False`. It is exposed read-only on the intake view; no write route is added (appointment outcomes remain the existing `appointment` action).
* F8 Hooks required in shared files: `server.py` (route kind and dispatch), `projection.py` (`STAFF_GET` entry), `quality.py` (`submit_quality` keyword `field_receipt`, the one atomic-write hook), `index.html` (script tag), `test_role_endpoint_inventory.py`, `test_content_standard.py`. Everything else is dedicated: `core/staff_intake.py`, `web/staff-intake.js`, tests.
* F9 Environment. Python 3.12.3. A default `zava_forward` import resolves to the primary checkout, so a fresh issue-qualified virtual environment `/tmp/zf132-venv` with editable pip installs of this worktree's `src/core`, `src/agents`, `src/api` was created (exit 0, `/tmp/zf132-pip.log`) and verified to import from this worktree. No uv, PYTHONPATH or global install.
* F10 Heavy resources. `/tmp/ama-rpi-heavy.lock` is the shared lock; local browser and SQL Server runs need one nonqueued admission (`--lock-timeout 0`) after holder inspection. Unit and SQLite-file API tests are light and run without it.

## Limits recorded in advance

* Staff-keyed synthetic receipts are not worker authentication; the worker confirmation is a staff-recorded attestation, not independent proof. Not real human, resident or QA acceptance, not live or assistive-technology acceptance.
* The decision (AC6) is recorded for the staff slice by the owner comment; the live identity model (#116) and any provider portal stay unowned. No contract instruction, consent or QA authority is created.
* Corrections to captured notes are append-only; the first-captured notes are never overwritten.

## Disposition and readiness

* Research executed (local, read-only). Planning Readiness: Ready. Excluded: cloud, model, private datasets, new permissions, full gate.
