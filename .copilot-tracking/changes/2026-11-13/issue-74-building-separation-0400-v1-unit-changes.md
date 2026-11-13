<!-- markdownlint-disable-file -->
# Changes: issue-74-building-separation-0400 V1 unit verification

Date 2026-11-13. Partial V1 only (unit tests). Continues the original research, plan, details, critique and review, which are preserved unchanged. This is not a whole-RPI release Pass and not closure.

## Source and environment

* Branch research/demo-building-separation-74-0400; HEAD 5676f9025 (planning freeze), full HEAD 5676f90251f069f63be18147426674b791683aac, tree 9f3ee51d2df6f094cda51e358c4167d7c80c92b1.
* Current origin/main after fetch: 6f2918011d55d63ffc52865073ef45bd7ea9197c, equal to the recorded product source (currentmain6f29) and to the merge base. No divergence. HEAD differs from origin/main only by seven tracking files.
* Worktree clean before and after execution; no product, test, configuration or dependency-manifest edit.
* Interpreter: owned venv `venv/bin/python` 3.12.3 under the coordinator output directory (`files/74-unit-verification-0408/`). No PYTHONPATH legacy hack; PYTHONPATH carried only the documented test-helper directories (`tests`; `../core/tests:../agents/tests`).
* Editables (pip direct_url, editable, file URLs): zava-forward-core, -agents, -api 0.1.0, all pointing at this worktree's `src/core`, `src/agents`, `src/api`. No scratch or other candidate.

## Dependency handling

The selected validation first failed with `ModuleNotFoundError: No module named 'zava_forward'` (core-attempt1.log, api-attempt1.log). Only then `pip install -e core -e agents -e api` (src README and api README form) ran in the owned venv; exit 0 (pip-install.log, pip-freeze.txt). No uv, no manifest change.

## Results

| Command (cwd) | Result |
| --- | --- |
| `PYTHONPATH=tests python -m unittest -v test_home_case` (src/core) | exit 0; Ran 8; OK; 0 skips |
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_home_case_api.py -v` (src/api) | exit 0; Ran 6; OK; 0 skips |

Total 14 unit tests pass. Named core IDs: funding_confirmed_is_true_only_for_explicit_true; recorded_versions_are_retained_and_conflicts_refused; roles_and_finance_restriction; scheme_registry_validation; shared_building_id_never_transfers_evidence_between_homes; unknown_scheme_closed_case_and_missing_source_are_refused; version_starts_unrecorded_and_links_are_explicit; versions_survive_reopen. Named API IDs: absent_funding_reads_as_not_confirmed_not_missing_case; finance_staff_get_building_cost_and_own_home_allocation_over_http; non_finance_staff_get_no_cost_amounts_over_http; screen_is_wired_with_manual_path; version_recorded_through_http_and_retained; view_separates_home_and_building_and_denies_unauthorised. The API tests use owned loopback HTTP and synthetic fixtures only.

Harness error retained: a first API invocation without the tests directory on the path failed with `No module named 'test_home_case_api'` (api-attempt2-invocation-error.log). This was my command error, not a product failure; the documented `discover -s tests` form was then used. No product failure occurred.

## Imported module SHA-256 (editable, this checkout)

* zava_forward.core.home_case c2cd534f99b13194a7d888d9e9c9b6eccc9279dc6fba5259ac54098272200a76
* zava_forward.core.store d1d20cfeaa2e0e82b2cdf3338561f7fa1161da8e09afbe5165459245e59ec19d
* zava_forward.api.server 67fc5ce04d661774b46d0bafba5748880aab87d3b62d663d20f7df21fde102ab
* building_fixture 07d3814ce978cf7aa5d3da632422c942a786b81dec7a52a963e8d907cb7624ad
* test_home_case.py cdee2f12ed4eb70728b99a02a6dc3349e50bfa75d9449d8931df55d46cbbb07f; test_home_case_api.py 0480b34a182d7b8d53725bf982c33130767298bdce7a7f1df55cf8d73f8ca3d0

Log SHA-256: core.log 1183851629fcb4c8c45a8090f620f083148afbb125fa8074abd5c13ed98e410c; api.log bfa015b3db4f33411d77f4251412c90102d14a6176f53993f54e91aad4663a1f; provenance.txt bd461c85915a09081fa19d30a3c9386f83f0bd0878487a0876a5749b97bf9bc8; pip-freeze.txt 6a051bca6a3b06ce39214a967add2ef0d47d2be7047d1df461054541f11f7e94. Raw outputs live outside the repository in the coordinator `files/74-unit-verification-0408/` directory (retained, with the venv).

## Limits

* Not executed: the 23 browser checks plus server PASS, the reported whole 24, buildingView, axe, AT, SQL, Docker, human review, criterion 2 acceptance. Chromium version not read. These stay unobserved; a separate actual-holder and resource admission follows after this environment freeze.
* The units do not repair or test G5 applicability, unknown-funding display, or outcomes (CR-001, CR-002, CR-003 unchanged). They cover source behaviour, not the rendered home panel.
* Source authorization beyond the 2026-11-12 test-only admission remains unknown, not zero or exhausted.
