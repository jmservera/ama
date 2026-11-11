# Research: #134 / PR 1455 extension E4 (import precedence)

Task connected-ext4-134-1111, native 360c88c7-7282-4605-abb5-7fdb080cba42. Frozen source 89a5c5d74def9035eae7af9861e1a97aa5274003, tree 653182f7. Local origin/main now a3862eed4a32 (descends from e691255ff; not integrated, no rebase or merge). Owner grant: up to three additional cycles; this is E4, the first. Original five, E1, E2 and E3 stay spent; E5 and E6 are not admitted.

## Evidence read

* Independent report independent-134-pr1455-discovery-cause-1111.json (High, request_changes) and raw hosted log pr1455-first-api-failure-1111-raw.log (ImportError: test_dependency_rule imported from src/core/tests, expected src/api/tests).
* Source: connected_home_browser_check.py line 45 runs sys.path.insert(0, core/tests) at import. The task text names the file quality_connected_home_browser_check.py; the actual file in this branch is src/api/checks/connected_home_browser_check.py (no rename made).
* Canonical hosted command (src-ci.yml line 88): python -m unittest discover -s tests -v from src/api with PYTHONPATH core/tests:agents/tests. Sorted discovery imports test_connected_home_check (which imports the checker) before test_dependency_rule; both src/api/tests and src/core/tests hold a test_dependency_rule.py.

## Findings

* Cause is import precedence: the prepend moves core/tests ahead of api/tests. Not DNS, dependencies, browser or StoreJourney.setUp (journey_snapshot imports lazily at test run).
* The earlier focused runs (python -m unittest tests.test_connected_home_check) never imported the second duplicate bare name, so they could not reproduce it.
* Scenario-manifest registry: a search of tracked non-tracking files finds the checker name only in the checker, its test and src/api/README.md. No manifest recipe digest references it, so no digest change or Core manifest check is needed (record, not assumed).

## Candidate and decision

Replace the unconditional prepend with a guarded append: add core/tests only when it is absent from sys.path. Under canonical CI it is a no-op; standalone use still finds the helper. Rejected: sys.modules deletion, renaming the test, package reshaping, broad catches, workflow edits.

Readiness: Ready. Actionable local engineering; no owner decision outstanding within this grant.
Limits: no whole connected-home, demo, live, AT or human acceptance; R1 unresolved; keyboard-probe drift not repaired.
