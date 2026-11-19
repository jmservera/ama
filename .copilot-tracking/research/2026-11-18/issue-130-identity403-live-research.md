# Issue 130 identity 403 research (2026-11-18)

Refs #130. Demo, desktop only. Disposition: executed (code reading, offline reproduction, mutation probe; live evidence reused from earlier runs because a fix cannot be deployed under this task).
Prior same-day artifacts named `issue-130-live-*` are preserved untouched in Git history; this run uses the slug `issue-130-identity403-live` for its own artifacts. The brief-mandated state file path `issue-130-live-state.json` was overwritten with this run's state; the previous content is in Git at `HEAD`.

## Findings

* `resident_decisions._operation` ran `if actor != _person(store, user.get("email")): raise PermissionError(...)` (about line 1112). `actor` is a copy of the verified Entra principal (extra keys: `tid`, `bound`, `identity_source`, `display_email`, `app_roles`, display name); `_person` returns the plain roster row. For any Entra principal the dicts always differ, so every staff write through `_operation` returned 403 "Reload your current staff identity before recording this step." Earlier live runs (issue 130 r1-r5, issue 220) saw exactly this 403 for the Entra demo principal.
* The same comparison was never exercised by a test: with the check replaced by a bare `_person(...)` call, all 449 tests in `tests/test_resident_decisions.py` still passed (mutation probe, output in the changes record).
* Offline reproduction: a roster row carrying `oid` and `tid` plus a bound Entra principal (`identity.principal` with `bound` code and email) is refused with the 403 message on the unfixed code (JSON and SQLite stores).
* Authorization keys are immutable: email, code and oid. `change_provenance._actor` already resolves the bound principal to exactly one roster row by tenant and object id and checks code and email against the binding.

## Criteria

* Only unticked criterion: "Representative participation and comprehension require authorized human evidence; constructed UI checks alone cannot pass that gate." Cannot be proven for the demo: data are synthetic, no representative authority is recorded, and the owner excluded person-run testing and DPO/Legal approval for the demo. Evidence: `docs/reference/research/issue-130-identity-403-live-2026-11-18.md`.

Planning Readiness: Ready.
