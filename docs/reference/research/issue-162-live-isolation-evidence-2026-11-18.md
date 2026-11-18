---
title: Chat and Memory User Isolation Live Proof on the Synthetic Demo (#162)
description: Live probes of the deployed demo showing that anonymous, resident-session and forged-identity requests cannot reach another user's chat or memory, what cannot be proven with one staff identity, and the criterion table
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope

Issue #162 has one unticked criterion (6, administrator and break-glass audit and policy). The owner also asked for live proof that one user cannot read another's chat or memory on the deployed demo. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). DPO and Legal approval, billing reconciliation and person-run assistive-technology testing are not needed for the demo. No `src/` change; tier FOCUSED.

Sign-ins were read from the owner's credential files at runtime and never printed. Thread ids, memory ids (`CM-` ids), the tenant GUID and email addresses are redacted in the retained output. The scripts and output are in [issue-162-live-isolation-2026-11-18/](./issue-162-live-isolation-2026-11-18/).

## What the demo can and cannot test

* Chat threads and memory live only in the staff API (`ca-cutover-test-demo-api`, Entra Easy Auth, `ZF_AUTH=trusted-proxy`). The server derives the owner from the validated principal; no route takes an owner.
* The resident portal (`ca-resident-demo`) signs in with a demo email and password and has no thread or memory routes (live 404, below). It cannot act as a second chat user on the API.
* Only one staff Entra identity is available. A real "user B requests user A's existing thread" test is therefore not possible live. Thread ids are `CT-` plus 16 random hex characters, so a foreign id cannot be guessed.

## Live probes

Raw output: [02-isolation-probe-output.txt](./issue-162-live-isolation-2026-11-18/raw/02-isolation-probe-output.txt) (first run, kept as adverse evidence) and [03-isolation-probe-output-run2.txt](./issue-162-live-isolation-2026-11-18/raw/03-isolation-probe-output-run2.txt) (final). Script: [probe-isolation.py](./issue-162-live-isolation-2026-11-18/probe-isolation.py).

| Probe | Result (run 2) |
| --- | --- |
| No session: GET threads, memory, status, a thread id; POST memory | 302 to the Entra sign-in for all five; no data |
| Resident signs in on the resident app, then GET `/api/chat/threads` and `/api/chat/memory` there | 404, 404 (no such routes) |
| Resident session cookies replayed to the staff API (threads and memory) | 302 to Entra sign-in; the resident session is not accepted |
| Staff session plus forged `X-MS-CLIENT-PRINCIPAL` naming another oid and role | `/api/me` account block unchanged; thread and memory lists equal the staff user's own (own thread and own memory item present) |
| Staff session plus forged `X-MS-CLIENT-PRINCIPAL-NAME` and `-ID` | Same: owner view unchanged |
| GET threads with `owner`, `user`, `user_id` or `email` query fields | 200, own list only |
| POST thread ask with body field `owner`, `user` or `email` | 400 "Only content and skill are accepted." |
| Never-issued thread id: GET, ask, messages, archive, delete | 404 "Not found." for all five |
| Never-issued memory id: edit, delete | 404, 404 |
| Positive controls: own thread GET, own memory list | 200 and the created ids returned, so the 404s are not a broken route |
| Cleanup | Own memory item and own thread deleted; memory opted out (user had not opted in and had no items); counts 0 and 0 before and after; memory status "not opted in" before and after |

Run 1 failed to add a memory item (400, the task was empty), so its memory-view comparison (`same-owner-view: False`) compared against a view with no item added and is not a denial finding. Its own thread and the opt-in were cleaned in that run too (counts 0 and 0, status "not opted in" after). Run 2 supplied the assistant task `stock-prioritisation`.

Screenshots in [shots/](./issue-162-live-isolation-2026-11-18/shots/):

* `staff-app-before-probes.png` shows the signed-in staff workbench (desktop 1440 by 900) before the probes. A second capture taken after the probes was byte-identical and was removed as a duplicate. It shows the session was live; they are not proof of any denial.
* `resident-signed-in-resident-app.png` was taken mid-sign-in and shows the "Still signing you in" state of the resident portal, not a signed-in page. The cookie names `__Host-zfdemo` and `__Host-zfdemo-csrf` printed in the raw output are the evidence that sign-in succeeded.
* `login-staff.png` is the staff landing after Entra sign-in; it is a near-duplicate view of the workbench and is kept only as the sign-in-landing label.

## Local proof for what is not provable live

`python3 -m unittest tests.test_chat_isolation` from `src/api` (33 tests, OK, rerun today; Observed; raw output not retained). `test_every_endpoint_is_owner_scoped_and_denies_cross_user` covers a second user against every chat and memory endpoint; `test_injection_cannot_cause_tool_calls_exposure_or_writes` covers injection.

## Criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1. Queries keyed by the authenticated user in the server | Ticked; live part Proven (forged identity headers and client owner fields do not change the view) | Probes above; `server.py` `_chat` |
| 2. Role matrix covers every chat and memory endpoint and denies cross-user | Ticked; live cross-user read of a real foreign thread Unproven (one Entra identity); proven locally | 33 tests OK (Observed; raw output not retained) |
| 3. Retrieved context uses the same field projection | Ticked; not exercised live (needs a model-backed answer and a second role) | Local tests only |
| 4. Never shared into another user's prompt | Ticked; not exercised live (needs two users and a model call) | Local tests only |
| 5. Prompt injection cannot cause tool calls, exposure or writes | Ticked; not re-run live | Local test set only |
| 6. Admin and break-glass audited with purpose, policy decided | Partly proven; left unticked | [Break-glass live proof](./chat-breakglass-live-proof-2026-11-18.md): refusals audited live; grants unproven live; policy decided for the demo only |

## Limits and disclosure

* Live proof of denial is for anonymous, other-system and forged-identity callers and never-issued ids. It does not show a second authenticated staff user being refused a real foreign thread.
* The staff user's memory opt-in was switched on then off during the run; the final status equals the initial one.
* The scratch cookie files `/tmp/state-*.json` were deleted after use.
* Process error: this worker overwrote the earlier run's `issue-162-live` research and state files and restored them with `git checkout` before continuing under `-live-r2` names (see the r2 research note). The `research-open` witness record at 12:43:17Z points at the restored original state.
* No cost-bearing Azure action was taken; no resource was created.
