---
title: Resident-choice CSV feature-wave checkpoint details (Refs #440)
description: Exact commands, prerequisites, static expectations and recording rules for the later admitted observation
ms.date: 2026-11-11
---

## Admission-gated prerequisites

* RAW = a new directory outside the repository under the session `files/` area, for example `.../files/choice-wave-main-440-observation-1111/` (one file per command: command, start and end UTC, exit, stdout and stderr).
* Private venv `/tmp/ama-440-choice-venv-1111`: `python3 -m venv`, then `pip install -e src/core -e src/agents -e src/api -e src/importer` and `pip install playwright==1.64.0` (the declared dev pin). Needs network to the package index. Preflight first: record the import result in the fresh venv, restore only after an actual import failure, then prove each `zava_forward.*` module origin lies under this worktree and `import playwright` works with the same interpreter that will run B1. Prior attempts failed on a missing Playwright in a private venv and on a private `HOME` hiding an existing user-site install; record rather than hide such a failure.
* `ZF_DATA` unset, `~/.zava-forward` absent before and after, no `.env`, no credential, no provider variable, `TMPDIR` an owned `mktemp -d` removed at the end. All commands under `env -i` with an explicit allow-list: `PATH`, `HOME` (an owned directory, with the Playwright browser cache reached by a symlink to the existing cache, or the real `HOME` only if the cache needs it and the `~/.zava-forward` state is proven before and after), `LANG`, `PYTHONDONTWRITEBYTECODE=1`, the `PYTHONPATH` each row names, and `ZF_*` variables the row names. The browser harness itself passes only `PATH`, `HOME`, `LANG`, `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX` to the server it starts.
* Cached Chromium matching the installed Playwright and `node` must already exist; if not, B1 is blocked, not installed here.
* Axe: `sha256sum` of the pinned asset must equal `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` and read axe 4.10.3. Reuse the existing copy; never refetch.
* Lock: `/tmp/ama-rpi-heavy.lock` free (`fuser` exit 1) and `MemAvailable` at least the 8 GiB headroom rule. Busy is blocked.
* `ZF_BROWSER_SCRATCH` for B1 = a new absolute directory outside the checkout (the harness refuses a path inside the checkout and otherwise writes a legacy `.venv` inside it).

## Selectors, in order (existing tests only; `PYTHON` is the venv interpreter)

Static expectations come from reading source (see the research table) and are re-derived on the actual merged main before the first run. A difference is recorded with its cause, never forced.

| Id | Directory, environment and command | Static expectation | Notes |
| --- | --- | --- | --- |
| C7 | `src/core`, `PYTHONPATH=tests`: `PYTHON -m unittest tests.test_resident_choice_queue -v` | 4 ran | JSON queue projection the CSV copies |
| C1 | `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`: `PYTHON -m unittest tests.test_resident_choice_export -v` | 30 ran (`Serializer` 17, `Http` 13) | New serializer and route; includes the three C1 regressions on the unknown review status |
| C2 | same environment: `tests.test_resident_choice_screen -v` | 9 ran | Node vm double; link, current-page note, no link on load failure |
| C3 | same: `tests.test_role_endpoint_inventory.RoleEndpointInventory -v` | 24 ran (14 own plus 10 inherited from `Matrix`) | Roles against the endpoint inventory including the new route |
| C4 | same: `tests.test_list_export_api.ListExportApi -v` | 11 ran | Shared registry untouched by the new route |
| C5 | same: `tests.test_role_screens_conformance.RoleScreenConformance -v` | 11 ran | `resident-choice` screen block |
| C6 | same: `tests.test_content_standard.CopyAudit -v` | 18 ran | Plain-language audit of changed copy |
| I1 | same: `tests.test_staff_intake_api.StaffIntakeApi.test_inventory_hold_after_capture_is_not_cleared_by_acknowledgement_or_qa tests.test_staff_intake_api.StaffIntakeApi.test_inventory_hold_after_acceptance_refuses_handover_and_a_later_capture_stays_held tests.test_staff_intake_api.JsonStaffIntakeApi.test_inventory_hold_after_capture_is_not_cleared_by_acknowledgement_or_qa tests.test_staff_intake_api.JsonStaffIntakeApi.test_inventory_hold_after_acceptance_refuses_handover_and_a_later_capture_stays_held -v` | 4 ran | The four merged 1432 inventory and QA regressions on the base and JSON-store classes; do not use `-k` (the candidate's `-k` attempt ran 0 tests). `MssqlStaffIntakeApi` not selected |
| B1 | `src/api`, same path variable, `ZF_AXE_JS=<pinned axe>`, `ZF_BROWSER_SCRATCH=<owned dir>`, under ONE `flock -n -E 99 /tmp/ama-rpi-heavy.lock timeout 900 PYTHON -m checks.role_screens_browser_check 232` | exit 0; PASS lines including the download link and attachment checks and the axe check with no violations | The checker has no self-lock. Exit 99 with no story output is a busy lock, recorded blocked. A `SKIP ... axe scan` line means the axe was not run and the result is partial, not a pass |

Sequence: C7, C1 to C6 and I1 first (no lock), then B1 once, never retried. Order of C1 first is allowed if Root prefers the primary selector first; none runs concurrently.

Not selected: whole Capacity and `capacity_browser_check`, whole importer, SQL Server and Docker selectors, `test_case_journey`, story `232s`, full gate, real model, cloud, default dataset. Reasons are in the research. Root may add a selector only with a named affected surface.

## Recording rules for the later documentation step

* Append one section to `docs/architecture/cutover-evidence-pack.md` headed as a dated resident-choice CSV feature-wave checkpoint (Refs #440 #1420 #1432 #80 #73), after the last section, with: identities (actual main, tree, per-directory trees, merged PR numbers and merge commits, relevant blobs, `src` tree compared with candidate `87ea0ed8`, issue and PR states read live, document versions and status, hosted checks stated as read or not read), a document-qualified requirement trace with the classes `local observed`, `implemented but unverified`, `deferred`, `blocked`, `unknown` (Azure observed stays empty), a raw command table with exit, ran, skipped and failure counts and each limit, findings with existing owners, recommendation (continue, fix or proposed pivot, marked proposed for the owner), affected gates (whole #80, #73 and #440 stay open), independent lanes that continue, and a process record.
* Keep candidate-side evidence (PR 1435's 127 focused, story 232 with 42 PASS lines, mypy 2.4.0 and Ruff 0.17.1 results, the original malformed-review-status High finding and the C1 correction) in a labelled "candidate history, not main evidence" paragraph. State that the earlier 1433 checkpoint was observed on `e0dec207d`, not on the CSV integration, and that the four 1432 cases are observed fresh here only if they actually ran.
* Append one entry to `docs/reference/log.md` (never edit earlier entries); touch `docs/reference/README.md` only if an index pointer is genuinely needed.
* Qualify every requirement id by document path, version, status and blob as in the research (BRD, `zava-forward` PRD, never the `proper-warm` PRD unless cited); mark the FR-048 and AC-065 link as partial.
* Quote raw outputs from RAW; correct nothing earlier in place; the witness and model label are asserted, not attested; the native review is not independent.
* State the unrelated exclusions plainly: PR 1435's design does not export all pages, filters or the sidebar list; actual-record export, privacy, retention, resident consent, assistive-technology behaviour and production stay unverified; whole #80, #73 and #440 stay open; the 1420 issue is closed or ticked only by Root after hosted checks and the final acceptance audit, not by this record.
* Check Markdown style (ASCII, `*` lists, no em dashes), relative links and `git diff --check`; confirm `git diff --name-only <main>` lists only the pack, the log and tracking files.
* Before web-facing wording is described as reviewed, the web-design-guidelines source must have been fetched and applied in the owning task; this checkpoint changes no web file and states that it performed no fresh web-interface review.

## Source-unchanged proof (plan launch)

At freeze: the planning commit descends from `1b169fe7d4f9b5a005123c8eb1825028ea431612`, `git diff --name-only 1b169fe7d4f9b5a005123c8eb1825028ea431612 HEAD` lists only `.copilot-tracking/` paths, and the `src`, `docs`, `infra`, `tools` and `.github` tree ids of the planning commit equal the pin ids recorded in the research.
