<!-- markdownlint-disable-file -->
# Issue 87 correction TWO

## Authorization and Starting Boundary

* Date: 2026-10-18; same session b9f13d51-f8d3-4fc5-80bb-0e255ec31995.
* Coordinator instruction 2026-10-18T02:15Z authorizes final source correction
  cycle TWO, both supplied Medium findings as one batch, no new RPI loop.
* Initially clean HEAD: 59dce3b6be4f1d358269b6848520270ee3eade9a.
* Prior source: 0830f7c339fe9b5fa936cda849f14edc5a0e3624.
* Base/fresh origin/main: 99056cae7bc679d2ace3e42c75f28577cfce8887.
* Branch: feat/appointment-commitment-controls-87; existing open PR397/main.
* Frozen original Review SHA256:
  b0759a56265e8f82a5db71a99443736e07cec597b0e5e17bcc2d9a7f1e6cba4b.
* Frozen critique SHA256:
  044c3b5b9399522993ddb81ba4f90fe0f8a708960cc812169f306f29e80f7396.

## Supplied Independent Evidence

Coordinator reports external agent40f6133c inspected 33 paths/10 artifacts and
returned Not accepted with two Medium findings, while explicitly closing the
original seven at corrected source, subject to receipt-only later browser steps.
This is supplied external evidence, not a new Review executed here.

1. `src/core/tests/dataset.py` changed, while the coupled scenario-manifest source
   digest is stale. Two named manifest/inventory tests error; supplied full core
   CI result was 1048 run, two errors, 114 skips. Refresh digest through existing
   conventions/tooling; preserve integrity checks and honest scope/Unknowns.
2. Browser check waits on absence of dirty markers that can occur before async
   refresh finishes. Assert actual replacement/refreshed form and cleared value,
   not old form; no sleeps, weakened assertion or swallowed failure. Full later
   provider/date/Committed/Ended/unrelated-order draft flow must execute.

## Execution Status and Boundary

Both authorized source findings are corrected; complete browser and coupled
contracts pass. Final complete core discovery passes: 1048 run, 934 passed,
114 existing skips, zero errors/failures. An earlier invocation forced tempfiles
inside the repository and hit unchanged privacy guards; the final invocation
uses normal CI temporary-directory behavior, without source/guard changes.
Coordinator does not implement source.
Investigate both supplied reproductions, make one surgical batch, run smallest
named tests and actual complete browser, then complete core suite because supplied
full discovery failed. Configured relevant static/diff/JSON/hash checks required.
No new SQL needed absent SQL/domain change; historical SQL75 stays historical.
Hardened image required only if application runtime bytes genuinely change.
Fresh web rules before any web edits/check, source-format inherited versus
introduced findings if applicable. No second Review/self-Pass or operational
approval. No rebase/force push/main write/merge/issue or board mutation.

## Remaining Work

Source corrections and required validation are complete. Coordinator owns
fresh base/identity checks, coherent commit/normal push/PR397 update.
This is the final authorized source correction cycle; substantive additional
issues must be reported, not silently expanded into a third cycle.

## Actual Reproduction and Surgical Implementation

P03-T01/P03-T02 continuation within the authorized final correction boundary.
Before editing, both exact manifest tests were executed from `src/core`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests ../../.venv/bin/python -m unittest test_needs_inventory.NeedsInventoryTests.test_scenario_scope_keeps_full_application_evidence_unavailable test_scenario_manifest.ScenarioManifestTests.test_current_iteration_is_complete_and_honest -v
```

Actual result: 2 run, 0 pass, 2 errors, 0 skips. Both raise
`ValueError: Scenario manifest: stale source hash: src/core/tests/dataset.py`.
The existing `synthetic.scenario_manifest.validate_manifest` computes SHA-256
over each exact allowlisted public source. There is no separate refresh CLI;
the existing source-binding mechanism is a content digest plus strict validator.
`sha256sum src/core/tests/dataset.py` returned
`a54612aa549cd5d048281a875b4c80a3a26b22e6d59c9c83d080eebbc8760dc5`.
Only that source row is refreshed. Manifest version, iteration, authority,
inventory, fixture/defaults and all full-journey unavailable claims are unchanged.
No fixture or validator assertions are edited. Index and append-only log record
this provenance maintenance without granting application acceptance.

The actual unmodified browser command was executed from `src/api` three times:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python checks/procurement_browser_check.py
```

