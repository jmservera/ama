<!-- markdownlint-disable-file -->
---
title: Versioned asset cache headers phase details
description: Evidence and completion expectations for local RV-001 correction
ms.date: 2026-10-31
---

## Metadata

* Task ID: 12a8273a-1cfb-42aa-ae85-97f032ffafbd.
* Task slug: versioned-asset-cache-headers.
* Related plan: .copilot-tracking/plans/2026-10-31/versioned-asset-cache-headers-plan.md.
* Evidence: .copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md; C1-C9.
* Initial direction: shared cache contract only; no source edits before critique.
* Boundaries: local synthetic requests, no Azure/secrets/push/workflows; no UI changes.
* Blockers: none for candidate drafting.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Shared cache policy and regressions | Complete | P01-T01, P01-T02 |
| P02 | Validation and reconciliation | Complete | P02-T01, P02-T02 |
| P03 | Review and local persistence | Review complete; persistence pending | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Shared cache policy and regressions

* Context: C1/C3-C6 show one shared Asset object and three route callers; query currently discarded by headers.
* Intent: immutable only for single current version; safe no-store/no-cache elsewhere.
* Targets: static_assets.py, server.py, resident_demo/app.py, resident_preview/app.py, tests/test_static_assets.py, two checks and README.
* Dependencies: single independent critique resolved.
* Completion evidence: exact handler response matrix and coherent diff; no unrelated behavior.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Query-aware shared headers

* Add snapshot version to Asset constructed by StaticAssets; its headers accepts raw query with default empty string.
* HTML precedence must remain first; use parse_qs with keep_blank_values=True and exact list equality to one current version.
* Employee passes existing parsed url.query to 200 and 304; residents obtain query via urlsplit(self.path) while retaining existing route selection and guard ordering.
* Keep ETags, wildcard/weak validator semantics, byte responses, MIME and HEAD framing.
* No new errors or silent exception handling introduced.
* Completion: all three app branches select one policy for current/old/bare queries, including conditional HEAD.
* Unresolved: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Coverage and documentation

* C7 existing CacheContract loops real rendered dependencies on all handlers; update current-version exact header and validator assertions.
* Extend requests for bare, stale, blank, unrelated, duplicate current/old values and encoded current value; exercise GET/HEAD/304 plus no-store HTML query.
* Add at most three focused methods; test changed release rejects earlier version for immutable caching while retaining original snapshot bytes.
* C8 asset-cache check: normal navigation in same browser context must reuse every current versioned script/style without additional origin request; explicit conditional request separately asserts 304, ETag and policy.
* C9 workspace check: preserve bare Leaflet no-cache assertion and add rendered versioned Leaflet immutable assertion.
* README states one-year policy, exact-current-version boundary, obsolete current-byte compatibility and process restart behavior.
* Completion: tests remain API-owned outside package, no removals, no changed UI or dependencies.
* Unresolved: none.

<!-- rpi:phase id=P02 -->
## P02: Validation and reconciliation

* Intent: run owner-selected verification on actual changed source and existing local browsers.
* Dependencies: P01 source/test/docs done.
* Outputs: external session artifacts, concise durable command outcomes in changes.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Requested commands and browsers

Run from src/api:

```bash
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python3 -m unittest discover -s tests -q
ruff check
ruff format --check
```

* Use the same source paths for focused unittest and browser modules.
* Relevant browsers: asset_cache_browser_check, workspace_scripts_browser_check, chat_submit_browser_check; no live browser/sign-in/model.
* Serialize heavy runs with /tmp/ama-rpi-heavy.lock; existing checks own loopback app lifecycle.
* Store output in new external directories under session files; do not overwrite failure evidence.
* If unavailable dependency blocks a command, preserve failure and restore missing dependency without relaxing pins/contracts.
* Actual first full run exposed three missing-dependency errors (azure.eventhub and API distribution metadata) and thirteen subtest failures from one existing test_ui_support versioned-script header expectation. Restore existing distributions in isolated external venv and update only that directly related assertion, then rerun focused selectors before the full discovery.
* Completion: zero exit for required commands and selected checks; no assumption that unrun browser suites pass.
* Actual completion: restored focused selectors 73 tests passed; final exact discovery 1430 tests in 502.331s, OK with 320 existing skips. Ruff check and format passed. All three selected browser modules passed again in restored environment.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Evidence reconciliation

* Mark actual completed tasks in plan and details; record files/commands/results and justified deviations in changes.
* Confirm no workflow changes, no remote/cloud activity and no unrelated dirty files.
* Preserve original adverse findings and distinguish source completion from publication/live acceptance.
* Completion: ready-for-Review handoff has no conflicting active task markers or validation claims.
* Actual completion: plan P01/P02 markers checked, source diff and final external logs/results bound in changes. P03 remains pending one independent Review and parent local persistence.

<!-- rpi:phase id=P03 -->
## P03: Review and local persistence

* Intent: independent post-implementation assessment once, followed by parent-owned local commit.
* Dependency: reconciled P02.
* Boundary: independent reviewer read-only except one dated Review artifact.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review

* Activate rpi-review in fresh worker with plan/details/research/critique/changes/source boundary.
* Assess full requested source task, exact header/query semantics, regression results and unperformed checks.
* Record execution separately from outcome; no repeat review or current-task source fixes after findings.
* Completion: one Review artifact and routed findings, without human/live/publication acceptance claims.
* Actual completion: one independent Review, execution Complete / outcome Conformant with justified divergence, zero actionable findings. Source diff identity and final evidence hashes independently verified; no source repairs or repeated Review.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Local commit

* Parent records Review outcome and updates state; obtains gh api user id/login for local privacy-safe email.
* Stage only task files; commit with Refs #568 and exact required Copilot trailer.
* Verify local commit content/author/committer/trailer and status. No push.
* Full publication gate and exact-head/human/hosted approval remain unperformed because publication is excluded.
* Completion: local candidate and original dated RPI evidence committed, clean worktree.
