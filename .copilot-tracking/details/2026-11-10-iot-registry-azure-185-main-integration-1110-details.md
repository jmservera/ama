<!-- markdownlint-disable-file -->
# Details: #185 main integration (2026-11-10)

Evidence directory: `ROOT/checks-185-main-integration-1110` (outside the repo). Each command logs to its own file with its true exit code.

## Commands (from `src/core` unless stated)

1. Repo root: `python3 -m venv /tmp/i185venv` then `/tmp/i185venv/bin/pip install -e 'src/core[dev]'`.
2. Previous 89 selector: `PYTHONPATH=tests python -m unittest test_device_registry_azure test_device_identity test_device_provision test_dependency_rule`.
3. Root regression: `PYTHONPATH=tests python ROOT/independent-185-registry-initial-1110/reproduce_functional_findings.py`.
4. `ruff check .` and `ruff format --check .` on the configured Core project.
5. Full configured Core `mypy`.
6. Provenance: print `azure.iot.hub.__file__` and the adapter `__file__`.
7. Directly impacted caller selectors only if a merged-main change is found to affect the adapter; none expected.

Not run by design: full Core discover, full or `--changed` gate, API suites, browser, image build, live Azure operations.
