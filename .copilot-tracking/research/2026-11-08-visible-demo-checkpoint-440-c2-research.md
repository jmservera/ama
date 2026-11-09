---
title: Visible-demo integration checkpoint 440 C2 research
ms.date: 2026-11-08
---

## Scope

C2 correction of candidate `d8cda455ca804b9b96c9a7dd55e7fb43b805e1d1` (tree `a43de72a049078a9b394ebd6643c16e58254bd7d`), session `9dfa8bcc-4468-4888-be6a-d543c459c94f`. Original `fcbd81e8`/`398a1b6c` and C1 `844884247`/`d8cda455` research, plans, critique, changes and author Reviews stay unchanged.

## Current identities

* `origin/main` fetched again: `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`, unchanged. Worktree clean at start.

## Independent assessment (preserved adverse evidence)

Coordinator file `review-440-visible-d8cda-independent.json`, read completely: verdict request_changes, 0 Critical, 0 High, 1 Medium, 2 Low. C1 F2, F3 and F4 were found addressed.

* R1 Medium (pack line 3243): the first sentence says the stored route calls `ChatModel` once per turn, contradicting the later "at most once". Own source check: `src/core/src/zava_forward/core/chat_panel.py` lines 583-591 show the refusal branch (`out_of_scope`) and the limit-reached branch return before any model call; the model is only invoked when `sources and self.model is not None`.
* R2 Low (line 3266): the BRD/PRD trace row says real-provider and human acceptance are not shown, which can read as no real provider observation. The pack already records one real generic model answer on deployed e2ece revision 27.
* R3 Low (C1 research line 8): the file says "Written 2026-11-08T20:10Z" but Git records research/plan commit `844884247` at 2026-11-08T20:08:47Z and implementation `d8cda455` at 20:09:18Z. Ancestry proves the committed plan preceded the correction commit; the stated wall-clock time conflicts and its cause is unknown. No timestamp witness exists and none is asserted.

## Limitations

* Findings come from the coordinator report plus the own source check above. No test, SQL, browser, model, Azure or hosted check is run in C2.