Actual local result: 3/3 complete executions passed before correction. The
reviewer's failure is supplied evidence, not a locally reproduced failure;
this invocation confirms nondeterminism rather than claiming failing-first
browser evidence. Source trace in `web/ops.js` shows `go` clears the saved
form's dirty marker before `await capacityView()`, whose API reads precede
replacement. Absence of all dirty markers can therefore observe the old form.
The check now retains the exact submitted form handle, waits for it to detach,
then retains the assertion that no dirty forms remain and asserts the newly
located refreshed form is not dirty and its evidence field is empty.
No sleep, swallowed error, deleted meaningful assertion or runtime edit.
The existing navigation-delay check elsewhere is inherited, not introduced.

No application runtime, domain, SQL or dependency bytes were changed.

## Actual Corrected Validation and Complete Browser Coverage

After the coherent source batch, the exact named command above passed 2/2,
0 skips/errors/failures. The existing complete coupled contracts also passed:

```bash
# From src/core, with project-local scratch for existing tempfile fixtures
TMPDIR="$PWD/../../.validation/issue87-correction-two" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests ../../.venv/bin/python -m unittest test_needs_inventory.NeedsInventoryTests.test_scenario_scope_keeps_full_application_evidence_unavailable test_scenario_manifest.ScenarioManifestTests.test_current_iteration_is_complete_and_honest -v
TMPDIR="$PWD/../../.validation/issue87-correction-two" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests ../../.venv/bin/python -m unittest test_scenario_manifest test_needs_inventory -q
```

Combined module result: 19 run, 19 pass, 0 skips/errors/failures. This includes
existing negative digest/default/authority/status mutation checks, not only a
JSON parse or a suppressed integrity gate.

Actual corrected browser command, from `src/api`:

```bash
TMPDIR="$PWD/../../.validation/issue87-correction-two" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python checks/procurement_browser_check.py
```

Five complete corrected executions passed, including one complete execution on
the final source bytes after retaining the global no-dirty-forms assertion.
Four earlier corrected runs also completed; they are not five final-byte runs.
No partial-flow result is promoted to completion. The last command returned 0
and the existing final PASS message, after executing all these later assertions:

* Manager selected visit `1 Jan 2099`, `Morning` and necessary `Knock and wait`
  instructions displayed before confirmation, with no legacy visit creation.
* Separate resident, staff and capacity manual keyboard confirmations produce
  Committed while preserving the unrelated unsaved threshold draft; refreshed
  confirmation source clears after each successful save.
* Saving that threshold draft detaches the original form before testing the
  refreshed form, no dirty forms and cleared evidence value.
* Separate provider context sees Committed, selected date/period and necessary
  instructions, still without a legacy visit.
* Existing booking/new version and second order proceed. Saving WO-0002
  configuration clears its own field but retains WO-0001's pending offer draft
  and dirty marker. Cancelling keyboard discard preserves it; explicit discard
  clears it through the existing manual path.
* Native labels and 320/390/1280 layouts retain no horizontal overflow with
  reduced motion. Human underlying-home-case closure requires its explicit
  checkbox and cancellable confirmation; accepted closure preserves the
  entire resident-update record and records one closure.
* Both contractor views retain only their own work order and deny package/
  write access. Required contract-version validation and valid keyboard package
  creation execute. Withdrawal then shows the provider Ended and the historical
  selected date/period, rather than a current commitment.
* Existing fixture binds only loopback and public tiny fictional inputs; both
  browser contexts abort all non-fixture requests. Browser and fixture HTTP/
  database resources are closed by existing normal/finally cleanup.

One intermediate corrected run returned PASS despite three server
`BrokenPipeError: [Errno 32] Broken pipe` diagnostics on background GETs during
navigation. They are observed diagnostics, not hidden failures or swallowed
assertions; the final-byte run had no such diagnostics and passed all steps.
The final browser script's main-page error assertion passed.

## Historical Initial Complete Core Invocation: Environment Errors

The configured `.github/workflows/src-ci.yml` core command is complete
`python -m unittest discover -s tests -v`, with no core PYTHONPATH override or
`TEST_AI_CONFIGURED` setting. Existing `.venv` editable distributions/tools were
used without installation; `TEST_AI_CONFIGURED` was absent. No easy-mode test
selection, new skip, AI endpoint, inference or paid service was activated.

Actual command from `src/core`:

```bash
TMPDIR="$PWD/../../.validation/issue87-correction-two" PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python -m unittest discover -s tests -v > ../../.validation/issue87-correction-two/core-full.log 2>&1
```

Actual result: **1048 tests in 261.892s; FAILED (errors=32, skipped=114)**.
There are 23 distinct errored test methods, 911 successful methods, 114 skips,
0 assertion failures and 32 error records because the sensor-fault class test
also records ten failing subtests. Both originally failing manifest methods
pass in this discovery. The supplied historical CI result of 1048/two errors/
114 skips is separate evidence, not this invocation's outcome.

