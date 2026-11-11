# Changes: #134 extension E4 (first of three new cycles)

Start source 89a5c5d74def9035eae7af9861e1a97aa5274003; plan commit 763d159ad0034cb83326dc7baf45a278adce6954. Local origin/main a3862eed4a32 not integrated. Owned: src/api/checks/connected_home_browser_check.py, src/api/tests/test_connected_home_check.py. No README, workflow, helper, product or manifest change; the scenario manifest does not reference this checker (search in research), so no digest change.

## Source
* The unconditional sys.path.insert(0, core/tests) is now an append only when the path is absent, so unittest discovery keeps api/tests first.
* New regression test_importing_the_check_keeps_api_tests_first_for_discovery: a fresh subprocess (cwd src/api, canonical PYTHONPATH) discovers this module then test_dependency_rule.py with one loader, prints the loaded module path as its own receipt, and the test requires it to be src/api/tests/test_dependency_rule.py with no failed import.

## Evidence (fresh directory /tmp/z134/e4-20261111T200508Z; each command has .out .err .exit)
| Name | Exit | Note |
| --- | --- | --- |
| red-discover | 1 | Canonical discovery on unchanged 89a5: ImportError, dependency_rule from src/core/tests. Genuine RED. |
| red-regression | 0 | Mislabelled: noclobber refused my checker swap, so this ran the repaired checker (a GREEN run). Retained unrenamed. |
| red2-regression | 1 | Genuine RED: the 89a5 checker bytes (sha256 in red2-checker-hash.out) fail the new test with the same ImportError; source restored and hash-checked after. |
| green-unit | 0 | tests.test_connected_home_check, 13 tests |
| green-discover | 0 | canonical python -m unittest discover -s tests -v from src/api: 2852 tests, OK, skipped 589 (pre-existing skips, not examined or changed). The new test ran and passed under it. |
| green-ruffcheck / green-ruffformat / green-mypy | 0 / 0 / 0 | touched files; mypy 234 files |
| green-browser | 0 | flock -n -E99 timeout 900, once: 142 PASS, 0 FAIL, empty stderr; Chromium 156.0.8078.4, standalone (append path exercised) |

Identity: venv /tmp/z134/venv python 3.12.3 (hosted CI used 3.12.16), playwright, mypy and ruff origins in identity.out; zava distributions are editable installs of this worktree. Axe not run. Hashes: hash-before.out, hash-after.out.

## Limits
No hosted run here; the hosted result for the repaired head is unobserved. Python patch differs from CI. No whole connected-home, demo, live, AT or human acceptance; R1 unresolved; keyboard-probe drift unrepaired. Prior records untouched. E4 spent; E5 and E6 not admitted.
