<!-- markdownlint-disable-file -->
# Issue 189 research: admin start/status/stop surface for the finite simulator control (2026-11-09)

Task `simulator-control-189`, initial RPI (not a correction cycle; owner default: five TOTAL review-correction cycles per issue, no reset or renewal, none spent).
Agent: hve-core-all:rpi-agent, Claude Sonnet 5.5. Research disposition: `executed`.

## Pinned identity

* Worktree `/home/azureuser/source/ama-demo-wt/issue-189`, branch `feat/demo-simulator-control-189-1109`.
* Base HEAD `df8e858b2150198e5e22c73d224a0d3592c73daa` (rubric record 78/100, after the #1304 IoT recovery `23e944c1f`), tree `af1e9ea329f7ff5116c1279ab780ef649b1593cd`.
* `git fetch origin main` at 2026-11-09 12:3x UTC: `origin/main` = `df8e858b2150198e5e22c73d224a0d3592c73daa`, equal to HEAD and merge-base. The primary checkout was not used.
* Python: new worktree-local `.venv` (git-excluded through `.git/info/exclude`) with editable installs of this worktree's `src/core`, `src/agents`, `src/api[dev]`. The pre-existing global editable installs point at the dirty primary checkout and were NOT used (first test run failed to import `live_control` through them, which proved it).

## Scope evidence

* Issue #189 (open): AC1 and AC2 ticked (#637, #707, #845); AC3 "Run has an owner, a time limit and a budget alert" unticked. Closure audit 2026-11-03: still unmet "verified live (#146)". Parent #184, depends on #140, related #146.
* `src/api/README.md` ("Bounded cohort and finite run control"): the control schema `live-sim-control-v1` and CLI `start|status|stop` exist; "An in-app admin screen for these controls is not delivered (unmet #189 detail; no UI was changed)". This is the documented gap.
* Demo critical-path audit (coordinator file, 2026-11-09): #189 is "ready source-only" for the admin start/status/stop surface; live AC3 stays unproven; no new simulator or model machinery; keep expiry, cap, owner/reference visibility and manual stop route.

## Existing code to reuse (not duplicated)

* `src/api/src/zava_forward/api/live_control.py`: `parse` (exact field set, 1..100 distinct valid home ids, non-placeholder owner and approval reference, strict UTC stamp), `check_window` (future, at most 14 days), `decide` (send/stopped/expired/invalid), `load`, atomic `write`, fixed `StreamError` codes. It has NO alert-reference field: the schema holds `approval_reference` only.
* `live_simulator.check_capacity(homes, Limits())`: the actual B1 daily budget (400,000 less 40,000 headroom) and slot-overrun guard; returns messages/day, budget, quota fraction and the Hub monthly allocation. The status and start paths call it; no quota or cost arithmetic is copied.
* `sensor_stream.RunBudget` holds owner/cost/alert strings for constructed replays only; it is not connected to the control file, so no live alert can be derived from it.
* `live_simulator` and `live_receiver` re-read the file every slot or two seconds; a stop, expiry or unreadable file ends sending (fail closed). The API surface therefore only edits the same file, it starts nothing itself.

## Auth model facts (src/api auth.py, workbench.py, server.py)

* Trusted-proxy Entra principals carry `app_admin` (app role `ZavaForward.ApplicationAdmin`), `identity_source=entra`, canonical `tid`/`oid`; tenant mismatch, missing OID, or a contractor holding the admin role is denied at `authenticate`. A password-provider user can never be `app_admin`.
* An administrator alone gets role "Application Administrator" and `view_only=True`: `do_POST` rejects every POST except logout with 403 ("shows every option but changes nothing"), and `projection.allowed` lets that role GET only `me`. An administrator who also holds a staff role keeps `app_admin=True` with that role.
* `workbench.navigation` shows administrators every option with `access` "needs a role with this authority". `test_entra_authoritative` asserts every admin navigation entry has that access string.
* Consequence: a start/stop POST for an application administrator needs one narrow, path-specific exception ahead of the `view_only` check. All other POSTs stay refused, and case, resident, finance and export data stay unreadable for the administrator (the status shows cohort size, never home ids).

## Overlap assessment with #1292, #1288, #144, #1296 (before any edit)

* #1292 (`fix/demo-recovery-1292-1109` at `51f2d8731`, merge-base `23e944c1f`): its only `server.py` hunks are in `POST /api/ai/priority` and the resident-decision handler (about lines 1239 to 1262), and its only `app.js` hunks are in `priorityPanel` (about lines 691 to 722). Everything else is `src/core` (store, sqlstore, mssqlstore, continuity) and tests.
* Planned 189 host hooks: `server.py` GET (after the `/api/governance` entry area, about line 410) and POST (between the CSRF check and the `view_only` check, about line 1135), `app.js` in `missingWorkspaceScripts` (about line 344) and `route` (about line 423), `workbench.py`, `index.html`, `style.css` untouched. All are at least about 100 lines from every 1292 hunk.
* Verdict: same files, line-disjoint hunks, no shared symbol. A trial `git merge-tree --write-tree origin/main fix/demo-recovery-1292-1109` on the unmodified base succeeds (exit 0); the same trial is repeated after implementation. Ordering rule recorded: the new logic lives in separate files (`simulator_admin.py`, `simulator-control.js`, new tests); the host hooks are small and textually disjoint, so 189 does not depend on unmerged 1292 source, copies none of it and makes no implicit stack. If the post-implementation trial or a later 1292 inclusion on main reports a conflict, final 189 host integration and publication wait for 1292 current-main inclusion and the candidate is frozen as partial LOCAL; independent module, tests and research are unaffected.
* #1288 owns readings UI/model/capture flags, #144 worker transport, #1296 policy: none is touched. No simulator, model, provisioning, Bicep or quota-calculation change.

## Truthful status vocabulary (derived from the real schema)

* Owner: recorded in the file, "declared, not identity-verified".
* Time limit: `expires_at` and `decide()` state (sending, stopped, expired, invalid), at most 14 days.
* Approval reference: declared text, not verified.
* Budget alert: the schema has no alert reference, so the surface can only say "Not recorded in the control. No budget alert is verified live (#146)". It never presents the approval reference or any fixture string as an alert. AC3 stays UNPROVEN.
* File missing, unreadable, invalid, not configured or not writable: "unavailable"/"invalid" with a manual route (the CLI and Azure RBAC on the file share); sending stays closed.

## Web evidence

* web-design-guidelines SKILL.md loaded; the current rules were fetched from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` on 2026-11-09 (full rules retrieved, applied in the plan and at Review).
* Fluent 2 design system, WCAG baseline and plain-language content standard in `docs/reference/research/ux/` honoured: reuse `h`, `api`, `show`, `AsyncAction`, native `button`, `label`, `input`, `dl`, `role=status`/`alert`, no colour-only status, copy audited by `test_content_standard` vocabulary rules, no redesign. This is engineering evidence, not accessibility acceptance.

## Planning Readiness

`Ready`. Open questions recorded as assumptions: the API process needs `ZF_SIM_CONTROL_FILE` pointing at a writable path (the deployed job mounts the share read-only and the API container may not mount it; the screen then reports unavailable truthfully, and no Bicep or permission change is made). Cross-process write races are bounded by an in-process lock, an expected-revision check and atomic replace; the file share is single-admin demo infrastructure.

## Follow-ups (current)

1. Authorized operator later mounts a writable control share for the API (infra change, not in scope) and verifies a live AC3 owner, time limit and budget alert (#146). 2. #146 budget alert verification. 3. Browser/axe evidence for the new screen on exact head.
