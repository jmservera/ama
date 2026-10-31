<!-- markdownlint-disable-file -->
## Research Brief

Correct PR #602's three unresolved metering threads for #432. Audience:
maintainers and independent reviewers. Focused, convergence-mode internal
research; no paid inference, secrets, deployment or unrelated changes.
The caller explicitly authorizes the full automatic RPI correction loop,
commit, ordinary push and thread resolution, with CI as publication gate
instead of waiting for the complete local gate.

## Research Parameters and Direction Controls

Task identity: issue-432-pr-602-final-threads; slug:
ai-metering-432-final-threads. Evidence root: `.copilot-tracking/`.
Initial areas: provider result shaping, assistant quarantine, report handling,
post-save attribution and existing external tests. No external research needed.
Pull ran first; main merge reports already up to date. Clean active topic
branch matches open PR #602. No rubric or log conflict required resolution.

## Extension Registry and Participation

Repository guidance selected for bounded source changes, external tests,
knowledge-base updates and preserved original evidence. RPI Research selected.
No specialist research lane: these failures form one coupled trace.
Owner supplied all scope and gate decisions; interaction is unavailable.
Research is read-only outside its evidence and required workflow state.

## Research Questions

* Q1: How can a model mismatch reach non-retryable quarantine after settlement?
* Q2: How can backend report holds retain the ordinary report and input errors?
* Q3: How can publication preserve usable saved/returned outputs after a hold?

## Research Cycle Log

Cycle 1 opening: Wider will trace adjacent completion/report/publication
contracts; Deeper will inspect bounded validation and test fixtures; Contrarian
will challenge retries, persistence consistency and unchanged financial holds.

## Findings, Evidence and Decisions

### Cycle 1: Wider

The three named GraphQL threads remain unresolved. Existing composed API
tests cover real loopback transport, JSON/SQL drafts, chat adapters, worker
serialization and manager HTTP reporting. No new dependency is needed.
Reflection: reuse that external harness rather than create package-local tests.

### Cycle 1: Deeper

* C1: `src/core/src/zava_forward/core/ai.py:96-118`: settlement occurs before
  mismatch raises; evidence then erases the returned-model signal.
* C2: `src/core/src/zava_forward/core/assistants.py:886-910`: only returned
  outcomes trigger model checking; unavailable outcomes are retryable.
* C3: `src/api/src/zava_forward/api/server.py:523-533`: backend DispatchHeld
  shares the input-error catch and loses the report.
* C4: `src/core/src/zava_forward/core/ai_consumption.py:180-191,552-608`:
  bounded reads hold above 10,000; an admitted reservation at 9,999 and its
  completion may reach 10,001. Do not relax admission or settlement bounds.
* C5: `src/core/src/zava_forward/core/ai_tasks.py:273-297` and
  `src/core/src/zava_forward/core/store.py:859-868`: output linking follows
  domain save, so hold handling must persist consistent fallback state.
* C6: `src/core/src/zava_forward/core/chatthreads.py:317-342`: message count
  determines sequence; expected_version prevents an incorrectly predicted
  delivery sequence. Link before final message save under the Store lock,
  guarded by that version, so a fallback needs no message-edit API.
* C7: `src/core/src/zava_forward/core/ai_consumption.py:900-948`: missing
  output joins already prevent reconciled economics after read recovery.

Reflection: preserve a closed model-mismatch outcome with a bounded model
value; preserve strict output() and expose a separate publication-only hold
helper. Explicit unresolved metadata accompanies fallback delivery.

### Cycle 1: Contrarian

Do not catch arbitrary persistence/input failures, truncate partitions, call
the provider again, relabel AI text as a manual answer, or let an oversized
model enter a durable envelope. Ordinary network failure must remain retryable.
Existing saved drafts should retain comparison evidence but show the same
manual fallback as the returned response. Chat sequence prediction must be
version guarded and needs no storage schema or message mutation.

Worker/API completion itself also links outputs transactionally (C2); this
cycle does not broaden the named post-save surfaces. Exact-capacity assistant
model-mismatch tests run below capacity; its settlement path remains unchanged.
One complete focused cycle covers Q1-Q3; next sources are redundant.

## External Evidence

* W1: https://github.com/jmservera/ama/pull/602#discussion_r4432028058
* W2: https://github.com/jmservera/ama/pull/602#discussion_r4432028083
* W3: https://github.com/jmservera/ama/pull/602#discussion_r4432028108

Retrieved 2026-10-31 with authenticated gh GraphQL. Supplied review findings
confirmed against C1-C7; no model authority or real benefit inferred.

## Alternatives and Decision State

Selected bounded signal and publication-only hold handling. Rejected broader
ledger/output semantics changes and arbitrary-error fallbacks (C4-C7).
No unresolved source question. Hosted and human approval remain separate.

## Planning Readiness

Ready. Research disposition: executed, complete. All Q1-Q3 evidence-backed.
Self-check: full Wider/Deeper/Contrarian cycle, provenance, scope, alternatives,
risks and handoff recorded. Parent proceeds to Plan.
