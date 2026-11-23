# Issue 202 live research, 2026-11-23

Disposition: executed. Planning Readiness: Ready.

## Criteria status (issue body read 2026-11-23)

* Four of five ticked. Only unticked: "Old workflows (`mvp-ci`, `mvp-validation`) removed or replaced, and branch protection required checks updated".

## Evidence

* Both workflow files exist, are `workflow_dispatch` only, and are `disabled_manually` on GitHub (`gh workflow list --all`: Source CI, Source validation).
* Ruleset `mainprotect` (24504150, active) has `required_status_checks: []`; no classic protection (HTTP 404). So no required check names the old workflows and no protection edit is needed. Not changed.
* Repo references to the files: `.github/workflows/src-ci.yml` (path filter line 5, actionlint line 281, no-working-data), `tools/rpi-checks.py` (WORKFLOWS, WORKFLOW_HASHES, coverage_rows), `tools/check-legacy-references.py` allowlist, `infra/tests/test_pipeline.py`, `tools/test_src_cutover_repoint.py`, docs (`infra/README.md`, `src/README.md`, `src/api/README.md`, `.github/rubric/README.md`).
* `src-ci.yml` has an `mssql` job equal to mvp-ci's; it has no `cap-drop` container-hardening probe (only mvp-ci `image` does), so that coverage is lost from hosted CI on removal and must be recorded.

## Classification

Workflow and gate-tool edits: full tier by impact (gate semantics). No external receipt is available to this worker and rpi-checks --all is forbidden, so the receipt remains owner/coordinator work.
