<!-- markdownlint-disable-file -->
# Changes: #185 Registry adapter extension E1

Registered 2026-11-10 BEFORE `implement-start` and before any source edit (source clean at `c7cfb463`). Task `185-iot-registry-azure-e1`. Plan: [plan](../plans/2026-11-10-iot-registry-azure-185-e1-1110-plan.md).

## Authority and E1 debit (durable)

* Owner grants: 2026-11-09T08:00:39Z (default five total per issue) and 2026-11-09T08:02:51Z ("add 5 additional cycles to exhausted issues").
* Root reconciliation 2026-11-10: #185 exhausted before the grant (certain historical debits at least 7 by 2026-11-06, strict 14 to 15); eligible by dated fact, no named list. Historical spent cycles and overage are preserved, not reset or retroactively approved.
* Extension before E1: 5. This batch is E1 and consumes it. Extension remaining after E1: 4. Further batches require a Root selection; no fresh default five and no new extension.
* The independent review of `c7cfb463` (REQUEST_CHANGES: High inventory, Medium context leak) is a correction of the Nov 10 initial increment and is charged here, not called initial work.

## Dated historical table (preserved from the 1344 audit)

| Date | Source | Commit | Class |
| --- | --- | --- | --- |
| 2026-11-01 | #647 | `67043a15a`, `3cdd3eab7`, `509abde04`, `eaa2a8f0e` | certain corrections (rounds 1 to 4) |
| 2026-11-01 | #647 | `4a2a21834` | certain correction after review |
| 2026-11-01 | #647 | `2df7d3b72`, `227256592`, `caffc6a86`, `91f67ee4f`, `7f416380c`, `822559d4a` | review-thread fixes, charging undefined |
| 2026-11-03 | #849 | `e34b8678e` | certain correction |
| 2026-11-03 | #849 | `2b0b6ffd2` | small correction, charging undefined |
| 2026-11-06 | #1205 | `a7d4e956d` | certain forward corrective cycle |
| 2026-11-10 | #185 | `c7cfb463` | initial increment, debit 0 |

## Files changed

* `src/core/src/zava_forward/core/synthetic/device_registry_azure.py`: F1 bounded confirmation of every entry without a string `statusReason`; F2 `__suppress_context__` on `RegistryError`.
* `src/core/tests/test_device_registry_azure.py`: red regressions then green; fixture update.
* `src/core/README.md`: minimal residual wording only.

## Implemented (2026-11-10, after `implement-start` 13:55:01Z)

* `device_registry_azure.py`: `RegistryError.__init__` sets `__suppress_context__ = True` (F2). `list_run` confirms every entry without a string `statusReason`, enrolled or not, by one `_read`, within `device_identity.MAX_DEVICES` (100) reads per call; present and exactly marked is returned (even when not enrolled), present unmarked or absent is excluded, denied or unreadable refuses `ACCESS_DENIED` or `UNAVAILABLE`, and the 101st ambiguous entry refuses `LIST_INCOMPLETE` before reading (F1). Docstring updated. No new code, SDK method, provider, permission or manifest policy.
* `test_device_registry_azure.py`: replaced the test that encoded the omission with `["SYN-A1","SYN-B1"]` plus unmarked and other-run exclusion; added unreadable-confirmation refusal, budget bound and exhaustion (exactly 101 GETs, no PUT or DELETE), whole-run teardown refusal `TEARDOWN_MANIFEST_INCOMPLETE:1` with no DELETE through the real SDK path, and a 13-path caller-handler traceback test. `test_list_run_returns_exactly_the_marked_identities` now expects the one confirmation read of the explicit-null SYN-B2 entry.
* `src/core/README.md`: list and error bullets and the limits sentence updated (bounded confirmation, refusal beyond 100 ambiguous entries, context object remains reachable).

## Validation (focused tier; isolated throwaway venv `/tmp/e1venv`, pip only, outside the repository)

* Provenance: `azure-iot-hub 2.7.0`, `six 1.17.0`, `ruff 0.17.1`, `mypy 2.4.0`; `azure.iot.hub` imported from the venv; `device_registry_azure` imported from this worktree `src/core`.
* RED on frozen source (`c7cfb463`) before any source edit: 4 tests failed (3 list tests: hidden SYN-B1 omitted, 1 GET instead of 101, `RegistryError not raised`; and the teardown test: `DeviceIdentityError not raised`), and all 12 refusal scenarios of the caller-handler test printed `CALLER-PRIVATE-SENTINEL-185` via "During handling of the above exception".
* GREEN after the source edit: `test_device_registry_azure test_device_identity test_device_provision test_dependency_rule` 89 tests OK (the original 85 plus 4 net new); Root `reproduce_functional_findings.py` 2 tests OK; `ruff check .` clean; `ruff format --check .` 233 files already formatted; Core `mypy` 286 source files no issues (includes the adapter and its tests).
* Impacted selectors: only the three Core device test modules and the dependency rule reference these contracts. `src/api/tests/test_live_control.py` matches the word "device_identity" only in a test name and uses none of these modules, so no API selector applies.
* Not run: the full Core `discover` (stopped by a 290s timeout, no result claimed), full or `--changed` gate, cloud, SQL, browser, scanners, hosted CI. No live Registry, identity, credential or token operation; no Azure service behaviour observed.

## Divergences and amendments

* The "unmarked entries trigger one read each" consequence (critique 1) also covers an explicit-null `statusReason`; one existing test assertion was updated accordingly. No other divergence from the plan.

## E1 status

E1 consumed by this batch. Extension remaining after E1: 4. No further correction is authorized by this record.