All 32 new error records trace to the existing
`synthetic.stock_fabric._destination` refusal:
`ValueError: Private stock output must be outside the repository`, either
directly or through CLI `SystemExit: 2`/`CalledProcessError`. Existing generator
tests request outputs beneath their tempfile root. This invocation's mandated
project-local scratch root conflicts with that unmodified destination guard.
No private register or real input was read; the affected tests use constructed
registers. No assertion, privacy guard, destination rule or discovery selection
was changed to conceal the conflict. `/tmp`, external scratch, symlinks and
monkeypatched guards were not used to retry this full suite.

Distinct unsuccessful methods, all outside this surgical source change:

| Module/class | Exact method(s) |
| --- | --- |
| `test_generated_dataset.GeneratedDatasetTests` | `test_stock_fabric_and_epc_generators_are_byte_deterministic_with_revision` |
| `test_sensor_faults.SensorFaultTests` | `test_analysis_has_no_truth_profile_config_or_clean_values`; `test_cli_tiny_register_replay_and_validation`; `test_each_class_has_observable_corruption_and_clean_truth` (ten subtest errors); `test_empty_choice_and_nonempty_output_safety`; `test_loader_refuses_new_schema_before_database_changes`; `test_replay_shards_estimate_and_option_order_do_not_change_assignments`; `test_writer_truth_positions_cross_sensors_shards_and_hashes` |
| `test_sensor_privacy.SensorPrivacyTests` | `test_stock_requires_explicit_matching_selection` |
| `test_sensor_stock.SensorStockTests` | `test_all_excluded_is_explicit_empty_output`; `test_cli_estimate_write_parity_and_missing_count_error`; `test_declined_and_unknown_have_no_sensors_or_readings`; `test_destination_and_refresh_refusal_precede_payload_writes`; `test_estimate_is_actual_sample_and_precedes_output`; `test_full_730_day_window_and_register_reconciliation`; `test_long_ids_sql_widths_portable_parameters_and_local_idempotency`; `test_manifest_hashes_sanitized_fabric_and_input`; `test_repeat_bytes_seed_and_date_variation_and_shards` |
| `test_stock_fabric.StockFabricTests` | `test_cli_absent_cases_read_once_invalid_dates_and_refresh_preservation`; `test_cli_determinism_hashes_defaults_and_explicit_failures`; `test_cli_raw_input_provenance_and_label_only_date`; `test_installed_cli_outside_checkout_refuses_destination_repository` |
| `test_synthetic_provenance.PrivacyMutationTests` | `test_register_backed_sensor_snapshot_is_checked` |

The 114 existing skips are 111 opt-in owned-local-MSSQL tests, one explicit
isolated Azure SQL test and two existing JSON-only/rollback distinctions.
No new SQL was requested or started; historical correction-ONE actual MSSQL75
evidence remains historical, expressly not rerun.

This initial run was not green. Parent resolved the environment-only constraint
by using the CI command's normal temporary-directory behavior below, not by
changing source, weakening destination guards or starting another source cycle.

## Final Complete Core Suite: Passed

The parent identified project-local TMPDIR as an added validation restriction,
not a user or CI requirement. Standard tempfile-created directories outside the
checkout are necessary for existing tests to verify the actual private-output
boundary. Tests use synthetic constructed fixtures and existing cleanup; no
private input, shared dataset, destination bypass or symlink workaround is used.

Actual command from repository root:

```bash
cd src/core
env -u TMPDIR -u TEMP -u TMP PYTHONDONTWRITEBYTECODE=1 \
  ../../.venv/bin/python -m unittest discover -s tests -v
```

Actual result: **1048 run in 345.258s; OK (skipped=114)**, 934 passed,
zero errors/failures. This is full unchanged CI discovery, not a narrowed
selection. Both manifest tests pass. Existing skip breakdown remains 111
opt-in MSSQL, one isolated Azure SQL and two backend-specific distinctions.
Parent's first launcher omitted `cd src/core` and exited127 before tests;
the corrected command above ran the suite. No failed attempt is counted passed.
Full log is a noncommitted session artifact at
`/home/azureuser/.copilot/session-state/b9f13d51-f8d3-4fc5-80bb-0e255ec31995/files/issue87-correction-two-core-full.log`.
No production/test source changed between the initial and final full runs.

## Static, JSON, Hash and Runtime Boundaries

Actual configured project commands, run from each corresponding project:

```bash
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
```

