# Issue 1420 correction cycle C1 changes (2026-11-11)

Additive. The original changes record, author Review, current-main validation and the independent report are unchanged. Grant: C1, the first of five (four remain). Amendment written before any edit: `.copilot-tracking/plans/2026-11-11-issue-1420-c1-correction-amendment.md`. Raw evidence: session folder `files/priv1420/c1/`.

## Changed hunks (four files, 66 insertions, 10 deletions)

* `src/api/src/zava_forward/api/resident_choice_export.py`: new constant `REVIEW_STATUSES = (REVIEW, "Reviewed with supplied acceptance")`; `_complete` accepts a review object only when its status is in that closed tuple (explicit `None` still means no review). Unrecognised review statuses now follow the existing unavailable path. The eight-column contract, Core and the projection are unchanged.
* `src/api/tests/test_resident_choice_export.py`: three regressions (serializer unknown and empty statuses, serializer valid and `None` statuses, HTTP projection path through the existing `detail` patch) plus typing: helper `version` and `measure` arguments are `Any` (they deliberately take malformed values), an annotated `broken_homes` tuple, and `App` built in one line with the repository's specific `# type: ignore[no-untyped-call]` (as in `test_case_journey.py`, `test_employee_live_responses.py`).
* `src/api/tests/test_resident_choice_screen.py`: `anchors_of` returns `list[dict[str, Any]]` (import added).
* `src/api/checks/role_screens_browser_check.py`: line 734 `base + (link.get_attribute("href") or "")`, so a missing href fails the preceding href check rather than raising.

Unchanged blobs versus `fa497143c`: `README.md`, `server.py`, `web/role-screens.js`, `test_role_endpoint_inventory.py`. No Core, server, UI, role, schema, registry, Capacity or shared serializer change; no manifest or config change; no new ignore on `server.py`.

## Red then green

* Red: the new regressions run against the unchanged serializer (`priv1420/c1/red.log`): exit 1, 2 failures (`'None recorded' != 'Solar panels: Unknown (evidence unavailable)'` on both the serializer and the HTTP path); the valid-states test passed. This reproduces the High finding by execution.
* Green after the fix: see the validation below.

## Validation (all synthetic, local)

* Own-source imports (`c1/imports.txt`): `server.py`, `store.py` and `resident_choice_export.py` resolve to this worktree.
* Focused selection: 127 tests OK (124 earlier plus 3 regressions), exit 0 (`c1/focused.log`). A first attempt with wrong module paths gave 101 tests and 2 import errors (path setup only; no source cause) and was corrected by adding `src/api/tests` to the private `PYTHONPATH`.
* Four merged intake tests on `StaffIntakeApi` and `JsonStaffIntakeApi` (inventory hold and acceptance, two each): 4 tests OK, no skips, exit 0 (`c1/intake4.log`). MSSQL classes were not run. (`c1/intake-try.log` is an earlier `-k` selection mistake that ran 0 tests; kept as an adverse note.)
* Project mypy, full command from `src/api` including tests and checks:
  * Pinned mypy 2.4.0 (existing exact-pin install, used read-only without installing or modifying it; `--python-executable` the default interpreter for the dependency stubs, private cache dir): `Success: no issues found in 232 source files`, exit 0 (`c1/mypy-pinned.log`).
  * The unpinned mypy 2.4.1 default `python3 -m mypy`: `Success: no issues found in 232 source files`.
  * Earlier result of 13 errors (`final-main/mypy-project.log`) is preserved as the original adverse result. `server.py` remains under the project's existing `ignore_errors` override; it is not fully typed and this cycle neither widens nor removes it.
* Ruff 0.17.1 (pin, existing exact-pin install used read-only): `ruff check` passes on the four changed files. `ruff format --check` passes on the three files this cycle formats; `checks/role_screens_browser_check.py` still reports the single pre-existing hunk at line 225, identical on pinned main `1b169fe7d` (`c1/main-checker-format-diff.txt` equals `c1/checker-format-diff-head.txt`) and left untouched.
* `node --check` on `role-screens.js`: exit 0 (file unchanged).
* Fresh real Chromium 156 story 232, one canonical heavy lock `flock -n /tmp/ama-rpi-heavy.lock` (lock free, nonqueued, harness has no self-lock on this checker): exit 0, 42 PASS lines including both download checks, pinned axe 4.10.3 (sha256 `880970c0...`), no violations, incomplete empty (`c1/browser232.log`). Two earlier attempts failed on `ModuleNotFoundError: playwright` before any browser launched (private venv has no playwright, then the changed HOME hid the existing user-site install); those logs are kept as `browser232-attempt1-import-error.log` and `browser232-attempt2-import-error.log`. The third run used the existing user-site playwright via `PYTHONUSERBASE`; no install occurred. The earlier observation is historical.

## Limitations

* No web or UI file changed in C1, so no new web-guidelines pass was run on changed web files.
* The pinned-mypy run borrows dependency stubs from the default interpreter; the repository's own pinned dev environment was not created.
* No full gate, no hosted CI, no independent reassessment yet, no human acceptance, no live or privacy review. Whole #80 and #73 remain open and no acceptance criterion is ticked here.
