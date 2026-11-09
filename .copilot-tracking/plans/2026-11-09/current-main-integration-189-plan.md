<!-- markdownlint-disable-file -->
# Issue 189 current-main integration plan (2026-11-09)

Research: [research](../../research/2026-11-09/current-main-integration-189-research.md). Details: [details](../../details/2026-11-09/current-main-integration-189-details.md). Critique: [critique](current-main-integration-189-critique.md). Parent: C4 (four of five cycles spent per brief; one remains; integration is not a correction and neither consumes nor resets a cycle). Refs #189 only.

## Objective

Ordinary `--no-ff` merge of actual `origin/main` `3a9767d5c` (#1240) into `feat/demo-simulator-control-189-1109`, composing the C4 optional-SDK fix with the merged lifecycle Core, preserving both source and RPI intents and published ancestry. Verify that the API controls still work on an SDK-free API base install against current Core types. No source correction.

## Phases

* [ ] P1 Commit this prospective research, plan, details and critique (one) before any merge or validation (frozen).
* [ ] P2 Preconditions (clean tree, HEAD is the frozen record commit, local noreply identity, fresh fetch, re-pin main); `git merge --no-ff origin/main`; no rebase, reset, stash, amend or force. A source conflict or intent ambiguity stops the work.
* [ ] P3 Pin differences and source equivalence: the C4 SDK paths (`live_simulator.py`, `test_live_simulator.py`) and all other #189 `src/api` paths byte-identical to `b933c2f60`; `src/core` and `tools` equal to `origin/main`.
* [ ] P4 Composition read: `Store.audit` signature and the lifecycle Core imports; no streaming SDK import in the merged Core.
* [ ] P5 Selected checks (owner demo-targeted tier), nonqueued, scratch in an owned `mktemp -d`:
  * Actual isolated SDK-free API base install (fresh venv, `pip install` of `src/core` and `src/api` only, then proof that `azure.iot.device` is not importable) and the scrubbed-server regression from `tools/`.
  * `tools` `test_rpi_checks` (includes 1312 cases).
  * API `test_simulator_admin test_live_control test_live_simulator test_iot_stream test_iot_credential_hygiene test_sensor_consistency` (with the declared SDK where the tests need it, in a separate owned venv) and API-base subset that does not need the SDK.
  * CI-profile strict API mypy 2.4.0, Ruff 0.17.1 check and format over affected source, tests and the browser checker.
  * One controlled synthetic browser run (`simulator_control_browser_check --axe` pinned asset) only after the holder check and one nonqueued admission; not repeated unless it fails.
* [ ] P6 Changes record, one original Review of the integration delta, state, evidence-only commit, handoff `handoff-189-current-main-integration.md`.

## Success criteria

* Clean worktree; merge parents are the frozen record commit and `3a9767d5c`; no resolution edits unless recorded.
* Final evidence-only head is source-equal to the tested merge. All selected checks exit 0 or each failure is a recorded blocker (not waivable).
* Skips and missing prerequisites reported as unverified, never passed. No SQL, cloud, model, private data, cost.

## Out of scope

Push, PR, issue/board write, rebase, new source, SQL services, `rpi-checks --all`, global installs.

## Stop rule

A source conflict, intent ambiguity or new defect records scope and the cycle count and stops with no correction until separately authorized.
