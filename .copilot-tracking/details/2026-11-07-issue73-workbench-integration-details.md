---
title: Issue 73 workbench integration details
ms.date: 2026-11-07
---

Companion to `.copilot-tracking/plans/2026-11-07-issue73-workbench-integration-plan.md`. All phases are PENDING; nothing here has been run.

## Phase 1: re-baseline checklist

* `git fetch origin`, record `origin/main` and the topic head. List changed paths of every merge since `23b26a7f3a4693cd20dcf0447303d97491096cb3`.
* Flag as dependents: `src/core/src/zava_forward/core/store.py`, `exception_register.py`, `exception_queue*.py`, `src/api/src/zava_forward/api/server.py`, `role-screens.js`, `app.js` and `src/api/tests/test_exception_register*.py`.
* Confirm the merged child commit is a single `feat(api)` change confined to `role-screens.js` and tests with `Refs #135` only.

## Phase 3: static integration assertions (cheap, no service)

* The data-operator `roles` equals `screenManagers`; `registerRoleScreen` has no new screen id.
* The new block contains one `<a>` and no `method`, `POST`, `fetch(`, `innerHTML` or form control.
* `overview` callers: only the data-operator screen uses `rows` and `c`; the screens at the other two `overview(signal)` sites are unchanged.

## Phase 4: browser observation scenarios (synthetic constructed data only, local server)

* S1 default load of `#/screens?screen=data-operator` as a manager: link present, no `/api/exceptions` request recorded.
* S2 activate link by keyboard (Tab then Enter): exactly one GET `/api/exceptions`; panel heading, status banner, access and sources render; focus is not lost.
* S3 constructed failed AI, quarantined and fell-back items plus a workflow-only note: kind wording and Quarantined versus Fell back to rules or template; no model result implied; no model or network call other than the GET.
* S4 constructed source conflict: both values with source, date, version, owner; eligibility Unknown; no winner.
* S5 empty and `roles_not_named` states: text says this is not an all-clear.
* S6 forced 403, 500, malformed body and network failure (route interception in the browser only): no rows, truthful panel, alert role.
* S7 stale: navigate away before the response resolves; nothing from the old request renders; navigating back re-requests.
* S8 non-manager role: screen not offered and API not requested.
* S9 keyboard and reflow: tab through table regions (focusable, visible focus), 320 px and 1280 px widths, no horizontal page scroll beyond table regions, reduced motion respected.
* Record browser build, viewports, steps and results actually seen; screenshots are evidence only, not AT or WCAG conformance.

## Tier-change triggers (stop and seek coordinator instruction)

* Any edit to server, store, auth, schema, model, infrastructure, dependencies or `ZF_EXCEPTION_STAFF` semantics.
* Widening screen `roles` for named non-manager stewards (owner decision; conflicts with the no-inferred-authority rule).
* Any new write, replay, release, recovery control or model call.
* Failing child gate requiring non-UI changes.

## Publication constraints (later, authorized only)

* Resolve the author with `gh api user`, build `{id}+{login}@users.noreply.github.com`, set repository-local `user.email` and use it for author and committer. Commit with the trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Child PR targets this topic with `Refs #135`; parent PR targets `main` with `Refs #73` and `Refs #135`. Neither uses a closing keyword. Each lists unmet criteria.
* Preserve the older anchor branch `feat/case-workbench-integration-73` (commit `56eec7369`, already main ancestry); it is not this topic.

## Refresh 2026-11-07 (post-merge)

* Phase 1 done: topic at `d17aee537ec267162af106e14056440274ae589d`, `origin/main` `23b26a7f…`.
* Phase 3 implemented as `HostIntegration` in `src/api/tests/test_exception_register_screen.py` (H1 to H5 of the plan). Phase 4 browser scenarios S1 to S9 remain DEFERRED pending a new coordinator admission.
* Heavy-class checks not run: `tools/rpi-checks.py --changed`, `Register` and `Endpoint` classes, browser. Light checks run are listed in the changes record.
* Publication constraints unchanged; this task commits locally only (author and committer `8036360+jmservera@users.noreply.github.com`, canonical Copilot trailer).
