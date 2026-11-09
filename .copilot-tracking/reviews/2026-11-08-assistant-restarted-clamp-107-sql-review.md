---
title: Issue 107 restarted clamp actual SQL execution review
description: Author review of the focused actual MSSQL run of three process methods; prior unexecuted reviews are preserved
ms.date: 2026-11-08
ms.topic: reference
---

Continuation of the [focused plan](../plans/2026-11-08-assistant-restarted-clamp-107-focused-plan.md) and [focused review](2026-11-08-assistant-restarted-clamp-107-focused-review.md), which left actual SQL unexecuted. Those records are not regraded.

## Admission and run

* Admission: the issue 86 holder was gone and `/tmp/ama-rpi-heavy.lock` was free (`flock -n` probe). The component then ran under `flock -n /tmp/ama-rpi-heavy.lock` for the whole container lifetime, stdin `/dev/null`, with no queue.
* Source: HEAD `8fac72f8934448b63acc5586deb54f610c8b45d3`, tree `8edc62409eac2536614400e912b3f5c63e2991e3`, main `0f05e9aae70768def8d1d9c300215f9ee2f11638`, ignored-inclusive clean. The run used `git archive HEAD` and a fresh venv installed with `--require-hashes`, then `--no-deps` core, agents and api. Modules resolved inside that venv (`.../g107-clamp-sql-r1/venv/lib/python3.12/site-packages/zava_forward/core/assistants.py`).
* Engine: owned loopback container `mcr.microsoft.com/mssql/server:2022-latest` (Microsoft SQL Server 2022 RTM-CU27-GDR 16.0.4305.5), generated password never logged, driver `mssql_python 1.15.0`, readiness on attempt 7. Container removed by trap (`docker rm` exit 0, no labelled container remains).
* Command (from `src/api`): `ZF_TEST_MSSQL=1 PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest -v` with the three exact `test_assistant_release.MssqlUnleasedRevocation` selectors. Script exit 0, unittest exit 0.
* External evidence: `/home/azureuser/.local/share/ama/gates/g107-clamp-sql-r1/` (`sql.err` verbose output, `sql.exit`, `ready.out`, `driver.out`), `g107-clamp-sql-r1.sh`, `.console`, `.runexit`.

## Results

| Method | Result |
| --- | --- |
| `test_restarted_processes_keep_partially_used_allowance_and_stop_at_stored_calls` | ok |
| `test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance` | ok |
| `test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment` | ok |

`Ran 3 tests in 10.883s`, `OK`, zero skips. No SQLite proxy or skip-shaped pass.

## Boundaries

* No source, test or tool change; this record is the only addition after the run, so the executed source equals the final source and the new records alone differ.
* Not run: `--all` or `--changed`, other SQL suites, browser, images, scans.
* Fixture authority is not human approval. Open: fresh hosted CI on the final head (inspect selection and skips), independent exact-head review, whole 107/104, real AI, attestation, budget and human release approval.
