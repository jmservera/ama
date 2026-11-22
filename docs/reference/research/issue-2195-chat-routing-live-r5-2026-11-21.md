---
title: Issue 2195 live routing, axe run and chat 500 fix
description: Live routing proof on revision 0000043, the pinned axe run, evidence that the chat 500s recur, and the local statement-serialisation fix with a per-criterion table
ms.date: 2026-11-21
ms.topic: reference
---

## Scope

Issue #2195, synthetic demo, desktop only. Live apps `ca-cutover-test-demo-api` (revision `--0000043`) and `ca-resident-demo`, Playwright Chromium, credentials read at run time and never printed. No Azure change. Probes and outputs: `issue-2195-chat-routing-live-r5-2026-11-21/` (`probe.py`, `live_routing_probe.json`, `resident_probe.py`, `resident_probe.json`, screenshots, `axe-results.json`).

## Live routing (employee)

| Question | Routing line shown |
| --- | --- |
| Can you check the grant claim and invoice? | Routed to the Funding evidence agent. The question is about grant, claim and funding evidence. |
| Which stock should we prioritise by EPC ranking? | Routed to the Stock prioritisation agent. The question is about stock facts and which homes to look at first. |
| Is the grant claim quality checked and which defect? | Handled by the General agent. The question fits more than one agent, so the general agent answers it. |
| Tell me what you can help with | Handled by the General agent. No specialist agent matches this question. |
| Approve the funding claim for this home | Handled by the General agent. No agent can do this. A person takes that action in the workflow. |

The quality question did not produce a routing line in this run because the first thread creation and ask returned 500 (see below); r4 recorded the quality route as proven on revision 0000042. Replies carry the AI-unavailable fallback text and `Model calls: 0`. The resident run routed "How is my case going?" and "Which documents do I need to upload?" and kept the weather question with the General assistant (`resident_probe.json`).

## Pinned axe run

axe-core 4.10.3 obtained with `npm pack` and verified against the repository pin (sha256 `880970c0...a68bb`). `python -m checks.employee_chat_browser_check --axe ... --out ...` printed PASS; `axe-results.json` holds three dialog states (model unavailable, cited answer, demo disclaimer) with 0 violations each. This closes the r4 gap for the employee chat dialog. The check runs on a loopback synthetic app, not the live apps.

## The chat 500s recur

In the live run, `POST /api/chat/threads` returned 500 three times and one `.../ask` returned 500, then 200 on retry. Container console logs for the same minutes show `ProgrammingError` for `POST /api/chat/threads`, `POST .../ask`, `GET /api/map` and `GET /api/briefing`, each beside concurrent `/healthz` requests. r4 saw none; this reverses that finding.

Hypothesis (not confirmed, the driver message is not logged): request threads share one SQL connection and their statements overlap. Fix: `mssqlstore._Conn._run` now holds a per-connection lock, reads each result inside it and returns a buffered cursor. Regression test `SharedConnectionThreads` (fake driver that errors on overlap) fails without the change and passes with it. Limit: an explicit transaction held across statements can still interleave with another thread.

## Local tests

* `src/core`: `test_priority_order`, `test_chat_routing`, `test_chat_panel`, `test_document_rescan`: 261 tests OK, 87 skipped (no SQL).
* `src/api`: accessibility baseline, content standard, resident assistant API: 59 OK.
* `ruff check` and `ruff format --check` clean; `mypy` shows the same 3 pre-existing errors (telemetry import, device_provision).

## Per-criterion table

| # | Criterion | Verdict for the demo | Evidence |
| --- | --- | --- | --- |
| 1 | Routing shown with agent name and plain reason | Proven live (employee funding, stock; resident status, documents) | Tables above, JSON |
| 2 | Unroutable questions stay general and say so | Proven live | Tie, no-match, refused, weather rows |
| 3 | Approval and consent boundaries unchanged | Proven live for the refusal row; no approval or consent code changed | Refused row; diff |
| 4 | AI-unavailable path works | Proven live | Fallback text, `Model calls: 0` |
| 5 | Tests | Proven locally | Test counts |
| 6 | Accessibility and content-standard tests | Proven: automated tests and pinned axe run on the employee chat; person-run assistive-technology testing is out of scope for the demo | Axe results, tests |
| - | Live 500s | Fix proven by unit test only; not deployed, so the live effect and the root cause are unproven. Needs image build, deploy and probe rerun | Logs, test |
