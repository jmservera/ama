<!-- markdownlint-disable-file -->
# RPI Phase Details: Legacy AI usage attribution

## Metadata

* Task ID: legacy-ai-usage-attribution-432-1112
* Task slug: legacy-ai-usage-attribution-432-1112
* Related plan: .copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Prove and fix the legacy usage join | complete | P01, P01-T01, P01-T02 |
| P02 | Correct documentation and validate | complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Prove and fix the legacy usage join

### Context

`Ai._request` (src/core/src/zava_forward/core/ai.py) updates the caller receipt with validated usage, then settles the ledger. `run` merges the receipt into the result, which `ai_tasks.finish` places in the record envelope.

### Intent

Result usage equals ledger-settled usage in every outcome.

### Boundaries

* Included: ai.py `_request`; one existing test module.
* Excluded: look_at, priority, assistants, chat host, price, report, authority.

### Likely Targets

* src/core/src/zava_forward/core/ai.py: statement order.
* src/api/tests/test_ai_consumption_api.py: configurable spy usage and new tests.

### Dependencies

* none

### Validation Expectations

* Targeted unittest of test_ai_consumption_api; ruff and mypy on changed files.

### Completion Evidence

* Failing-first output recorded in the changes record.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add legacy join tests

#### Context

Fixture class ConsumptionApi has a loopback spy and `authority(capability, ...)`. Legacy `briefing` runs through `ai_tasks.run_text_task` with a store whose `ai` is the spy-backed `Ai` (pattern at test line 460).

#### Intent

One test class method set with at most six cases, written once: success join (envelope usage equals ledger tokens, output record present, no marker strings in ledger), omitted usage, malformed usage, provider HTTP failure, settlement failure, workflow-only no dispatch.

Case map against existing coverage (all edits stay in the existing test module; removals none; maximum six additions; the #116 session's modules are untouched):

| Case | Existing legacy-path coverage | Disposition |
| --- | --- | --- |
| Success envelope usage equals ledger tokens, output joined | Review recovery at test_ai_consumption_api.py:460 and documents at :978 never assert envelope usage; assistant-only at :246 | Add |
| Omitted usage | None on legacy (chat/assistant only) | Add |
| Malformed usage (total mismatch) | Unit only for `usage()` in test_ai_consumption.py:171 | Add |
| Provider HTTP 500 on legacy draft | :803, :877 chat and :1374 assistant only | Add |
| Settlement failure: one-shot `RuntimeError` from `consumption.complete` on the first call via `patch.object`, second call real; expect result usage None, template text, ledger completed with no tokens | None | Add; failing-first on unfixed source |
| Workflow-only (`mode="workflow-only"`) | :1149 chat only | Add: zero provider requests and zero reservations |

Ledger records are also scanned for the synthetic input and output marker strings (none expected).

#### Boundaries

* Included: a `response_usage` attribute on the fixture handler with a sentinel to omit.
* Excluded: payload-equality matrix of the independent #116 session; edits to its modules.

#### Likely Targets

* src/api/tests/test_ai_consumption_api.py: new tests.

#### Dependencies

* none

#### Validation Expectations

* Settlement-failure test fails on the unfixed source for the stated reason.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reorder receipt usage after settlement

#### Context

ai.py: `receipt.update(usage=...)` precedes `self.consumption.complete(...)`.

#### Intent

Settle first, then update the receipt (model and usage).

#### Boundaries

* Included: those two statements.
* Excluded: any other change.

#### Likely Targets

* src/core/src/zava_forward/core/ai.py

#### Dependencies

* P01-T01

#### Validation Expectations

* All new and existing tests pass.

<!-- rpi:phase id=P02 -->
## P02: Correct documentation and validate

### Context

docs/reference/resources/ai-tokenomics.md lines 77-81 state that legacy paths discard usage.

### Intent

Accurate knowledge base and recorded validation.

### Boundaries

* Included: that sentence, docs/reference/log.md append.
* Excluded: issue edits, tick claims, slides, memory.

### Likely Targets

* docs/reference/resources/ai-tokenomics.md
* docs/reference/log.md

### Dependencies

* P01

### Validation Expectations

* Link and diff review; targeted tests; lint and types.

### Completion Evidence

* Changes record with command results.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Correct the tokenomics sentence and log

#### Context

Sentence contradicts C1-C4.

#### Intent

State that legacy `run`/`look_at` return validated usage and join output records, with remaining gaps (chat host, no cost, no price, no billing).

#### Boundaries

* Included: one bullet and one log entry.
* Excluded: unrelated rewriting.

#### Likely Targets

* docs/reference/resources/ai-tokenomics.md, docs/reference/log.md

#### Dependencies

* P01

#### Validation Expectations

* Markdown relative links resolve.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Targeted validation

#### Context

PYTHONPATH must list this worktree's src first.

#### Intent

Record results for the whole test_ai_consumption_api module, the other `_request` consumers (src/api tests test_ai_tasks, test_document_controls, test_ai_boundary; src/core tests test_ai_input_bounds, test_ai_consumption_safety; src/agents tests test_chat_model), ruff and mypy where configured, all read-only runs. The `_request` reorder also affects `evidence()` envelopes, so those suites are part of the check.

#### Boundaries

* Included: targeted commands.
* Excluded: full gate, SQL, browser, network.

#### Likely Targets

* none

#### Dependencies

* P01, P02-T01

#### Validation Expectations

* Pass, or exact failures recorded.
