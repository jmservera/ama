---
title: Routed browser recovery origin guard implementation
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: pr-594-browser-asset-origin-guard-568.
Parent: pr-594-browser-asset-matchers-568.
Implementation date: 2026-10-30.
Approved plan and details: `.copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md` and `.copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md`.
Input: original `.copilot-tracking/reviews/logs/2026-10-30/browser-asset-matchers-568-review.md`, RV-001 Medium, Complete / Not accepted.

## Execution Status and Declared Scope

Complete. Later bounded `rpi-implement` invocation for RV-001 under original P01-T01 origin-denial requirement, not a second Research/Plan/Review cycle or a rewrite of the completed task. Non-interactive execution resolves this directly coupled three-line omission to complete the caller's requested local correction. No new product decision, remote operation or approval is inferred.

## Approved Boundary

Only `chat_widget_browser_check.recovery_case` context guard and a sixth regression method in the existing new `test_browser_asset_urls.py`. Original plan, critique, research, implementation evidence and Review retain their assessed content. No additional helper/file/test-budget expansion, no cache routing, Azure, secrets or push.

## Planned Validation

Guard regression must inspect the actual constructor's registered callback, asserting local continuation and off-origin abort without sending an external request. Run full chat-widget browser check, six new regression methods plus existing relevant units, API Ruff/format and mypy under the same heavy lock. Existing original CI replay and seven-harness results remain historical evidence, not a claim that a new independent Review passed.

## Completed Work

Added the existing local-only context route to `chat_widget_browser_check.recovery_case`. The origin-bound asset matcher handles only owned assets; external lookalikes fall through to the registered abort guard.

Added sixth test method `test_chat_recovery_context_registers_local_only_guard`: invoke the actual recovery constructor with mocked browser/expectation plumbing, obtain its registered route callback, and assert local bare/version paths continue while off-origin and host-lookalike requests abort. This callback regression sends no network traffic; it complements the existing native browser matcher/off-origin tests and the repeated real chat recovery harness.

## Validation Record

From `src/api` with the same task-owned pip environment and API/core/agents test PYTHONPATH:

```bash
flock -w 600 /tmp/ama-rpi-heavy.lock bash -c '
  set -e
  python -m unittest test_browser_asset_urls test_static_assets test_workspace_scripts \
    test_chat_widget_focus test_case_journey test_design_system \
    test_accessibility_baseline test_content_standard -q
  python -m checks.chat_widget_browser_check --axe <pinned-axe> --out <guard-chat-widget>
  ruff check .
  ruff format --check .
  ruff check --isolated --config '\''src = ["src", "tests"]'\'' \
    --select E,F,I,B,UP --target-version py312 --line-length 100 \
    checks/asset_urls.py tests/test_browser_asset_urls.py
  ruff format --isolated --line-length 100 --check \
    checks/asset_urls.py tests/test_browser_asset_urls.py
  mypy
'
```

Passed: 74 unit cases in 5.973s; full employee/resident chat-widget browser module including transient recovery and bounded exhaustion; API Ruff lint/format; strict new-code lint/format; mypy 122 source files. Output root: `/home/azureuser/.copilot/session-state/7dc0069c-bd97-46db-8804-627147673f47/files/`.

`guard-validation.log` SHA-256: `b2b40121c7307423010cf10bcc3afe29fea975086d42bc4045f74d695938aa46`.
Original Review SHA-256 remains `ac1b9ce62fd5bb8f5fda6f56703db707d6a4534f798a4e7e0d73adafcb0a993a`.
Fresh browser screenshots/results remain external in `guard-chat-widget/`.

## Remaining Work and Blockers

No implementation work remains. Create the requested local commit with the original adverse Review and this later implementation evidence; do not push. No dependency blocker.

## Review and Outcome Boundaries

Preserve exactly one original Review with its adverse outcome. A passing later regression demonstrates guard implementation, not independent finding-closure verification or a revised conformance outcome. No second Review will run.

## Return-to-Caller State

Bounded later implementation Complete; no blockers or remaining source work. Original Research/Plan/Implement/Review order and one-pass outcomes remain preserved. Local engineering proof is now original CI before/after, seven affected browser checks (chat rerun after guard), 74 relevant unit cases and Ruff/mypy. Full publication gate, hosted/live/human acceptance and an independently reassessed final candidate remain unperformed.
