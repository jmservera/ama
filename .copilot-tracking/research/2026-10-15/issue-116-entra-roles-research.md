# Research: issue 116 Entra roles and field-level visibility

Disposition: executed. Planning Readiness: Ready.

* Existing: `mvp/zavaforward_mvp/projection.py` default-deny allow-lists; `tests/test_role_matrix.py` covers many endpoints.
* Gaps: no route inventory guard; audit/export/search/AI-prompt contractor canaries not asserted together; staff-written free text (contact notes and outcomes, appointment and hazard notes) shown to staff without a reason need and outcomes fed to AI prompts.
* Decision (owner direction 2026-10-15): keep existing sign-in, map Entra app roles to personas. ADR 0005: synthetic fixtures only.
* Open (owner/external): OD-14 and OD-19 role confirmation by DPO/Legal (Juan Manuel Servera), Entra B2B guest contractor identity, browser acceptance per role.
