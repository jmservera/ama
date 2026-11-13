# Independent critique (rubber-duck), executed once

Verdict: Revise. Findings and dispositions:

* Use bare module names with explicit PYTHONPATH (no __init__.py): accepted. Core: `src/core/tests`; agents: `../core/tests:../agents/tests`; api: `../core/tests:../agents/tests`, plus fixture dirs.
* Record python, setuptools versions, import origins; check `git status --short` after installs and tests for src changes (egg-info is ignored or reported): accepted.
* Offline boundary: setuptools upgrade may touch the package index; the brief mandates it, so failure is reported rather than bypassed. Issue AC text read-only via `gh issue view` as the brief requires; no writes. Loopback sockets in API tests are local only and are reported, not excluded.
* Add test_chat_case_funding_sources to core; dependency_rule tests excluded as boundary tests, not regulatory.
* Evidence: record commands, versions, exit codes, counts, skips, sha256, AC mapping: accepted.
