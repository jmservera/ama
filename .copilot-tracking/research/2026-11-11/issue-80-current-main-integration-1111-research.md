---
title: Issue 80 current-main integration research
description: Ordinary merge of main 0509ddce into PR1423 and revalidation plan
ms.date: 2026-11-11
---

## Source identities

* Before merge: parent `d7d0b9c58c247d3c7771e292f10471348d87fe8f` (tree `b3a71ab3`), clean.
* Fetched `origin/main` = `0509ddcef14d9c2046791b283fad65229f536202` (staff132 #1425). `git merge-tree --write-tree` and the real merge both showed one content conflict, `src/api/tests/test_role_endpoint_inventory.py`; `server.py` and `README.md` auto-merged.
* Ordinary merge committed as `ef16f3e21454b915a46c930a90cc7d3c010bf055`, tree `4168b3139141318c2cb396d237b22123a37e0901`, parents `d7d0b9c5` and `0509ddce`. No reset, rebase, force or discard.
* The earlier trial `b839` (main `b8394cd5`) does not qualify this tree; its results are historical.

## Conflict and resolution

* The conflicting line is the `GET_ENDPOINTS` list. Parent side added `/api/handoffs/unaccepted.csv`; main added `/api/workorders/WO-0001/field-intake`. A scripted assertion confirmed the two sides differ only by those two entries, so the resolution is their union (both approved rows). No other line was changed; the POST list auto-merged with main's staff-intake POSTs.
* No role, authorization, route or server change was made; `server.py` is the git auto-merge of both sides.

## Main 132 delta (b8394cd5..0509ddce, src)

`staff_intake.py`, `projection.py`, `quality.py`, `server.py` (8 lines), `index.html` (+1), `staff-intake.js` (new), staff-intake API and browser tests, `test_content_standard.py`, `test_role_endpoint_inventory.py`, READMEs. Capacity checker and `ops.js` are not changed by it, but `index.html` (served) and `server.py` are, so the earlier capacity whole-run is not source-equivalent.

## Impacted checks

Role endpoint inventory; staff intake API and browser (real Chromium, opt-in), content standard; child CSV 13, UI 6, guidance 9, handoff API; case journey 31, list export 11, static 60; resident API; Ruff, format, mypy, Node syntax for changed JS (`staff-intake.js`, `app.js`, `ops.js`); one whole capacity run because served `index.html` and `server.py` changed. Tests with an internal heavy lock are NOT wrapped in `flock`.

## Limits

* Tested tree is the actual committed merge in this worktree; the tracking-only commit that follows changes no source.
* Native, not independent review; hosted checks not run. Staff132 checkpoint 440 handling, #1420, child 1419 and unmerged siblings are excluded.

## Planning Readiness

Ready. Research disposition: executed.
