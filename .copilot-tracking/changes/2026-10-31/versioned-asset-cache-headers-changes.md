<!-- markdownlint-disable-file -->
---
title: Versioned asset cache headers changes
description: Local implementation, validation and Review handoff for RV-001
ms.date: 2026-10-31
---

## Metadata

* Task ID: 12a8273a-1cfb-42aa-ae85-97f032ffafbd.
* Task slug: versioned-asset-cache-headers.
* Related plan: .copilot-tracking/plans/2026-10-31/versioned-asset-cache-headers-plan.md.
* Phase details: .copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md.
* Implementation date: 2026-10-31.

## Execution Status

* Status: Complete for full plan; source, validation, independent Review and local persistence complete.
* Completed markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02.
* Remaining active-plan markers: none.
* First boundary: P01-T01 shared headers and three callers; source writes only after Ready critique disposition.

## Execution Summary

Implement exact-current-version immutable static caching, preserving existing freshness, route guards and conditional HTTP. Approved write boundary is the plan's source/tests/checks/README and task artifacts; no UI, Azure, secrets, workflow or remote writes.

## Completed Work

### Shared query-aware response policy

* P01-T01: Asset retains its immutable snapshot version; headers parses a single matching current `v`, preserving blank values.
* Files: static_assets.py, server.py, resident_demo/app.py, resident_preview/app.py under src/api/src/zava_forward/api.
* All three handlers pass request query to shared policy for GET/HEAD/304; route guards, validators and response framing unchanged.
* HTML still returns no-store before parsing; bare/stale/ambiguous values revalidate.
* Completion evidence: coherent source diff; focused tests pending P02 after test/check batch.

### Focused regression matrix, browser assertions and guide

* P01-T02: existing actual-handler matrix now tests exact current/bare/stale/blank/duplicate/other versions and GET/HEAD/304 policy, no-store HTML with current query and wildcard validator.
* Added one focused ReleaseIdentity method for decoded current version, query ordering and retained old snapshot/new bytes; no removals or new test files.
* Browser check preserves legacy warm-cache turnover and failure recovery, observes normal-navigation origin counts for immutable reuse, then sends explicit conditional GET and checks bare/old policies.
* Workspace check preserves bare Leaflet bytes/MIME/ETag/no-cache and adds actual rendered versioned counterpart.
* API README records one-year policy, stale-query compatibility and existing restart/no-hot-reload boundaries.
* Completion: focused tests passed, 5 tests in 3.423s; Ruff check passed; Ruff format --check reported 65 formatted files; git diff --check passed.

### Final requested validation and reconciliation

* P02-T01: created an isolated external venv with system-site-packages after the actual missing-dependency failure, then installed existing src/core, src/agents and src/api distributions using pip; no dependency manifests changed.
* Focused restored selectors: test_static_assets, test_ui_support.ScreensApi.test_employee_shell_aliases_serve_all_scripts_with_security_headers, test_iot_stream, test_sensor_consistency and test_version: 73 tests, 21.114s, OK.
* P02-T02: source/tests/checks/README diff reviewed, no workflow edits or unexpected tracked modifications; task artifacts reconciled for Review.
* Final source/document/test diff against initial HEAD f1a87593dcad38114c8ddbcc6ea721ae87c8e735 SHA256: 16242405c4fea4b502a798d7404da33aa34a22fa7ab83b59bf7b14ef42cf932d.

### One independent Review

* P03-T01 completed by a fresh read-only general worker activating rpi-review.
* Canonical Review: .copilot-tracking/reviews/logs/2026-10-31/versioned-asset-cache-headers-review.md.
* Execution Complete; outcome Conformant with justified divergence; zero actionable findings.
* The existing UI-support assertion amendment and isolated dependency restoration were assessed as justified. Source diff and final external validation hashes independently verified.
* No source repairs, repeat critique or repeat Review. Original Review remains immutable at its pre-local-commit boundary; P03-T02 persistence follows.

### Verified local persistence

