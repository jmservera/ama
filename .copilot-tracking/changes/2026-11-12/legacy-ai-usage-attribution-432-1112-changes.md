<!-- markdownlint-disable-file -->
# RPI Changes: Legacy AI usage attribution

## Metadata

* Task ID: legacy-ai-usage-attribution-432-1112
* Plan: .copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md
* Phase details: .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md
* Declared scope: full plan
* Base: 139176fa0382add781b1830b1ac9db785ed086fe

## Execution Status

Complete for the declared plan. Local only; no push, issue or PR edit, network, provider or model call.

## Execution Summary

The hypothesis that legacy paths discard usage was false on current source. Implemented one ordering fix in `Ai._request`, five legacy text-draft test methods (the missing/malformed case is one method with three subtests), and a documentation correction.

## Completed Work

### P01-T01 Legacy join tests

* src/api/tests/test_ai_consumption_api.py: fixture `response_usage` attribute with an `OMIT` sentinel (default payload unchanged), helpers `legacy_draft` and `legacy_ledger`, and tests for success join, omitted and malformed usage (total mismatch, cached above prompt), provider HTTP 500, settlement failure, workflow-only no dispatch. Existing tests untouched except the handler body construction.
* Failing-first: on the unfixed source the settlement-failure test failed with the envelope reporting `{'prompt_tokens': 100, 'completion_tokens': 20, 'total_tokens': 120, 'cached_tokens': 10}` where None was expected; the other four methods passed.

### P01-T02 Receipt ordering

* src/core/src/zava_forward/core/ai.py: `receipt.update(usage, returned_model)` moved after `consumption.complete(...)` with one explanatory comment.

### P02-T01 Documentation

* docs/reference/resources/ai-tokenomics.md: stale legacy sentence corrected, source-observed wording, no cost claim.
* docs/reference/log.md: dated 2026-11-12 entry appended.

### P02-T02 Validation

See the Validation Record.

## Implementation-Time Plan and Detail Updates

* The malformed-usage test does not assert a manual-route text: observed behavior is that the draft text is still shown while the ledger records Unknown liability, an alert and a held completion, and the output is joined; the test asserts those. Local judgment, no plan change; behavior is unchanged from main.
* Case table said "six cases"; the implementation has five methods (one with three subtests), within the cap.

## Validation Record

PYTHONPATH put this worktree's src and tests directories first (the installed editable distributions point at another checkout).

| Check | Result |
| --- | --- |
| Baseline `tests.test_ai_consumption_api` before changes | 32 tests OK |
| New tests on unfixed source | 5 run, 1 failure (settlement failure) as intended |
| After fix: api `test_ai_consumption_api`, `test_ai_tasks`, `test_document_controls`, `test_ai_boundary` | 129 OK |
| After fix: core `test_ai_input_bounds`, `test_ai_consumption_safety`, `test_ai_consumption`, `test_ai_dispatch_marker` | 52 OK |
| After fix: agents `test_chat_model` | 13 OK |
| New tests after formatting | 5 OK |
| `ruff check` and `ruff format` on the test file; `mypy` on the test file | Pass |
| `ruff format --check` on ai.py | Would reformat; pre-existing, not changed by this work, left alone |
| Not run | Full gate, SQL Server, browser, network, model, hosted CI |

## Pre-Review Reconciliation

Plan markers checked; details, changes and handoff agree; no blockers.

## Blockers

None.

## Remaining Work

None in plan.

## Follow-Up Items

* Envelope-usage proof for `look_at` and priority; resident chat host join (owner-gated); issue body wording to be updated by the owner or a later authorised action.

## Return-to-Caller State

Ready for Review of the committed candidate. Excluded: resident chat host, assistants, `look_at`/priority proofs, price, billing, authority, reports, issue edits.
