<!-- markdownlint-disable-file -->
# RPI Plan Critique: PR #1801 c2 Credential-Hygiene Test Fixture Remediation (Issue #185)

## Metadata

* Task ID: issue-185-simulated-device-identity-provisioning-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass final-candidate critique for `issue-185-simulated-device-identity-provisioning-c2` (`simulated-device-identity-provisioning-185-c2`) on branch `feat/iot-185-device-provisioning` (`ffce28c98`, `PR #1801` targeting `feat/demo-164-chat-grounding-provenance-0900` / `PR #1641`). Remediate the 3 `test_iot_credential_hygiene.SourceScanTests.test_no_device_key_or_connection_string_in_repository_text` matches across `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` via runtime string assembly while keeping runtime inputs byte-for-byte identical and literal source matches at `0`, validate under the Focused tier, and commit all code and `c2` `.copilot-tracking/` artifacts locally (`Refs #185` plus Copilot `Co-authored-by` trailer) without pushing or running `gh pr create`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md (`C1`-`C9`), .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md, .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md, src/api/tests/test_iot_credential_hygiene.py, src/core/tests/test_live_provisioning.py, src/core/tests/test_device_provision.py, src/core/pyproject.toml, and .github/workflows/src-ci.yml.
* Decisions, dependencies, and acceptance criteria considered: Confirmed split-keyword and split-payload runtime fixture assembly (`C3`-`C7`), standalone `src/core` test-source hygiene verification (`FR-2`), Focused validation tier under owner decision D4 and Issue #1294 (`C8`, `C9`), Python 3.12 `ruff` (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`) and strict `mypy` parity (`C6`, `C8`), and post-Review single clean local commit with privacy-safe noreply email and no remote push (`FR-3`).
* Assessment boundary: Evaluates plan and phase-detail completeness, technical accuracy, regex/formatter resilience, test-ownership counts, validation parity with .github/workflows/src-ci.yml, and local commit sequencing from the supplied artifacts and source files. Hosted `PR #1801` check re-execution after push is intentionally outside `c2` per caller no-push constraint.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern                                                                                                                                                              |
|------------------------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-1 (`C2`, `C3`, `C4`, `C5`, `C6`)      | Partial  | Runtime split-keyword and split-payload assembly eliminates all 3 CI matches and `[^\n]*` single-line bridging; `FR-1` mentions the 36-char fragment in singular (`PC-002`).     |
| FR-2 (`C3`, `C4`)                        | Partial  | Adds standalone `src/core` raw-source credential-hygiene scan across 6 files, but should explicitly preserve the existing `ast` `lp.contains_raw_secret` loop (`PC-002`).        |
| FR-3 (`C1`, `C9`)                        | Covered  | Reconciles all 7 dated `c2` `.copilot-tracking/` artifacts and defers the single atomic local commit until after `rpi-review` to avoid amending or splitting commits.            |
| NFR-1 (`C4`, `C5`, `C7`)                 | Covered  | Enforces runtime SHA-256 invariance against `ffce28c98` and `lp.contains_raw_secret(...) == True` potency checks across `24/24` combined provisioning tests.                     |
| NFR-2 (`C2`, `C6`, `C8`, `C9`)           | Covered  | Matches `.github/workflows/src-ci.yml` (`ruff check .`, `ruff format --check .`, `mypy`, `unittest discover` in `src/core`, and `12/12` in `test_iot_credential_hygiene.py`).    |
| P01 / P01-T01 (`C2`, `C3`, `C4`, `C6`)   | Partial  | Sound runtime constant assembly, but records `10` / `10/10` tests instead of actual `12` / `12/12` (`PC-001`) and under-specifies keeping `ast` scan + both line sites (`PC-002`). |
| P01 / P01-T02 (`C2`, `C3`, `C5`, `C6`)   | Partial  | Sound runtime owner-string assembly in `test_report_refuses_secret_bearing_credential_owner`, but records `14` / `14/14` tests instead of actual `12` / `12/12` (`PC-001`).      |
| P02 / P02-T01 (`C6`, `C8`, `C9`)         | Covered  | Runs all caller-specified Focused validation commands, verifies runtime SHA-256 digests and `{id}+{login}@users.noreply.github.com` local git config, and withholds `git push`.  |

## Verdict

* Verdict: Revise
* Rationale: The remediation architecture, contrarian `[^\n]*` single-line regex-bridging defense, Focused validation commands, and post-Review single-commit closeout are well-grounded in supplied evidence, but two direct planner-correctable inaccuracies need revision before implementation: `plan.md` and `phase-details.md` transpose the per-file test method counts (`10` and `14` instead of actual `12` and `12`), and `FR-2` / `P01-T01` should explicitly retain the existing `ast` `lp.contains_raw_secret` check on production modules (alongside scanning the 6 files with the 4 hygiene patterns and updating both 36-char signature fragment occurrences) so standalone base64 detection and `import ast` (`ruff` `F401`) remain intact.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Correct transposed per-file test method counts for `test_live_provisioning.py` and `test_device_provision.py`

