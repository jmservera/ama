<!-- markdownlint-disable-file -->
# Issue 189 C1 plan: correct F1 (High), F2, F3 (2026-11-09)

Research: [research](../../research/2026-11-09/simulator-control-189-c1-research.md). Details: [details](../../details/2026-11-09/simulator-control-189-c1-details.md). Critique: [critique](simulator-control-189-c1-critique.md). Parent plan: [original](simulator-control-189-plan.md) (frozen). Cycle C1 of five TOTAL; four remain; no reset or extension.

## Objective

Smallest fix that closes the original independent findings without adding authority. Refs #189 only.

## Phases

* [x] P1 F1 source: add `view_only` denial in `simulator_admin.handle` for POST (new code `VIEW_ONLY`, 403, existing wording); move the `server.py` POST hook after the existing `view_only` gate; mark view-only `GET` status `read_only` and not writable; navigation access "needs a role with this authority" for view-only administrators.
* [x] P2 F1 tests: revert the `test_entra_authoritative` assertion edit; module and HTTP start and stop denials for a view-only administrator with a valid revision, CSRF and trusted principal (no file, lock or audit change); success paths use administrator plus an existing staff role; non-administrator denials unchanged.
* [x] P3 F2 screen: independent confirmed Stop form for every parsed writable control (send, expired, invalid window, already stopped); Start independent; view-only message; loaded revision preserved.
* [x] P4 F2 browser check: real browser interaction for expired enabled, invalid window, already stopped, stale, rejected, error and manual (view-only, not writable) states with pinned axe 4.10.3.
* [x] P5 F3: record raw bounded reproduction facts; label the error "unresolved selected-suite error"; no waiver.
* [x] P6 Docs: `src/api/README.md` view-only sentence; C1 changes artifact; coordinator handoff.
* [x] P7 Targeted checks, one authored Review, local commit.

## Success criteria

* A view-only administrator gets 403 on start and stop with no file, sidecar-lock or audit effect, through both the HTTP route and the module; `GET` status still works and reports `read_only`.
* Administrator plus an existing staff role keeps start and stop; non-administrators unchanged (401/403, no disclosure).
* Stop is reachable and sends the loaded revision for every parsed writable control.
* No new permission, capability, allowlist, schema, infrastructure or owner-approval inference.

## Validation (targeted demo tier)

`test_simulator_admin`, `test_entra_authoritative`, `test_auth`, `test_live_control`, `test_workspace_scripts`, `test_content_standard`, `test_design_system`, navigation/priority consumers found by grep, ruff and mypy on touched files, browser check with pinned axe. Not run: full gate, full suite, cloud, SMB flock, live job, private `ZF_DATA`.
