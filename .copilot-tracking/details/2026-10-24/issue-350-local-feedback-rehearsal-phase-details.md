<!-- markdownlint-disable-file -->
---
title: Issue 350 local feedback rehearsal phase details
description: Concrete steps, success checks and stop rules for the local rehearsal
ms.date: 2026-10-24
---

## Phase 1: Prepare isolated runtime

* Runtime root `/home/azureuser/rehearsal-350` (outside the repository): venv with pip editable installs of core[sql], agents, api (no PYTHONPATH=mvp).
* Container `ama-350-feedback-sql`, image `mcr.microsoft.com/mssql/server:2022-latest`, port published as `127.0.0.1:<random>:1433`, random SA password in a 0600 file under the runtime root, memory bounded.
* Fixture: `dataset.DATA` plus coordinator contractor/coordinator staff written to `fixture.json` in the runtime root. Database `zf_feedback350` created on that container only.
* Success: server health 200 on loopback; store reports tables.

## Phase 2: Exercise real behavior

* Login as Sam (RLO), Pam (programme manager), contractor; read `/api/me`, `/api/cases?view=all`.
* Anonymous API, wrong-password login, forged `X-MS-CLIENT-PRINCIPAL*`, `X-Forwarded-*` and forged cookie requests return 401/denied and no data.
* Role denial: contractor cannot read another role's case or programme view.
* One allowed action: `POST /api/cases/ZF-1/call`; reload; audit entry.
* Restart: stop server, start a new process, same SQL; the action persists. Also restart the SQL container and confirm.
* AI: `POST /api/cases/ZF-1/ai` and `/api/ai/priority` with no model configured must fail closed without inference; ordinary case work still works.
* Browser: Chromium via existing Playwright at 390 and 1280 px: sign-in, queue, case open, call logged, no console errors.
* Stop rule: a real defect triggers a focused failing test, a surgical fix and at most two correction cycles.

## Critique amendments (2026-10-24, see critique artifact)

* Environment contract for every server process: `ZF_DATA=/home/azureuser/rehearsal-350/fixture.json`, `ZF_STATE=/home/azureuser/rehearsal-350/state`, `ZF_STORE=mssql`, `ZF_SQL_AUTH=password`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_PORT`, `ZF_SQL_DATABASE=zf_feedback350`, `ZF_SQL_USER=sa`, `ZF_SQL_PASSWORD`, `ZF_SQL_TRUST_CERT=1`, `ZF_PASSWORD`, `ZF_BIND=127.0.0.1`, `PORT`; `AI_ENDPOINT` unset.
* AI check: `POST /api/cases/ZF-1/ai` with `{"task":"summary"}` and `POST /api/ai/priority`; expect 200 template/manual result with `model: null` and no outbound call.
* Contractor denial: external fixture adds a second contractor company case and staff; assert the first contractor gets 404/no data for it.
* Hand-off states that choosing a staff email selects a role under a shared password: not identity proof.

## Phase 3: Owner-facing server

* tmux session `ama-350-feedback`, `ZF_BIND=127.0.0.1`, `PORT=8350`, `ZF_PASSWORD` random in the 0600 file, `ZF_ENV` unset (password mode is refused in production).
* Health evidence by curl from loopback; `ss` proves the listen address.
* Disposable helpers (test servers, browser) stopped; the SQL container stays because the owner server needs it.

## Phase 4: Evidence and gate

* Changes artifact records commands and results. Commit evidence, fetch main, run `tools/rpi-checks.py --all`, verify receipt, independent review artifact.