* Related IDs: P01, P01-T01, P01-T02, NFR-1
* Evidence: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md (`Scope and Non-Goals -> In Scope`), .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md (`P01-T01` and `P01-T02` `Validation Expectations` and `Completion Evidence`), src/core/tests/test_live_provisioning.py, and src/core/tests/test_device_provision.py
* Concern: The plan (`Scope and Non-Goals -> In Scope`) and phase details (`P01-T01` and `P01-T02`) state that `src/core/tests/test_live_provisioning.py` has `10` test methods (`10/10`) and `src/core/tests/test_device_provision.py` has `14` test methods (`14/14`). Inspection of the source files shows `LiveProvisioningTests` defines `12` `test_*` methods (`src/core/tests/test_live_provisioning.py:39-453`) and `DeviceProvisionTests` defines `12` `test_*` methods (`src/core/tests/test_device_provision.py:36-142`), summing to the `24` combined tests cited in `NFR-1` and `P02`.
* Impact: Per-task verification in `P01-T01` and `P01-T02` and test-ownership lock checks during `rpi-implement` and `rpi-review` will observe `Ran 12 tests` in each file, contradicting the `10` and `14` completion gates and raising a false missing-test discrepancy on `test_device_provision.py`.
* Smallest useful change: Update the test-method counts from `10` and `14` to `12` (`12/12`) for `src/core/tests/test_live_provisioning.py` and `12` (`12/12`) for `src/core/tests/test_device_provision.py` in .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md and .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md.
* Action owner: planning parent
* Exact resolving evidence: Updated `In Scope` test ownership lock in .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md and `Validation Expectations` / `Completion Evidence` in `P01-T01` and `P01-T02` of .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md recording `12` test methods (`12/12`) for each file (`24` combined).
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: Explicitly retain the `ast` production-module secret check and cover both 36-char signature fragment sites in `test_live_provisioning.py`

* Related IDs: FR-1, FR-2, P01-T01, NFR-2 (`C4`, `C6`)
* Evidence: .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md (`FR-1`, `FR-2`, `P01-T01`), .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md (`P01 -> Likely Targets`, `P01-T01 -> Intent`), src/core/tests/test_live_provisioning.py, and src/core/pyproject.toml
* Concern: First, `src/core/tests/test_live_provisioning.py:1,132-143` imports `ast` and walks `ast.Constant` string nodes across `live_provisioning.py`, `device_identity.py`, and `device_provision.py` with `lp.contains_raw_secret(node.value)`, which catches standalone 44-character base64 keys even without a key-assignment prefix (`src/core/tests/test_live_provisioning.py:198,217`). `FR-2` and `P01-T01` describe scanning the 6 production and test files against the 4 credential-hygiene regex rules without stating that the existing `ast` `lp.contains_raw_secret` check on the 3 production modules stays in place; replacing it would drop standalone base64 literal coverage on production modules and leave `import ast` unused (`ruff check` `F401` under `src/core/pyproject.toml:32`). Second, the 36-character SAS signature assertion fragment appears at two call sites (`src/core/tests/test_live_provisioning.py:220` and `src/core/tests/test_live_provisioning.py:261`), whereas `FR-1` and `P01-T01` refer to "the 36-char signature assertion fragment" in the singular.
* Impact: Ambiguity in `P01-T01` could cause an implementer either to accidentally replace the stricter `ast` production-module check (triggering `F401` or weakening standalone key detection) or to split only line 220 while leaving line 261 untouched.
* Smallest useful change: Clarify in `FR-1`, `FR-2`, and `P01-T01` that (a) `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` retains its existing `ast.walk` + `lp.contains_raw_secret` check over the 3 synthetic production modules in addition to adding runtime fixture potency assertions and the 4-pattern raw-source scan across the 6 production and test files (splitting regex keyword tokens in `re.compile(...)` so the test file cannot self-match), and (b) both 36-char signature fragment occurrences (`src/core/tests/test_live_provisioning.py:220` and `src/core/tests/test_live_provisioning.py:261`) share a runtime-assembled constant or split expression.
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-1`, `FR-2`, and `P01-T01` wording in .copilot-tracking/plans/2026-11-15/simulated-device-identity-provisioning-185-c2-plan.md and .copilot-tracking/details/2026-11-15/simulated-device-identity-provisioning-185-c2-phase-details.md naming retention of the `ast` `lp.contains_raw_secret` production scan and both 36-char fragment sites (`lines 220 and 261`).
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strong root-cause and contrarian regex analysis: Identifying greedy `[^\n]*` single-line bridging in `PATTERNS["device connection string"]` and `PATTERNS["shared access signature"]` (`src/api/tests/test_iot_credential_hygiene.py:46-50`) and splitting both marker keywords/domains and base64 payload halves via explicit `"".join((...))` / `+` prevents `ruff format` (`line-length = 100`) from re-creating any match while keeping runtime SHA-256 fixture digests 100% unchanged.
* Cross-package blind-spot closure: Extending `test_live_provisioning.py` to scan synthetic provisioning test files closes the feedback gap where standalone `src-core` CI passed in `c1` while `src-api` caught literal test fixtures.
* Clean single-commit RPI sequencing: Verifying `{id}+{login}@users.noreply.github.com` in `P02-T01` while deferring the single local `git commit` until after `rpi-review` reconciles all 7 `c2` `.copilot-tracking/` artifacts avoids `git commit --amend` or split commits atop `ffce28c98`.
* Residual risk (explicitly accepted by caller constraint): Hosted `PR #1801` `src-api` check verification waits on coordinator push of the frozen local commit; mitigated locally by executing the identical `src/api/tests/test_iot_credential_hygiene.py` suite and `src/core` CI checks (`unittest discover`, `ruff check .`, `ruff format --check .`, `mypy`).

## Questions or Blocking Evidence Gaps

* None. All findings are direct planner corrections fully resolved by the supplied repository files and caller constraints.

## Limitations

* Critique stayed strictly read-only with respect to plan, phase details, session state, and source/test files, and did not execute external network or remote GitHub mutations.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Directly revise `PC-001` (`12` + `12` per-file test method counts) and `PC-002` (explicit retention of `ast` `lp.contains_raw_secret` production scan and coverage of both 36-char signature fragment sites at lines 220 and 261) in the plan and phase details, then finalize planning without another critique pass and proceed to `rpi-implement`.
* User response required: no
