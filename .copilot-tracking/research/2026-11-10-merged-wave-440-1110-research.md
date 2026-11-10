<!-- markdownlint-disable-file -->
# Merged-wave 440 checkpoint (2026-11-10) research

Task `440-merged-wave-1110`, mode automatic, prospective record written before any validation command or document edit. Original; later corrections are additive.

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Identities read (actual tool output)

* Worktree `issue-440-merged-wave-1110`, branch `docs/demo-merged-wave-440-1110`, clean at start; `HEAD` = `da4f52abb5bfdc50acc9b9b8aa84cc42babc77fe`, tree `823c9cba2e219c5810f4e289145cb4ebe5c7c6cf`.
* `git fetch origin main` and `git ls-remote origin refs/heads/main` at 2026-11-10T02:04:16Z: `da4f52abb5bfdc50acc9b9b8aa84cc42babc77fe` (same as HEAD). Later main is not implied by any result.
* Subtree ids at pin: `src` `f8cf2443b124c0e8e089ea4f49ed6ef1eeebd6f3`, `tools` `74ad3cb586dbff7f08ed3ba78301b9596a31ca86`, `infra` `d94040329d5497aee252300972cb3c7497689d25`, `.github/workflows` `29eb03ea759ea6717e334d8f0949915d5ba37a90`.
* Documents at pin (blob): BRD `34d88395de86` (0.21.0, draft); PRD Zava Forward `c788b917bafa` (0.21.0, in-review); PRD proper-warm `f7f9b7675e60` (0.13.0, in-review); addendum `28c1924285ee`; original `0aec2d807011`. Unchanged from the Quality M2 record; none approved.
* Merged inputs (gh, 2026-11-10): PR 1343 `a740072d1` (01:23:03Z), 1346 `0385ad6a5` (01:41:47Z), 1345 `96afce427` (01:45:21Z), 1348 `da4f52abb` (02:00:25Z), Quality M2 record 1347 `e9c98eb20` (docs only, inherited), scorer bots 1349 `933416991` and 1350 `5861d6d3e` (rubric score file only). PR 1351 is OPEN and excluded. Issues 440, 149, 153, 1238, 93, 96, 148 are OPEN.
* Source files changed by the four feature PRs (git show --stat): 1343 `src/api/.../web/timecapture.js` and `test_timecapture_copy.py`; 1346 `src/core/.../resident_decisions.py`, `test_resident_decisions.py`, core README; 1345 `src/core/.../form_review.py`, `forms.py`, `form_export.py`, tests `test_form_dependencies.py`, `test_form_export.py`, `test_form_review.py`, core README; 1348 `src/orchestrator/.../rebuild_azure.py` and `test_rebuild_azure.py`.
* Environment: Python 3.12.3, node v24.21.0, no ambient `ZF_*` variable. Pre-existing editable installs in the user site point at another checkout (`/home/azureuser/source/ama/src/*`), so an owned venv with editable installs of this worktree's four distributions is required.

## Existing harnesses selected (no new checker)

* Finance: core `test_form_dependencies`, `test_form_review`, `test_form_review_pack`, `test_form_export`, `test_form_staging` (earlier 67) and API `test_form_staging_api` (earlier 14, and 7 in another record: re-observed here, not assumed).
* Resident: core `test_resident_decisions` (JSON, SQLite and fake-Azure classes; `MssqlResidentControls` skips without a disposable SQL Server by design). Representative named cases: `test_forward_defaults_unconfigured_and_keeps_local_request`, `test_supersede_default_unconfigured_rejects_inferred_roles_and_forged_rows`, `test_supersede_binding_is_validated_and_immutable`, `test_supersede_restamped_binding_digest_on_an_old_approval_does_not_count`, `test_supersede_legacy_generic_audit_entry_is_not_proof`, `ComplaintsRouteConfiguration.test_only_unconfigured_is_known_and_it_sends_nothing`.
* Rebuild adapter: orchestrator `test_rebuild_azure` (`FakeAzure`, `DryRunTests`, `GuardTests`, `RebuildTests`, `TeardownTests`) and `test_rebuild`; README command `PYTHONPATH=../core/tests python -m unittest discover -s tests -q`.
* Time capture: API `test_timecapture` (off by default, DPIA, notice, manager-only activation) and `test_timecapture_copy` (text units, plus opt-in `StaffTimeGuidanceBrowser` that needs `ZF_BROWSER_TESTS=1`, loopback Chromium, external routes aborted).
* Served staff journey: API `test_case_journey` (Node-driven, synthetic), `test_role_matrix` (loopback HTTP roles, denials), `test_workbench` (manifest).
* Integrity and boundaries: core `test_scenario_manifest`, `test_needs_inventory`, `test_version`, `test_dependency_rule`; the same module names exist in API, agents, orchestrator and importer (`test_version`, `test_dependency_rule`), so each runs in its own process from its own project directory and import origins are checked.

## Constraints carried

* Targeted tier only (src/README stabilization ladder rungs 1 to 3 local, rung 4 not entered). No blanket `rpi-checks.py`, no SQL Server, no Azure, model, provider, IoT Hub, real image build or push, private data or real users.
* Only canonical writes: `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` and own RPI records. No product, test, tool, infra or policy edit. A real blocking defect would be preserved with command, source and reproduction, compared with existing issues, and routed, not fixed.
* Correction ledger for #440: C2 of five spent, three remain (as stated in the brief). This observation does not reset or consume it and grants no source correction.
* Classes kept separate: local observed, historical, implemented-unverified, blocked, not run, unknown.

## Open risks identified before running

* Mixed Core and API module names: counts must name the process and directory.
* Browser opt-in test is local Chromium only; a failure there needs environment-versus-product classification.
* `test_resident_decisions` is large; it may take minutes on SQLite. Bounded by `timeout`.

## Follow-up candidates (current at research)

1. Owner release, budget and role decisions and an admitted live walkthrough (#1288, #184) keep actual-model proof blocked.
2. Named human activation and approval of resident forwarding and supersession (#1238) remain absent.
3. Live rebuild admission (#148) still needs owner authority and cost headroom.
