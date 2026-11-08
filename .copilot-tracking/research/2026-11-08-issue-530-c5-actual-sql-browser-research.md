---
title: Issue 530 C5 actual chat SQL and employee browser execution research
ms.date: 2026-11-08
---

* Disposition: executed (read-only). HEAD ce3f27f08 (tree e092d57b), Main 0f05e9aa unchanged on fetch, ignored-clean. Refs #530 only. Original session 225166fc. Admitted: the 21 chat SQL methods and the maintained employee chat Chromium/axe check only.

## Maintained interfaces (trusted source, tools/rpi-checks.py)

* SQL: runner installs `src/api/requirements.txt` with `--require-hashes`, verifies the driver (`SQL_DRIVER`), starts a labelled container (`--label ama.rpi.owner=<token> --memory=3g --cpus=2 --publish=127.0.0.1::1433`, `MSSQL_MEMORY_LIMIT_MB=2048`), waits for `SELECT 1` and `CREATE DATABASE rpi_disposable`, then runs `python -m unittest -v <selectors>` in `src/api` with `PYTHONPATH=<snap>/src/api/tests:<snap>/src/core/tests:<snap>/src/agents/tests`, `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_PORT`, `ZF_SQL_DATABASE=rpi_disposable`, `ZF_SQL_AUTH=password`, `ZF_SQL_USER=sa`, password env, `ZF_SQL_TRUST_CERT=1`. The runner would `docker pull`; this execution does not (image `mcr.microsoft.com/mssql/server:2022-latest` is already local, no pull authorised).
* Browser: `python -c BROWSER_ENTRY checks.employee_chat_browser_check --axe <axe> --out <out>` in `src/api` with `PYTHONPATH=<safety>:<tests paths>`, `TMPDIR` external (the entry patches `TemporaryDirectory` to `$TMPDIR`), safety `sitecustomize` refusing non-loopback `socket.connect`. Axe is pinned: script refuses unless SHA-256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`. Success is the `PASS employee chat: ` line and `axe-results.json` with exactly states actual-model-unavailable, synthetic-cited-answer, demo-disclaimer-model-answer, each with empty violations and positive passes (`check_employee_chat_results`).
* The checker's model-answer states use a controlled synthetic provider response, not a real model or Azure.

## Admission facts at 09:48

* Lock `/tmp/ama-rpi-heavy.lock` unheld (lsof), no sqlservr/chromium/gate processes, no containers. Root free 21154656256 bytes, /mnt 4497403904 (not used), RAM available 8167800832, 4 shared CPUs. Local SQL image cf8f0ab2ebe6.
* r1 failed receipt (SHA-256 15adeeff795d96375f186438b2f101759a8d6ecb8bf799383bdb6615dea104e8) is preserved and is not resumed.

## Limits

* A manual targeted record, not a runner receipt and not a partial or full receipt. Load-only is not execution. No prior 2007-test result is claimed for this head.

## Planning readiness

* Ready.
