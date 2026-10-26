<!-- markdownlint-disable-file -->
---
title: Issue 350 local feedback rehearsal changes
description: Evidence of the executable local synthetic rehearsal; no repository source change
ms.date: 2026-10-24
---

## Scope and honesty

Local synthetic engineering rehearsal of the existing `src` application only. It is not deployed sign-in, user usability acceptance, operational readiness, AI acceptance or #350 closure. No source file was changed by this rehearsal. The branch already differs from `origin/main` by the earlier published offline-checker work (`tools/check-demo-feedback.py`, `tools/test_check_demo_feedback.py`, dated 2026-10-21 to 2026-10-23 RPI artifacts, PR #436); that is historical, not new maintenance. New in this pass: the 2026-10-24 RPI artifacts and a local merge of `origin/main` f1e2d830 into the branch (merge commit; published history and earlier reviews preserved).

## Environment (outside the repository, `/home/azureuser/rehearsal-350`)

* venv: `pip install -e src/core[sql] -e src/agents -e src/api` (pip only, no `PYTHONPATH=mvp`).
* `make_fixture.py` builds `fixture.json` from `src/core/tests/dataset.py` `DATA`: 6 fictional cases (ZF-1..ZF-6), 5 staff (liaison, programme manager, coordinator, two contractors from different companies). Not the 60,000-home stock fixture and not the 980-case programme.
* SQL Server 2022 container `ama-350-feedback-sql`, published on `127.0.0.1` only (random port; it changes if the container restarts), database `zf_feedback350`, random SA password and app password in 0600 files.
* `run.sh` sets the environment contract from the critique (`ZF_STORE=mssql`, `ZF_SQL_AUTH=password`, loopback SQL, `ZF_BIND=127.0.0.1`, `AI_ENDPOINT` and `ZF_ENV` unset).
* Owner-facing server: tmux session `ama-350-feedback`, `http://127.0.0.1:8350`, `ss` shows `127.0.0.1:8350` only.

## Results (transcripts: `exercise-run.txt`, `persist1.txt`, `persist2.txt`, `browser-run.txt` in the runtime root)

| Check | Result |
| --- | --- |
| Anonymous `/api/me`, `/api/cases`, POST call | 401 |
| Wrong password, unknown email | 401 |
| Forged `X-MS-CLIENT-PRINCIPAL*`, `X-Forwarded-User`, `X-ZF-CSRF` headers and forged session cookie | 401 (password provider ignores headers) |
| Roles: liaison, manager, coordinator | `/api/me` 200; queue lists all 6 cases |
| Contractor `con@` | sees ZF-1..ZF-5; ZF-6 (other company) 404; POST call 403 |
| Contractor `other@` | sees ZF-6 only; ZF-1 404 |
| Allowed action | liaison `POST /api/cases/ZF-1/call` 200; reload shows the contact |
| App restart (new process, same SQL) | contact persists |
| SQL container restart plus app restart | contact persists (`persist2.txt`); `docker inspect` shows the container restarted at 13:31:32Z after creation at 13:29:03Z (port changed 32768 to 32769); `sql-evidence.txt` shows 6 cases, 5 staff and 10 audit rows (`log_contact` x3, `ai_run_*`/`ai_record`) in SQL |
| AI with no model | case summary and priority both 200 `source: template`, `model: null`, reason "AI is not configured"; audit records `source=template model=None`. No outbound inference; this does not replace real-AI acceptance |
| Browser (Chromium, 1280 and 390 px) | `/sign-in` form, 5 queue items for the liaison, case opens with address; no horizontal overflow; console shows pre-login 401, `/api/law/alerts` 503 (law store not configured) and one 403 (unidentified endpoint, not investigated). The regulatory-alerts panel stating "law store is not loaded; rule checks are unknown" was observed in the 1280 px screenshot, not asserted in the script |

Observation (not adjudicated, no change made): any signed-in staff role can log a contact on any visible case; liaison Sam logged a call on ZF-5, owned by the programme manager, and it was audited. The fixture therefore holds three synthetic contacts (ZF-1 intended; ZF-2 from a stray script step; ZF-5) and matching audit rows.

## Limits

* Shared password plus staff email is the existing local synthetic mode: choosing an email selects a role and is not identity proof. It is never available when `ZF_ENV=production`.
* Law store, map tiles, photo tokens, model deployment, time capture and the other #350 prerequisites are absent by design here.
* One browser path and one action are not a usability study.

## Cleanup

No disposable helper process remains; the SQL container and tmux server are deliberately kept for owner use.
