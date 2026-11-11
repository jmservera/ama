# Issue 1420 implementation changes (2026-11-11)

Admitted by `.copilot-tracking/plans/2026-11-11-issue-1420-choice-csv-research-1110-admission-amendment.md`.
Original research, plan, critique and partial witness are unchanged (plan-only launch, commit c50cfa2a).

## Pins

* Integrated main: `a853cce16fafdfe32c7a5fe90f3b0c8b544eef0b` (includes 1433), merge commit `469f60cb6a879a9a21f2931ebca8da40ad0c31cd`.
* Before implementation `git diff --name-only a853cce` listed only `.copilot-tracking` paths, so `src`, `infra`, `tools` and `.github` equalled that main.
* The shared `origin/main` ref later advanced to `064f42f83` (1432) without any action here; no further fetch or merge was done, so that commit is not integrated.
* Research-to-current delta for the nine source files (6d4cd62 to merge): `server.py`, `projection.py` and `resident_decisions.py` changed (1419 handoff CSV, field intake, tenure inventory). None touch the choice queue, role gate, query parsing or `measure_decision_view`; the other six files are unchanged. Judged not an unexpected resident projection, role or query change.
* The one inherited tracking conflict was resolved as Root directed (original plan blob preserved, main bytes taken, hashes asserted); see the integration note.

## Source changes (own files only)

* New `src/api/src/zava_forward/api/resident_choice_export.py`: eight-column page serializer, header-only when empty, closed vocabularies, `safe_cell` on every cell, `TypeError` on an unexpected page shape.
* `src/api/src/zava_forward/api/server.py`: `get_kind` line and one `GET /api/resident/choice-queue.csv` branch reusing the store method, `num()` clamps, 400/403 mapping and the generic 500 JSON wrapper. 1419 registry and dispatch additions untouched; `LIST_EXPORTS` untouched.
* `src/api/src/zava_forward/api/web/role-screens.js`: `choiceDownload` native anchor ("Download this page for Excel", no `download` attribute, no button) with a scope note, shown only after a successful load with integer limit and offset.
* New `src/api/tests/test_resident_choice_export.py` (27 tests); `test_resident_choice_screen.py` (link and failure tests); `test_role_endpoint_inventory.py` (one inventory line); `src/api/README.md` paragraph; `src/api/checks/role_screens_browser_check.py` story 232 gained link and download assertions.
* No core, role, schema, `ops.js`, Capacity checker or `LIST_EXPORTS` edit.

## Validation (focused, local, synthetic only)

* `unittest` of `test_resident_choice_screen`, `test_resident_choice_export`, `test_role_endpoint_inventory`, `test_list_export_api`, `test_resident_choice_queue`, `test_case_journey`, `test_content_standard`: 124 tests, OK. Earlier first runs failed (one serializer test, the inventory regex test, one screen test, one content-standard copy rule on the word "holds"); each was corrected and the first adverse results are kept here.
* `ruff check` clean for the changed Python files; `ruff format` applied to the three new or heavily edited Python files; `ruff format --check` still reports one pre-existing hunk in `role_screens_browser_check.py` (line 222, not mine, left alone). `mypy` (2.4.1, repo pin is 2.4.0) clean on the new typed module. `node --check role-screens.js` OK.
* One bounded real Chromium 156 run, `python3 -m checks.role_screens_browser_check 232`, exit 0, under a single `flock -n /tmp/ama-rpi-heavy.lock` (lock free beforehand, not queued, harness has no self-lock). Pinned axe 4.10.3 (sha256 verified, read from an existing gate copy): no violations, incomplete empty. Log: session `files/priv1420/browser232.log`.
* Not run: full API/Core suites, the full gate, other browser stories, any SQL, cloud, private or default dataset.
