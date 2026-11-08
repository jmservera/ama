---
title: Issue 79 changes, continuation r17
ms.date: 2026-11-07
---

Task `issue-79-r17-align-post-891`. Planning commit `7e4bf6373` (pre-rebase hash `02c0368bc`) precedes the rebase.

## Base and refs

* Final base: `origin/main` `0f420dc9514db22081cb48fa733267d9d33a0d24` (score-only bot commit after 891 merge `312fa3dcc`). Scorer run 42361331168 on `312fa3dcc` completed `success` (waited about 1 minute); main was re-fetched twice and did not move. A scorer run 42361843532 on another head `c80bfc3e` completed `failure`; it is not this topic and was not investigated.
* Preserved refs: `preserve/issue-79-pre-r17-align` = `11fb73f4543b1ccf12d11eded0b3fdee766ffb90` (previous local head); `preserve/issue-79-r17-planning` = `02c0368bc823454d906251ddd3a42dea0dc110af`. Remote topic and PR 1239 remain `181a1c1bb`.
* Command: `git rebase origin/main`; 19 commits replayed, no conflicts, none skipped. HEAD before the records commit: `7e4bf6373afca29c8030fbb0746c7cc66fe28609`, tree `39f342b8fd437e0a341358339d415dc5c4bfffd6`.

## Fidelity proof

* `git merge-base --is-ancestor origin/main HEAD` true; `git rev-list --count origin/main..HEAD` 19.
* `git range-diff preserve/issue-79-r17-planning...HEAD`: 18 commits identical (`=`), one changed (`92d73ce81` to `c331ed911`, the first `docs/reference/log.md` append, whose context moved with main's 891 entry).
* Blob comparison of the 64 non-log topic paths against the preserved head: 0 differences.
* `docs/reference/log.md` against main: 15 additions, 0 deletions; main's 891 entry is intact.
* Source drift relative to the preserved head is exactly main's 891 and rubric changes (13 paths: 891 records, `.github/rubric/scores/latest.json`, log, activation record, `src/api` README, chat widget CSS and JS, browser check, chat panel test).

## Checks (logs under `/tmp/79-r17-1106/`, `PYTHONDONTWRITEBYTECODE=1`)

| Check | Exit | Result |
| --- | --- | --- |
| publication and runner tests (`core.log`, `/tmp/zf79venv`) | 0 | 49 tests OK |
| API wiring test (`api.log`) | 0 | 15 tests OK |
| API chat panel test (`chat.log`) | 0 | 53 tests OK, 1 skipped (existing) |
| Ruff check, format check (pinned 0.17.1, `/tmp/79-align-r13-1106/venv`) | 0, 0 | clean, 214 files formatted |
| mypy 2.4.0 | 0 | no issues in 268 files |

## Limits

* No FULL, browser, SQL or heavy lock use. The 891 browser check was not run. Receipts r14, r16 and child r13 do not cover this head; the coordinator's single `--stack parent --stack tip` gate on final main is required.
* Pushing this rewritten topic needs an owner-approved lease push; PR 1239 is unchanged. Independent exact-head review, hosted CI, policy signoff and Legal retention remain unproven.
