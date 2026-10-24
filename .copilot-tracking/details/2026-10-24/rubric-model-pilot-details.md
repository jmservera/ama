<!-- markdownlint-disable-file -->
---
title: Rubric Model Pilot Details
description: Execution constraints and measurement boundaries
ms.date: 2026-10-24
---

## P01

Use a frozen selected-artifact snapshot without a Git remote or baseline score
file. Read-only tools only; no shell, writes, network tools, delegation or
record_rubric_score tool available to the model. Return one flat scorecard JSON
as the final response. This is an explicitly recorded transport deviation from
hosted MCP output, not an output-runtime equivalence claim.

## P02

Run explicit model IDs sequentially, no auto routing or paid retries. Set a
250-credit per-session soft guardrail (USD 2.50 equivalent), leaving USD 2.50
aggregate headroom for three runs. Inspect recorded usage before each later
run and refuse to start if remaining allowance cannot cover its guardrail plus
headroom. Inference price estimates are not a billing invoice.

## P03

Parse final JSON, reconstruct it through scorecard_adapter.from_inputs, then
evaluate locally through gate.evaluate. Record full criteria before and after
gate enforcement. Missing artifacts may force scores to zero downstream.
Compare full vectors, not totals alone. With one run per model no estimate of
within-model variance or robust latency distribution is possible.

## Completion Evidence

The runner, frozen manifest, original responses/usage and comparison are under
.copilot-tracking/sandbox/2026-10-24/rubric-model-pilot/.
comparison.json retains all measured fields and gate/card validity. analyze
verifies all raw registered-file hashes, context/prompt hashes, deck extraction,
exact actual user prompts and no extra user turn. Local jq invariants confirm
three requested/served identity matches, complete accounting, read tools only,
zero reported file changes and reported equivalent usage below USD 10.

No further model invocation is authorized. Source snapshot 4ed85ba remains the
measurement target even though the owner concurrently changed the live deck.

## P04 Native Extension

The owner subsequently approved one native-MCP invocation each for Haiku 4.5
and GPT-6 Luna within the original USD 10 aggregate allowance. Retain the
original snapshot at 4ed85ba, rubric and tool schema. Use the pinned unmodified
gh-aw-actions 924af5fdc64061cfbf66fb584c8b07e2ac230c60 runtime with the existing
test harness's generated config and schema. Real pinned blob and stdio/HTTP
validation/append tests: 7 passed; an earlier wrong archive path skipped all
checks and was corrected, not counted as validation.

Expose read tools and only record_rubric_score, whose custom-job handler
appends locally. No trusted gate/publisher job is executed by the MCP process.
Strip credentials from its child environment. Give each model separate config,
tools, output, usage and log paths. The CLI remains 1.0.103 and the same pinned
runtime is local, not an actual hosted workflow. At preparation no P04
inference had started.

## P04 Completion

Both approved native invocations complete, one tool call and one append each;
no schema-rejected call or correction. Haiku strict-gate-valid 64/100 at
111.07 seconds, USD 0.10206125 equivalent; A5 rationale 303 characters is an
instruction violation. Luna strict-gate-valid 56/100 at 107.97 seconds,
USD 0.01870419 equivalent; rationale-length check passes. Nine final-grade
differences; missing thought leadership forces D1-D3 to zero for both.

Native evidence is in
.copilot-tracking/sandbox/2026-10-24/rubric-model-pilot/native/comparison.json,
with raw CLI logs, usage, per-model append files and gate decisions alongside.
Runtime blob hashes, frozen inputs, actual prompt identities, requested/served
models, allowlisted tools and no reported source edits checked. Native usage
USD 0.12076544 equivalent; all-five aggregate USD 0.50707620. No further
assessment invocation is authorized. Keep original invalid results intact.
