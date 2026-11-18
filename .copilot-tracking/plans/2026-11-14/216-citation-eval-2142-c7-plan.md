<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #216 Child Hardening Pass 7 (`216-citation-eval-2142-c7`)

## Metadata

* Task ID: 216-citation-eval-2142-c7
* Parent Task ID: 216-citation-eval-2142-c6
* Date: 2026-11-14
* Research reference: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c7-research.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c7-phase-details.md

## Scope and Objectives

Resolve `RV-002`..`RV-007` and expose a `src/core` `RegulatoryChat.surface(...)` selector in `src/core`:

1. Enforce UTF-8 string validity (`_is_utf8_str`, `_safe_quote`, collision-free `["invalid_utf8_str", ascii(v)]` digest tagging, and UTF-8 mapping keys) and fail-closed `render_extractive_answer` refusal on non-`Mapping` or incomplete `sources`/`facts`/`cards` (`sources=[{}]`, malformed facts) so malformed inputs never raise `UnicodeEncodeError` or `KeyError` (`RV-006`, `PC-005`, `PC-007`).
2. Require projection-aware provenance validation (`_source_provenance_valid`, `_projected_provision_valid`, `_fact_provenance_valid`, `_card_provenance_valid`) in `grade_chat_turn` and `_baseline_projection_matches`, derive `conflict` consistently across `bundle` and `expected`, and verify baseline projection parity across `answer`, `conflict`, and `refused` cases (`RV-002`, `RV-005`, `PC-001`, `PC-002`, `PC-004`).
3. Require `graded` cases to contain at least one `answer` turn, `adversarial` cases to contain at least one `refused` turn, and `prompts` to contain only non-blank UTF-8 strings covering `ADVERSARIAL_PROMPTS`, recording `dataset_gaps` on any violation (`RV-003`, `RV-007`).
4. Bind every paired staff observation pair by `(role, participant, case_id, task)` and arm-specific `surface_sha256` (`observation_surface_digest`) to the evaluated `cases` and `paired_cards` surfaces (`RV-004`, `PC-003`).
5. Add admitted, single-snapshot `RegulatoryChat.surface(...)` in `src/core/src/zava_forward/core/regulatory_chat.py` backed by `resolve_regulatory_surface` (defaulting to `cards_only` without invoking `ask` or persisting turns), update `src/core/README.md`, and add comprehensive regressions in `src/core/tests/test_regulatory_eval_gates_216.py` (`RV-001` core boundary, `PC-006`).

## Implementation Checklist

* [x] `P01`: Harden provenance, dataset-gap, surface-bound observation, baseline projection, and UTF-8 guards in `src/core`
  * [x] `P01-T01`: Implement `RV-002`..`RV-007` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and add `RegulatoryChat.surface(...)` in `src/core/src/zava_forward/core/regulatory_chat.py`.
  * [x] `P01-T02`: Update `src/core/README.md` and `src/core/tests/test_regulatory_eval_gates_216.py` with `observation_surface_digest`-bound observations and regression tests for `RV-001`..`RV-007`, then pass full `src/core` validation.

## Follow-Up Items

* Cross-package `src/api/src/zava_forward/api/server.py` HTTP route wiring and `src/agents` helper deduplication remain outside the user-bounded `src/core` scope.
