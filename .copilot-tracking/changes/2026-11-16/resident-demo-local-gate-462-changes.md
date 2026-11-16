---
title: "Changes: resident-demo-local-gate-462"
description: "Implementation and verification evidence for the Issue #462 local candidate"
ms.date: 2026-11-16
---

Status: complete. Base `5e0c7f74432ffce73cfeaa672e4e40a605ca6274`, branch `feat/resident-demo-rpi-gate-462`. No source code changed: every local check passed on unchanged main code. No Azure access, deployment, spend, push, PR or merge occurred.

## Files changed

| File | Change |
|------|--------|
| `docs/reference/research/resident-demo-threat-model-2026-11-16.md` | New: threat model (T1 to T10) |
| `docs/reference/README.md` | Index row for the threat model |
| `docs/reference/log.md` | Appended 2026-11-16 entry |
| `src/api/README.md` | Link to the threat model from the showcase section |
| `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-16/`, `rpi-sessions/2026-11-16/` | RPI evidence and state |

## Dependency and preview evidence

* #444 is CLOSED; PR #455 is MERGED (2026-10-25T21:25:42Z). `git diff --stat 5e0c7f744 -- resident_preview.py resident_preview_browser_check.py` is empty: previews are untouched.
* The rubric history was not edited, rerun or bypassed. Whether the historical failed rubric counts as resolved is left to the coordinator.

## Local verification

Run from the worktree. Packages were imported from the worktree through PYTHONPATH because the installed editable packages point at another checkout.

| Check | Command (abbreviated) | Result |
|-------|-----------------------|--------|
| Lint, format, types | `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/api` | Pass (core 272 files formatted, 325 typed; api 221 and 305) |
| Core unit | `unittest tests.test_resident_showcase tests.test_resident_showcase_verifier` | 50 tests OK |
| API unit | `unittest tests.test_resident_demo_api test_resident_demo_check test_resident_demo_script` | 65 tests OK |
| Infra unit | `unittest tests.test_resident_demo_deploy test_resident_demo_secrets test_secret_lifecycle` | 52 tests OK |
| SQL Server parity | throwaway `mcr.microsoft.com/mssql/server:2022-latest` (image id `sha256:cf8f0ab2ebe6...`) on 127.0.0.1 with `ZF_TEST_MSSQL=1`, `unittest tests.test_resident_showcase_sql` | 40 tests OK, 0 skipped (27 skipped without the container) |
| Browser journeys | `checks.resident_demo_browser_check` | 79 PASS, 0 FAIL |
| Browser journeys | `checks.resident_account_check` | 4 PASS, 0 FAIL |
| Browser journeys | `checks.resident_summary_browser_check` | 1 PASS, 0 FAIL |
| Existing preview | `checks.resident_preview_browser_check` | 58 PASS, 0 FAIL |
| Docker non-root | `checks.resident_demo_image_check` (builds `Dockerfile.resident-demo` from head 5e0c7f744) | Pass: image user 10001:10001, process uid 10001, read-only root, no capabilities, refusals echo no secret, health, forged and wrong-password 401, fake sign-in and sign-out |

The SQL container password was a random throwaway value in a mode 600 temporary file, shredded afterwards and never written to the repository. The container was removed.

## Not done or not claimed

* Azure spend record, resource plan, deployment and live browser acceptance (issue criteria 6 and 7): need owner pre-spend approval; out of scope.
* Hosted checks and the coordinator exact-head assessment.
* Human accessibility, copy and Legal or DPO review.
* The complete exact-head gate runs after the candidate commit; its external receipt path and verification are reported in the final response, not in this committed file.
