---
title: Closure-wave integrated-main checkpoint details (Refs #440)
description: Exact commands, prerequisites, expected counts and recording rules for the later admitted observation
ms.date: 2026-11-11
---

## Admission-gated prerequisites

* RAW = `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/closure-wave-main-440-observation-1111/` (new, outside the repository; one file per command: command, start and end UTC, exit, stdout and stderr).
* Private venv `/tmp/ama-440-closure-venv-1111`: `python3 -m venv`, then `pip install -e src/core -e src/agents -e src/api -e src/importer` and `pip install playwright==1.64.0` (the declared dev pin). Needs network to the package index. Prove each `zava_forward.*` module origin lies under this worktree. No global or shared install, no `.env`, no credential, no provider variable, `ZF_DATA` unset, `~/.zava-forward` absent before and after, `TMPDIR` an owned `mktemp -d` removed at the end.
* Cached Chromium (read previously as build 1248) and `node` must already exist; if not, blocked, not installed here.
* Axe: `sha256sum /tmp/axepk/package/axe.min.js` must equal `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` and the asset must read axe 4.10.3. Reused, never refetched.
* Lock: `/tmp/ama-rpi-heavy.lock` must be free (`fuser` exit 1) and `MemAvailable` at least the 8 GiB previously used as the headroom rule. Busy is blocked.

## Selectors, in order (existing tests only; `PYTHON` is the venv interpreter)

Static expected counts come from reading the pin and are compared with the actual counts. `ran` must be nonzero and equal the expectation, or the divergence is recorded; skips are listed raw.

| Id | Directory, environment and command | Static expected | Notes |
| --- | --- | --- | --- |
| N1 | `src/core`, `PYTHONPATH=tests`: `PYTHON -m unittest tests.test_priority_order.SqliteC4Corrections -v` | 21 ran | 1426 contract on the SQLite store double; MSSQL subclasses not selected |
| N2 | `src/core`, `PYTHONPATH=tests`: `PYTHON -m unittest tests.test_ai_consumption.ConsumptionTests -v` | 34 ran | 1428 core ledger including the joined-reservation case |
| N3 | `src/importer`, `PYTHONPATH=tests`: `PYTHON -m unittest tests.test_import_exceptions.TransferFailureTests -v` | 8 ran | 1426 importer failure messages |
| N4 | `src/importer`: `PYTHON -m unittest discover -s tests -v` (README command) | 82 ran | whole importer suite, Root may restrict to N3 |
| N5 | `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`: `PYTHON -m unittest tests.test_ai_consumption_api.ConsumptionApi -v` | 32 ran | permit timing and attribution on owned fixtures |
| N6 | same environment: `tests.test_unaccepted_handoff_csv_api.UnacceptedHandoffCsv` | 13 ran | CSV bytes, read-only, role and age-limit boundaries |
| N7 | same: `tests.test_handoff_api.HandoffApi tests.test_list_export_api.ListExportApi` | 18 ran (7 and 11) | JSON handoff and shared export path |
| N8 | same: `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 24 ran (14 own plus 10 inherited from `Matrix`; critique PC-001) | every role against the endpoint inventory including `/api/handoffs/unaccepted.csv` |
| N9 | same: `tests.test_case_journey` | 31 ran | Node subprocess journey |
| N10 | same: `tests.test_content_standard tests.test_static_assets tests.test_capacity_browser_check` | 28 ran (18, 5, 5) | plain-language audit of changed `app.js` and `ops.js`, static assets, and `CapacityBrowserCheck` (5 methods, one of which runs a 4-test no-Playwright subprocess; critique PC-003) |
| B1 | `src/api`, same path variable, `ZF_BROWSER_TESTS=1`, unwrapped: `PYTHON -m unittest tests.test_unaccepted_handoff_download_ui -v` | 6 ran, 0 skipped | class self-locks; a busy lock skips and is recorded blocked |
| B2 | same, `ZF_BROWSER_TESTS=1`, under ONE `flock -n -E 99 /tmp/ama-rpi-heavy.lock timeout 900 PYTHON -m unittest tests.test_handoff_read_guidance -v` | 9 ran, 0 skipped | the class has no own lock; read-only and role boundaries in real DOM. Exit 99 with no `Ran N tests` line is a busy lock, recorded blocked; any other nonzero exit is a failure (critique PC-002) |
| B3 | `src/api`, unwrapped, own lock: `PYTHON -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` (no `--mssql`) | exit 0, scenario lines PASS, axe states with no violations | ONE whole run; BLOCKED text means not run |

Sequence: N1 to N10 first (no lock), then B2, B1, B3 one after another, never concurrently, none retried. Each of B1, B2 and B3 acquires the shared lock exactly once and releases it on exit; no outer flock wraps B1 or B3.

## Recording rules for the later documentation step

* Append one section to `docs/architecture/cutover-evidence-pack.md` headed as a dated closure-wave checkpoint (Refs #440), with: identities (head, tree, trees, blobs, PR and issue states, document versions and status), a document-qualified requirement trace table with the classes `local observed`, `implemented but unverified`, `deferred`, `blocked`, `unknown` (Azure observed stays empty), raw command table with exit, ran, skipped and failure counts and the limit of each selector, findings with existing owners, the #132 remaining gap and resume point, recommendation (continue, fix or proposed pivot, marked proposed for the owner), affected gates (whole #80, #73, #144, #131, #132 and #440 open; #1420 expansion waits on the disposition), independent lanes that continue, and a process record.
* Append one entry to `docs/reference/log.md` (never edit earlier entries); touch `docs/reference/README.md` only if an index pointer is genuinely needed.
* State that #1425 (staff intake) and #1422 (household inventory) sit below the four increments on the integrated tree but have no selector here, so the pass or fail result says nothing about them (critique PC-004).
* Quote raw outputs from RAW; correct nothing earlier in place; the witness and model label are asserted, not attested; native review is not independent.
* Check Markdown style (ASCII, `*` lists, no em dashes), relative links and `git diff --check`; confirm `git diff --name-only 8aedb56b5909903abd6c6f84777b49f237c1cbb0` lists only the pack, the log and tracking files.

## Source-unchanged proof (plan launch)

At freeze: `git rev-parse HEAD` is `8aedb56b5909903abd6c6f84777b49f237c1cbb0`, `git diff --name-only 8aedb56b5909903abd6c6f84777b49f237c1cbb0 HEAD` lists only `.copilot-tracking/` paths, and `git rev-parse HEAD^{tree}` of the planning commit differs from the pin tree only by those tracking files; `src`, `docs`, `infra`, `tools` and `.github` tree ids equal the pin ids recorded in the research.
