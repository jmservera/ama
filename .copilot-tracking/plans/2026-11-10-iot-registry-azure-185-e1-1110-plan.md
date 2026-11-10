<!-- markdownlint-disable-file -->
# Plan: #185 Registry adapter extension E1 (inventory completeness and context suppression)

Written 2026-11-10 (after `research-open` witnessed 13:54:04Z). Task `185-iot-registry-azure-e1`. Authority: extension E1 only (extension 5 before, 4 after). Research: [research](../research/2026-11-10-iot-registry-azure-185-e1-1110-research.md). Details: [details](../details/2026-11-10-iot-registry-azure-185-e1-1110-details.md). Critique: [critique](critiques/2026-11-10-iot-registry-azure-185-e1-1110-plan-critique.md). Changes (registered before implement): [changes](../changes/2026-11-10-iot-registry-azure-185-e1-1110-changes.md).

## Scope

Repair only independently confirmed F1 (High, incomplete inventory) and F2 (Medium, caller exception context) in `device_registry_azure.py` with direct regressions in `test_device_registry_azure.py` and a minimal README residual note. No other file, no new SDK surface, code, provider, permission or manifest policy.

## Phases

* [ ] P1 Red: add regressions that fail on `c7cfb463` (F1 hidden non-enrolled marked identity; F2 caller handler traceback). Confirm each fails for the intended reason before editing source.
* [ ] P2 Source: `list_run` confirms every entry without a string `statusReason` by a bounded read within `MAX_DEVICES` reads, refusing `LIST_INCOMPLETE` beyond that; `RegistryError` suppresses ambient context.
* [ ] P3 Existing-fixture update: change the one existing test that encoded the omission; add budget, unmarked-exclusion, unreadable-confirmation and teardown-refusal tests.
* [ ] P4 Validate in an isolated throwaway venv outside the repository: new tests, existing 85 Registry/identity/provision/dependency tests, impacted Core selectors, Ruff check and format, Core mypy including both files.
* [ ] P5 README: replace the omitted-payload residual wording with the bounded-confirmation statement and its refusal limit.
* [ ] P6 Review once, commit locally, freeze clean, handoff.

## Success criteria

* Root repro `reproduce_functional_findings.py` fails on the old head and passes after.
* A successful inventory includes every exactly run-marked identity or the call refuses with a fixed code; teardown never reports success with a hidden marked identity.
* No traceback of an adapter refusal contains a caller exception secret.
* No wildcard, unconditioned or widened destructive path; no new network call types; at most 101 calls per `list_run`.
