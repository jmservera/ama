<!-- markdownlint-disable-file -->
---
title: Progress dashboard correction research
description: Focused evidence for the two PR 540 correction findings
ms.date: 2026-10-29
---

## Research Brief

* Topic: Refs #533, PR #540 correction round.
* Purpose/audience: local implementation and independent review of two supplied defects.
* Scope: synthetic non-list history handling and accessible date-range errors, with regressions.
* Non-goals: visual redesign, unrelated historical findings, cloud or publication.
* Criteria: dashboard/archive unknown lifecycle without exceptions; linked inline date errors and first-field focus; real-source API tests, browser check and pinned axe.
* Output mode: convergence, preparing Plan.

## Research Parameters

* Posture: focused, selected for named source files and concrete supplied failures.
* Root: `.copilot-tracking/research/2026-10-29/`.
* Prior knowledge: verify supplied review claims against current source; parent completed loop is historical, not current validation.
* Candidate internal areas: API progress read model, progress UI, unit/browser regressions, API README, design-system contract, scenario manifest.
* Candidate external area: current Web Interface Guidelines only.

## Direction Controls

Use the existing clean topic branch and open PR. No push, az, force-push, closing keyword, private data or mvp source. Hold the nonblocking heavy lock for full suites; if busy, targeted tests only. Commit original dated RPI evidence and preserve parent artifacts.

## Extension Registry and Provenance

* Repository instructions: selected; src layout, native Fluent-compatible form errors, honest validation boundaries and privacy-safe commits.
* rpi-research: selected; inline wider/deeper/contrarian cycle.
* web-design-guidelines: selected; complete current source fetched 2026-10-29 from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
* accessibility: selected; field identification and focus; pinned existing axe is engineering evidence, not WCAG conformance.
* Redesign skills: skipped; no design improvement or visual redesign is requested.
* Specialists: inline research, no independent uncertainty warrants delegated discovery.

## User Participation and Research Decisions

No intake prompt: caller supplied exact scope, continuation authority and validation limits. Recovered parent automatic mode; explicit full-loop request selects this correction child.

## Questions

1. What guard preserves unknown lifecycle behavior for malformed history?
2. How can date validation be distinguished from actual read failures without mislabelling valid fields?
3. What regression and pin surfaces must change?

## Research Cycle Log

Cycle 1 opening: verify admission/lifecycle and shared load/error paths, then examine API error metadata, field-error prior art and regression infrastructure, then challenge alternatives and boundary cases.

### Wider

Read progress.py, progress.js, API README, unit/browser regressions, parent state and design-system contract. Both supplied defects are supported. Shared load handles both dashboard and archive, so reversed archive dates need the same field contract. Reflection: preserve read-failure alert/retry and unknown-date coverage rather than changing admission or hiding malformed cases.

### Deeper

Reproduced `synthetic({is_synthetic: True, history: None}) == True` followed by lifecycle TypeError using this worktree's src and `/tmp/ama-533-venv`. API errors already expose HTTP status and `reasons` to JavaScript. Existing field-error styles provide warning glyph, text and invalid border. Reflection: structured range-error metadata can reuse this path without string matching or changing shared app.js.

### Contrarian

Challenged client-side duplicate range validation: omitted dashboard dates depend on store.as_of, while the archive deliberately has no 366-day cap. Treating every 400 as invalid dates would mislabel unknown parameters or paging failures. Matching error text would couple UI behavior to prose. Select a dedicated ValueError subtype for actual range failures, serialized through existing reasons metadata. Non-list history must return unknown before traversal, including iterable strings/dictionaries; merely using `history or []` would leave other invalid types. Reflection: test both endpoints and storage backends, reversed/oversized/defaulted ranges, valid boundaries, and real read errors without field invalidity.

### Synthesis and re-entry

All three questions have evidence. No further cycle: remaining sources are redundant for these two bounded changes. Research executed inline; no delegated lane implied.

## Evidence Log

| ID | Evidence |
| --- | --- |
| C1 | `src/api/src/zava_forward/api/progress.py:62-100`: explicit synthetic admission bypasses history checks; lifecycle traverses unguarded history. |
| C2 | `src/api/src/zava_forward/api/progress.py:124-134,279-288`: dashboard caps inclusive range at 366 days; archive checks ordering only. |
| C3 | `src/api/src/zava_forward/api/web/progress.js:64-78`: shared load renders only page alert and show() focuses main. |
| C4 | `src/api/src/zava_forward/api/web/app.js:45-81`: API preserves status/reasons; show() focuses main synchronously. |
| C5 | `docs/reference/research/ux/design-system.md:105-122`, `src/api/src/zava_forward/api/web/style.css:230-232`: invalid fields require linked text and existing field-error styling. |
| C6 | `src/api/tests/test_progress_dashboard.py:99-424`, `src/api/checks/progress_browser_check.py:180-208`: JSON/SQLite inherited tests and real loopback browser harness; old range assertion checks only alert/editability. |
| C7 | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:46-51`: four pins; none are proposed edit targets. |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-29: inline field errors and first-error focus; full source successfully retrieved. |

## Findings Mapped to Questions and Evidence

Q1: C1 supports an explicit list guard and unknown result. Q2: C2-C5/W1 support a typed range validation signal, linked inline field errors and focus after mounting. Q3: C6-C7 support inherited JSON/SQLite coverage, HTTP metadata assertions and expanded browser/axe states; no pinned files need editing.

## Alternatives and Decision State

Accepted: explicit non-list guard; structured range exception and reasons metadata; native per-field errors. Rejected: falsy-only history guard, client duplicate date algorithm, message matching, and treating all failures as field errors, for the reasons in Contrarian. Keep server date semantics and admission unchanged.

## Open Questions, Risks, and Residual Uncertainty

The requested `/home/azureuser/source/ama-wt/issue-526-journey/.venv/bin/python` does not exist (initial invocation exit 127; directory probes confirm absence). Existing `/tmp/ama-533-venv` has project/dev dependencies and Playwright; this worktree's src resolves correctly there. Use that existing environment without installing or modifying a shared environment, and disclose the deviation. Prior pinned axe exists at `/tmp/ama-533-evidence/axe-4.10.3.min.js`. Heavy-lock availability remains a validation-time check. No full publication gate or human accessibility acceptance will be inferred.

## Planning Readiness

Ready. Research disposition: executed / Complete. Current decisions: preserve both endpoint date semantics; use current-source PYTHONPATH with existing fallback venv because the requested path is unavailable. No unresolved implementation decision. Self-check: questions, three ordered waves, evidence IDs, alternatives, constraints and handoff recorded.

## Continuation

Automatic parent proceeds to Plan for this correction child. No publication or cloud authorization is granted.
