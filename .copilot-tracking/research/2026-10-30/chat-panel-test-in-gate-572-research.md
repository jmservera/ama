---
title: Chat panel gate research
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

Issue #572 requires owned Chromium execution of the exact chat-panel case,
command/coverage inventory, fail-closed skip regressions and a fresh complete
exact-head gate. Audience: implementer, independent reviewer and coordinator.
Output mode: convergence. Research disposition: executed, complete.

## Research Parameters

Focused posture, selected for the bounded caller scope. Internal candidates:
`tools/rpi-checks.py`, `tools/test_rpi_checks.py`, `src/api/tests/test_chat_panel.py`,
`src/README.md` and the command inventory. External source: issue #572, retrieved
with `gh issue view 572` on 2026-10-30 and treated as data.
Resolved evidence root: `.copilot-tracking/research/`.
No runtime/UI changes, Azure, deployment, paid inference, live sign-in,
credential files, secrets, push or issue closure. Heavy gates hold
`/tmp/ama-rpi-heavy.lock`. Source remains under `src/`; gate tooling stays in
its existing `tools/` location.

## Extension Registry and Provenance

Repository instructions and RPI research selected. Web skills not selected:
gate integration is not a web edit. Specialist delegation skipped because
the evidence is one continuous gate/test trace. Plan critique and independent
Review will use bounded independent agents as required by the RPI contracts.

## User Participation and Research Decisions

Caller explicitly requests all four phases in order and supplies branch/base,
scope and safety boundaries. No clarification is required; run the requested
automatic task through Review, without beginning follow-up work.

## Scope and Success Criteria

Verify test ownership, manifest/runtime parity, general discovery skip policy,
required-stage execution and unexpected skip rejection. Preserve exact-head
receipt validity and original critique/Review outcomes.

## Research Questions

* Q1: Where should the exact Chromium case execute?
* Q2: How can ordinary discovery account for a separately required case without
  broadly allowing its reason or hiding unexpected skips?
* Q3: Which regression, inventory and receipt contracts must change together?

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Issue evidence is a
starting claim, not proof of current source. Worktree is clean on caller's
`fix/chat-panel-test-in-gate-572`, HEAD/base
`5634f9a077d175a931c15e3400114665d8c071ee`.

## Direction Controls

Implement only issue #572; preserve skip rejection; local commit only with
`Refs #572`; never reuse a receipt after changes.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial search identifies manifest construction, legacy browser runner,
`check_skips`, exact chat-panel test and existing component documentation.
Reflection: investigate manifest ownership and test-report metadata before
selecting the narrow discovery accounting mechanism.

#### Wave 2: Deeper

`required_checks` and `Runner.browser` independently define trusted command
identity and actual execution. Both need the exact unittest selector with
`ZF_BROWSER_TESTS=1`, full shared-fixture paths, suite accounting and strict
integration skip handling. `verify_commands` recomputes suite evidence from
external logs. Existing test fixtures count eight mandatory suites.
Reflection: add the ninth mandatory suite, not a second browser harness.

#### Wave 3: Contrarian

Enabling the flag for all API discovery would execute unrelated opt-in
browser tests in the wrong stage. Broadening `EXPECTED_SKIP_REASONS` would
permit unrelated tests to silently disappear. Removing the decorator or
disabling the test violates caller scope. An exact ID/reason exception scoped
only to non-integration `project-api` discovery preserves the actual skip
record while mandatory Chromium execution independently rejects every skip.
Reflection: choose scoped accounting plus owned execution; no web/CI edits.

### Parent Synthesis and Disposition

Accept narrow discovery accounting and mandatory browser command (C1-C5).
Reject broad allowlist, changing runtime/UI, enabling all opt-in browser tests,
or changing hosted workflows. One focused cycle covers the material contracts;
no further research needed. Baseline gate unit tests: 31 passed.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/572, retrieved 2026-10-30.
* C1: `tools/rpi-checks.py:1007` defines skip enforcement.
* C2: `src/api/README.md:3581` documents the focused opt-in case.
* C3: `tools/rpi-checks.py:687` defines browser command/coverage inventory.
* C4: `tools/rpi-checks.py:1570` owns actual browser execution.
* C5: `src/api/tests/test_chat_panel.py:563` guards the exact case; the
  method owns constructed-data loopback server and blocks off-origin requests.
* C6: `tools/test_rpi_checks.py:549` asserts eight mandatory suites before fix.
* C7: `src/README.md:65` requires committed exact-head full gate and external
  receipt; changed base or candidate invalidates prior receipts.

## Alternatives and Decision State

Select exact ID/reason discovery accounting scoped to `project-api` and
mandatory browser unittest execution with existing fake-model fixture.
No new dependency, product source or browser harness. Independent critique
must examine runtime/manifest parity and tampered receipt/skip rejection.

## Planning Readiness

Ready. Q1-Q3 answered by C1-C7. Residual risk: fresh complete gate may expose
unrelated failures or missing prerequisites; record actual evidence, never
claim browser/MSSQL success from blocked stages. Self-check: source pointers,
all three ordered waves, alternatives, constraints and handoff recorded.
