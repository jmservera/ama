---
title: Issue 153 stale-stage advance refusal research (continuation)
ms.date: 2026-11-12
task_id: 153-blocked-copy-readiness-1112
task_slug: employee-denial-copy-153-1112
---

## Relationship to the original record

Continuation of the same RPI task and session. The original record `2026-11-12-employee-denial-copy-153-1112-research.md` (commit `aded42cb4`, NOT_READY for the safety-stop reason) is preserved unchanged. It wrongly treated the stale-stage refusal as out of scope because "the button only appears at that stage". A second authorized actor can advance the case after the first client renders, so the refusal is reachable. This file corrects that reasoning from the earliest affected point.

Target change recorded prospectively: this unpublished child now targets `feat/demo-ux-integration-1112` (parent `43b2187b918206666c63cb25d8b338be09791118`, which contains `59eac8951`; its `store.py` is identical to this worktree's). The original main-target notes remain historical. The worktree was not rebased or moved. Funding is excluded and no role is assigned.

## Reproduction (synthetic fixture only)

Script `/tmp/i153/race.py`, output `/tmp/i153/race-out.txt` (complete, untruncated). The first attempt exited 1 with `ModuleNotFoundError: No module named 'playwright'` in the venv; its output file was overwritten by the rerun, so only this description survives. The rerun followed `pip install playwright==1.64.1` into the same venv. Real `ThreadingHTTPServer`, core fixture ZF-3 made advanceable with the same contract/work-order/appointment fixture used by `api/tests/test_mvp.py`, Chromium via Playwright.

1. Client A (Sam, Resident Liaison Officer) rendered `#/case/ZF-3`: Final checks card "Everything is in place." with button "Ready to book the installation".
2. Client B (Pam Lead, Retrofit Programme Manager) POSTed `/api/cases/ZF-3/advance`: `200`, stage `Install booked`, `waiting_on` Kim Builder, case `owner` Sam Example (Resident Liaison Officer).
3. Client A clicked its old button: `POST /api/cases/ZF-3/advance` returned `400` with `{"error": "This case is not at the final checks."}` and no `reasons`.
4. Client A screen: `p.err` and status region read exactly "This case is not at the final checks." The stale Final checks card and button stayed rendered; no owner, no next action, no hint that someone else moved the case.

## Contract check

* Reason: present but terse; it does not say the case may already have moved on.
* Owner: absent from the message. The existing contract knows the case owner (`c["owner"]`, shown on the screen as "Case owner" and used in sibling gate messages "Owner: <name>"), so no new role assignment is needed to state it.
* Next action: absent. The existing safe path is to refresh the case and check its history, the wording already used for the recorded/uncertain history barrier.
* No structured `reasons` exist for this branch, so the client catch block (app.js lines 1021 to 1026) renders only `e.message`. Wording at the single server raise site is the smallest change; no client, status code, permission or gate change is needed.

## Finding

A distinct literal criterion 3 gap is reproduced for one confirmed non-funding denial: the stale-stage refusal states a reason without an owner or next action. Planning Readiness: Ready for a one-line wording change plus a regression. Funding, safety-stop role naming, resident wording and proposal cards remain out of scope. Criteria 2, 3 (universally) and 5 remain unproven.
