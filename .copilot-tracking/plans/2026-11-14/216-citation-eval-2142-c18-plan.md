<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 18 for Issue #216 (`RV-047`..`RV-048`)

* Task ID: `216-citation-eval-2142-c18`
* Parent Task ID: `216-citation-eval-2142-c17`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close `RV-047` and `RV-048` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c17-review.md` inside `src/core`:

1. Isolate `snap` from renderer mutation in `RegulatoryChat.ask()` and `RegulatoryChat.surface()` by passing `copy.deepcopy(snap)` to `self.render(...)` and copying the returned mapping before grounding verification (`RV-047`).
2. Refine `_REFUSAL_PATTERNS[1]` in `regulatory_eval_gates.py` so indirect `\bwhether\s+...meeting` compliance inquiries refuse regardless of outer WH framing, inquiry-governed `(?:if|that)` clauses refuse (including `tell me/us`, `ask`, `see`), and polite-prefaced informational WH-conditionals (`"Could you explain what happens if..."`) are not falsely refused (`RV-048`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c18-plan-critique.md` (`Complete`, `Pass`).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-047`..`RV-048` in `src/core` and Verify

* [x] `P01`: Implement `RV-047`..`RV-048` across `regulatory_chat.py`, `regulatory_eval_gates.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Deep-copy `snap` and rendered replies around `self.render(...)` in `RegulatoryChat.ask()` and `RegulatoryChat.surface()`, and refine `_REFUSAL_PATTERNS[1]` in `regulatory_eval_gates.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Add `test_c18_renderer_bundle_mutation_isolation_and_whether_vs_prefaced_wh_if_precision` in `test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and pass `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a separate multi-package PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.