* P03-T02: local implementation/original-evidence commit b516db894c3e7d02e11ccd726a9b1a7ec73f5c83 on fix/versioned-asset-cache-headers.
* Sixteen committed files: nine tracked source/test/check/doc changes and seven dated RPI/state artifacts. No workflow changes.
* Authenticated gh api user returned id8036360/loginjmservera; configured repository-local privacy-safe email 8036360+jmservera@users.noreply.github.com and explicitly used it for both author and committer.
* Commit subject: fix(api): cache current versioned assets immutably (Refs #568).
* Trailer verified: Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.
* Git commit succeeded, actual author/committer/body read back and status clean. This subsequent artifact-only closeout records those observed facts; source and original critique/Review unchanged.
* No push, Azure, secret access, issue closure or publication gate claimed.

## Implementation-Time Plan and Detail Updates

### Critique disposition and shared lock

* Plan Critique Disposition rejects PC-001's alleged /tmp ban because no such rule exists in parent environment and repository src/README.md requires /tmp/ama-rpi-heavy.lock across worktrees.
* Original independent critique remains Complete / Revise; no second critique.
* Plan/details Ready; no user decision required; use external result storage and shared lock.

### Full-discovery header assertion and dependency restoration

* P01-T02/P02-T01: first full discovery ran 1368 tests in 483.107s, failed with 13 subtest failures, 3 errors and 320 skips.
* All thirteen failures come from one pre-existing test_ui_support.ScreensApi versioned-script assertion expecting no-cache. Update it to the exact immutable policy; focused coverage remains in test_static_assets and no new methods are added outside its owner.
* Errors: missing azure.eventhub imports in test_iot_stream/test_sensor_consistency, and missing installed API distribution metadata in test_version.
* Actual missing-dependency failures authorize restoration of existing project distributions/dependencies in isolated external venv, not manifest edits, skips or system package mutation.
* This is an immediately relevant current-state amendment within approved cache behavior/validation; plan scope, ownership and phase details reconciled. No changed user intent or repeat critique.
* Original first-run log retained externally at session files/cache-validation/api-unit.log.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Baseline unittest test_static_assets -q | Existing handlers | Passed | 4 tests, 2.130s, before source edits |
| Changed unittest test_static_assets -q | Actual three handlers and direct snapshot tests | Passed | 5 tests, 3.423s |
| ruff check / ruff format --check | API project | Passed | All checks passed; 65 files already formatted |
| Final full API unittest | Changed source, isolated restored venv | Passed | 1430 tests in 502.331s; OK, skipped=320 |
| Final ruff check / ruff format --check | API project | Passed | All checks passed; 65 files already formatted |
| Final three selected browsers | Restored environment, actual loopback apps | Passed | Cache reuse/turnover; workspace recovery/Leaflet; actual employee/resident chat submission |
| git diff --check | Changed tracked files | Passed | No whitespace errors |
| First full API discovery | Changed source, system Python | Failed | 1368 tests; 13 related assertion failures, 3 missing-dependency errors, 320 skips |
| Three selected browser checks | Actual loopback apps | Passed | asset-cache, workspace recovery/versioned Leaflet, chat-submit logs and results in external session cache-validation |

### Exact command and evidence boundary

Final commands ran from `src/api`, with PATH selecting the isolated restored venv and this exact source import context:

```bash
export PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m unittest discover -s tests -q
ruff check
ruff format --check
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m checks.asset_cache_browser_check --out <external>/asset-cache-restored
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m checks.workspace_scripts_browser_check
flock -w 600 /tmp/ama-rpi-heavy.lock python3 -m checks.chat_submit_browser_check --out <external>/chat-submit-restored
```

`<external>` resolves to `/home/azureuser/.copilot/session-state/12a8273a-1cfb-42aa-ae85-97f032ffafbd/files/cache-validation`.
It holds distinct original failed and final passing logs, browser outputs and the venv. No generated binary output was added to the checkout.

| Final evidence relative to external root | SHA256 |
| --- | --- |
| api-unit-restored.log | 6afbaae612a1c2bed509d3aaa1a39308319885f9690cb77ecc02def95ef9cfeb |
| asset-cache-restored/results.json | 66b7772501982430898fdd12bce2715eac19436e951ceb5d864063d3d7a6c5f0 |
| workspace-restored.log | c6976c85c52dde47e9f9bdc502754a02793f068f7918291958d23c6c0963788b |
| chat-submit-restored/results.json | 90f90dca18ca55fe7074f94a4e68cb116a4a1756a5c4512f5c4a0303b34c5bbf |

* Existing runtime packages were restored from their unchanged manifests; current source imports remain explicit on PYTHONPATH.
* Existing skips remain disclosed; real SQL/live/cloud/model prerequisites and full browser matrix were not exercised. No skip tokens or Azure operations used.
* All three selected browser checks own and stop their constructed-data loopback apps. Cache check keeps browser cache enabled and verifies fresh immutable reuse without Playwright routing interception.

## Pre-Review Reconciliation

* Plan markers and details: P01/P02 current and complete; P03 pending as explicitly sequenced.
* Completed-work evidence and handoff: current; nine tracked source/test/check/doc files plus dated task artifacts.
* Validation: requested commands and three selected browsers passed in restored environment; original failed attempt preserved.
* Blockers: none for source Review; publication/live/human gates remain unperformed.
* Review readiness: Ready for exactly one independent assessment; no current-task source repair or repeat Review afterward.

## Blockers

None for implementation.

## Remaining Work

None in the requested local source task. Publication and live acceptance remain distinct deferred work.

## Follow-Up Items

* Owner-authorized deployed cache/signed-in acceptance remains separate; no live acceptance inferred from source fix.
* Full publication gate remains necessary before later push/publication; not an acceptance claim here.

## Return-to-Caller State

* Automatic parent: full requested local task complete; independent Review Complete / Conformant with justified divergence.
* Requested validation and selected browser checks passed; existing 320 skips disclosed.
* Critique: Complete / original Revise, PC-001 rejected with parent-context evidence.
* No implementation blocker or actionable Review findings. Local source/original evidence persisted; no publication or live acceptance.
* Automatic-session status remains running at the Follow-up checkpoint; no child work is selected or authorized in this non-interactive no-push task.