Core: lint passed, 70 files already formatted, mypy no issues in 123 files.
API: lint passed, 24 files already formatted, mypy no issues in 56 files.
Final-byte harness checks also passed from `src/api`:

```bash
../../.venv/bin/ruff check checks/procurement_browser_check.py
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy checks/procurement_browser_check.py
```

Final harness type-check result: no issues in one source file. An earlier direct
`ruff format --check checks/procurement_browser_check.py` forced processing of
a file excluded by existing `checks/*.py` configuration and returned 1.
New lines were wrapped locally without reformatting unrelated code. Baseline
and current bytes both return 1 when forced through
`ruff format --check --stdin-filename src/api/checks/procurement_browser_check.py -`.
This inherited forced-format result is not reported as a clean unexempted file;
the actual configured project format gate passes with unchanged exemptions.

`git diff --check` passed. Python JSON parse/deep comparison verified the
manifest differs from HEAD only in the one fixture digest, and recomputed all
four allowlisted SHA-256 bindings successfully. The first 412579 bytes of
`docs/reference/log.md` retain SHA-256
`32be94b555c9b0d739b281ddf9f4ec27fb892ee1e2f339b2c2e3367370950f3e`;
the new entry is append-only.

All 112 tracked files under the five application `src/*/src` roots are
byte-identical to starting HEAD59dce3b6. Their aggregate SHA-256, feeding each
`git ls-files` path, NUL, bytes and NUL in that order, is
`c9d99d0856a4d85852e03952e2a5cb29c57ee35e1f1085fa156fbde9a0f7e272`.
No runtime/domain/SQL/image/dependency configuration changed. A fresh hardened
image and SQL rerun are not applicable, not claimed as newly passed.

No web runtime file was edited and no bounded changed-web source review was
performed. The web-runtime-edit/fresh-guideline/redesign workflow is therefore
not applicable to this Python browser synchronization-only correction. Existing
Fluent/native/WCAG/plain-language runtime, dirty guards and retained evidence
bindings remain unchanged; no fresh web conformance or independent Review is
claimed.

Frozen Review/critique match the hashes in Authorization, including Not accepted.
Original case and memory retain SHA-256
`bf8f4462c41b58c8c92c40dd3ebeeba49eacae59b379daa67ee465ee51fcaadd` and
`6c7d56639cf17a42842efc15a81e412d07adfba5dabe430eb21de9fda8988f43`.
The coordinator-owned state file was not edited by this worker and retains its
opening SHA-256
`793a08f99074b2ea876218c8d976411c1d98e30287c6a92ce2025ffa119e075b`.

## Final Reconciliation, Cleanup and Coordinator Return

Both supplied source findings are addressed in this one final authorized batch.
P03-T01/P03-T02 current plan/details, current changes and correction routing now
separate this invocation from original P01-P03 and correction-ONE receipts.
The earlier correction-ONE receipt has only an appended later clarification;
its prior observed-result bytes are not rewritten. No new phase, acceptance,
Review or critique marker was created. No worker edit to coordinator state.

Final changed-file SHA-256:

| File | SHA-256 |
| --- | --- |
| `src/api/checks/procurement_browser_check.py` | `393422efdb05ad1d6a19c9918e4626f9bf7a34d3b52c49d4fe49ce929a6cc3fe` |
| `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` | `9f54f7e7f1cfc7732ea6c462047847d40bf47d25b9207d586adf52d781f3e3b6` |

Complete-core counts and both repaired methods' successful discovery entries
were checked against the actual log before cleanup. Changed KB relative links
resolve. Final protected-artifact checks passed; HEAD remains59dce3b6 and local
`origin/main` ref remains99056cae (no claim of a new remote fetch).

All synthetic scratch/log files under the exact task-owned
`.validation/issue87-correction-two` directory were removed after transcription;
its empty local parent was removed too. Existing fixture cleanup closed the
browser contexts, synthetic HTTP server and database. No SQL or image/container
was started by this cycle, so no container cleanup or fresh SQL/image result is
invented. No unrelated process/resource was stopped or modified.
`git diff --check` passed after cleanup; only authorized source/KB/artifacts
and the coordinator's pre-existing state change remain in the worktree.

Source implementation and validation are complete for both supplied findings:
final full core1048/934 passed/114 skips, coupled19/19, named2/2 and actual complete
final-byte browser plus configured static/hash checks. Coordinator owns normal
publication, fresh authenticated identity and remote base check. This records
actual execution, not independent acceptance or a change to original Review.
No commit, push, branch operation, PR/issue/AC/board mutation, merge, independent
acceptance, self-Pass, live approval, external inference or paid service occurred.
