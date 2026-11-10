<!-- markdownlint-disable-file -->
# Issue 189 C1 research: correction of the original independent Functional review (2026-11-09)

Task `issue-189-simulator-control-c1`, parent `issue-189-simulator-control`. Cycle C1 of five TOTAL correction cycles (four remain after this productive cycle; no reset or extension). Head `522adc3946f754a86f48747bd00fb0911434e469` (clean), base `df8e858b2150198e5e22c73d224a0d3592c73daa`. Research disposition: `executed` (targeted reading of the existing source plus bounded reproduction for F3). Planning Readiness: `Ready`.

## Input and preserved adverse evidence

Original independent Functional review (coordinator file `independent-189-controls/functional-findings.json`): `request_changes`, 1 High, 2 Medium. All three findings are preserved as adverse. The original author Review artifact (`reviews/2026-11-09/simulator-control-189-review.md`, "no significant findings") is retained unchanged; it is superseded in outcome by the independent review but not edited or deleted. The original plan, details, critique, changes and state artifacts are frozen.

## F1 (High): view-only administrator mutates the control

Evidence read:

* `server.py` POST dispatch calls `simulator_admin.handle` at the hook placed before the existing `u.get("view_only")` refusal, a deliberate path-specific exception recorded in the original plan.
* `auth.py:158` sets `view_only=not staff_assigned` for the trusted-proxy principal: an administrator with no staff assignment is view-only; an administrator with a staff role is not.
* `simulator_admin.handle` authorizes only `app_admin is True` plus a verified identity; no `view_only` check, so the module does not defend this boundary by itself.
* `workbench.navigation` marks `#/simulator` "available" for every administrator; `test_entra_authoritative` was edited to expect that, and `test_simulator_admin` encodes a success start for an administrator alone. Those tests and the navigation state encode the bypass.

Decision (owner brief, no new authority): keep the existing server `view_only` denial in force for the simulator POSTs and add the same denial inside the module handle (defence in depth). No new permission, capability, allowlist or owner approval is inferred or created. Valid authority stays "administrator plus an existing staff/write role" (`view_only` false). Read-only `GET` status stays available to every verified administrator.

## F2 (Medium): Stop missing for readable expired or invalid-window controls

`simulator-control.js` renders the Stop form only in the `state === "send"` branch, so an enabled but expired or beyond-maximum control shows only Start, and an already stopped control shows no Stop. The module already stops any parsed control (idempotent for disabled, error `NOTHING_TO_STOP` only when unparseable). The screen must expose an independent confirmed Stop form for every parsed writable control, with the loaded revision, without requiring Start first.

## F3 (Medium): unresolved selected-suite error

Original evidence: whole `src/api` discover, 2103 ran, 365 skipped, 1 error in `ConsumptionApi.test_assistant_completion_preserves_capacity_quarantine_and_terminal_release` (subtest `model='other-model', capacity=False, revoked=True`). The producer was piped through `grep`, so the traceback and the Python exit status were lost; they cannot be recovered without a full rerun, which is excluded. The original label "unrelated" was unproven.

Bounded reproduction in C1 (raw outputs in `/tmp/c1/*.txt`, summarised in the C1 changes artifact; no full suite rerun, no filtering of the producer exit status, no skip or waiver):

* Head, single test, `.venv`: exit 0, 1 test OK (9.4 s). PYTHONPATH `tests:../core/tests:../agents/tests`.
* Head, ordered predecessors `test_accessibility_baseline`, `test_ai_boundary`, `test_ai_call_site_inventory` then the single test: exit 0, 25 tests OK.
* Head, `discover -p "test_a[a-i]*.py"` (every module loaded before and including the one in question, 110 tests): exit 0, OK (76 s).
* Pinned base `df8e858b2`, isolated worktree and fresh venv with editable installs from that worktree: single test exit 0; same discover prefix exit 0, 110 tests OK (99 s).

Conclusion: the original error is NOT reproduced at head or base with these bounded reproducers, and its cause is NOT established. It stays an unresolved selected-suite error with a lost traceback; neither "unrelated" nor "flaky" nor "baseline failure" may be claimed. Not run, deliberately: the full suite (excluded by the brief). Residual risk: ordering, import-time state, time or load interaction from modules after the prefix cannot be excluded.

## Web guidelines (changed UI)

Read in full `.github/skills/web-design-guidelines/SKILL.md` and fetched the source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (HTTP 200, 8055 bytes, sha256 `d246b026f4f29b5823a9cc857f9edf3d2507002e055e32040cadeaf3b38e0234`) in this parent session. Rules that bear on the changed Stop form: form controls need labels (checkbox shares one hit target with its label), destructive actions need confirmation, specific Title Case button labels, errors with a next step, async updates announced (`role=status`/`alert`), no `outline: none`. Repository overrides apply (Fluent 2, plain-language content standard, WCAG baseline, ASCII punctuation, native semantics, non-colour status, manual path retained). The original independent reviewer lacked fetch tools; this retrieval is parent evidence and does not make a fresh complete independent web or assistive-technology review.

## Scope, integration and unverified items

* Targeted tier only: modified and impacted auth, admin, live-control, workspace, priority, browser/axe and static tests. No full gate, cloud call, private `ZF_DATA` or global install.
* `origin/main` is now `ad679b96b` (#1295 merged); the branch base `df8e858b2` is its ancestor and `git diff --name-only df8e858b2 origin/main` lists no `src/api` path (157 files changed elsewhere, including the #1141 agents adapter), so the touched files are unaffected. #1292 is not on main. No refresh or merge is made in C1; an ordinary merge is only for final host integration, which waits for #1292 on main. No unmerged #1292 copy and no implicit stack.
* Unverified and manual: SMB flock on Azure Files, mounting the control share into the API, budget alert reference (AC3, no schema field), live cohort/job acceptance. No schema, infrastructure, financial, consent, professional, job, model or role authority is added.
