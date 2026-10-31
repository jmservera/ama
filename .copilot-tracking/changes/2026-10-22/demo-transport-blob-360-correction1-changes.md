# Changes: #360 correction1

* Plan: `.copilot-tracking/plans/2026-10-22/demo-transport-blob-360-correction1-plan.md`; critique dispositions applied (PC-001 to PC-006).
* Base head under correction: 829890010f693cceeb82bc82c2254b85019ef4c1 (run5 receipt is historical evidence for that head only).

## P01 Credential binding (complete)

* `infra/scripts/staff_azure.py`: `ProfileCredential` obtains storage tokens only through `cli.call`, so the selected or fallback `AZURE_CONFIG_DIR` applies; cached, never logged; generic errors `from None`; scope allowlist. `default_container(url, cli)` primes the token under a bounded deadline (restores `cli.deadline`) and sets connect 5 s, read 15 s, retry 2. `DefaultAzureCredential` removed.

## P02 Operation budget (complete)

* `infra/scripts/staff_blob.py`: `_bounded` daemon-thread deadline, `PREFLIGHT_BUDGET` and `READ_BUDGET` 45 s, server `timeout` on list and download. Preflight expiry keeps "no job was created"; read expiry is "unverified". `execute` passes the job deadline to `read_result`; the existing finally cleanup is unchanged.

## P03 Tests, docs, validation (complete)

* `infra/tests/test_staff_azure.py`: real `ContainerClient` built via the real `Azure` fallback profile with patched `subprocess.run` (asserts `AZURE_CONFIG_DIR`, no ambient credential), token failure and leak tests, scope refusal, stalled preflight list, stalled download, stalled list during read, failing download, exhausted deadline, server timeouts, and `execute` passing the transport. Stalled cases assert job cleanup.
* Docs: `infra/README.md` correction subsection, evidence pack row, append-only `docs/reference/log.md` entry.
* Validation: infra suite 390 OK; ruff check/format and mypy clean.

## Divergences

* None from the revised plan. Live token acquisition, real latency and live routing remain NOT RUN.
