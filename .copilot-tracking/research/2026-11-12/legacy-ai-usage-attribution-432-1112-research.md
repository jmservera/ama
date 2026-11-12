<!-- markdownlint-disable-file -->

# Task Research: legacy-ai-usage-attribution-432-1112

## Research Brief

* Topic: whether a legacy (pre-assistant) AI path still discards provider usage, and the smallest source-owned legacy path whose provider-returned usage can be joined to the existing Consumption ledger and output-record envelope, for the first #432 criterion.
* Purpose: decide one bounded offline slice (or "already implemented, no duplicate") before any code.
* Output mode: convergence. Posture: balanced (bounded internal task with named source targets); provenance: caller prompt.
* Non-goals: resident-host authority renewal, paid measurement, OD-51 approval, price or budget assumptions, new dispatch, new service or store, resident chat host, assistants.js, the independent #116 provider-spy tests, #184 design, any whole-#432 tick.
* Baseline: base `139176fa0382add781b1830b1ac9db785ed086fe`, branch `feat/demo-legacy-ai-usage-432-1112`, 2026-11-12.

## Research Parameters

| Item | Value |
| --- | --- |
| Date | 2026-11-12 |
| Evidence root | .copilot-tracking/research/2026-11-12/ (inline waves) |
| Delegation | None. One continuous trace through a single call path; inline fallback recorded. |
| Network, model, cloud | None. Local read-only inspection and local tests only. |

## Extension Registry and Provenance

| Extension | Disposition | Scope |
| --- | --- | --- |
| Repository instructions (AMA) | Selected | Branch workflow, validation tiers, knowledge-base log, evidence conventions |
| rpi-research, rpi-plan, rpi-implement, rpi-review | Selected | Phase protocols |
| Web development guidance | Skipped | No web files change |
| Security and python skills | Skipped | Small surgical change, no new surface |
| Company role agents | Skipped | No company fact needed |

## User Participation and Research Decisions

Non-interactive run. Caller direction recorded as controls: local-only, no push or PR/issue edits, no cloud or provider calls, one initial slice, stop with an exact blocker if a source restriction or schema prevents safe completion.

## Scope and Success Criteria

* Verify the unimplemented path against current source and the issue ledger.
* Name one legacy path, its join and its exclusions, and show Unknown handling for missing or invalid usage.
* Success: Planning Readiness `Ready`, or a precise "already implemented" result.

## Task Research Requests

None beyond the caller prompt.

## Direction Controls

Active: one slice; reuse existing wrappers, Store and ledger; synthetic spies only; no touching of other sessions' test modules; no price or budget assumption.

## Research Questions

1. Does a historical source restriction conflict, and what authority remains? (Q1)
2. Which legacy paths call a provider and do they discard usage today? (Q2)
3. Is a successful legacy response already joined to the ledger and output record, and how are missing or malformed usage and failures handled? (Q3)
4. Is a join defect or untested legacy behavior left that a source-owned, no-dispatch change can close? (Q4)

## Prior Knowledge Gate

Hypothesis under test, not fact: the tokenomics resource and issue body say legacy `Ai.run()` and `look_at()` use `_chat()` which "returns text only and discards usage".

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Issue #432 comments (2026-10-27 to 2026-11-07): criterion 1 unticked; resident-host window ended 2026-11-01; the 2026-11-07 comment blocks only the resident host persistent join and says it is "not a blanket prohibition on legitimate ledger integration" (W1). No restriction conflicts with a legacy-path join.
* Provider callers enumerated: `Ai.run` (priority at store.py:1008; text tasks at ai_tasks.py:324), `Ai.look_at` (ai_tasks.py:336), `Ai.evidence` (assistants, simulation lane, agents dispatch), and a direct `ai._chat` call in the resident chat host.

#### Wave 2: Deeper

* `_request` takes a `receipt` dict, reserves, dispatches, records usage in the receipt, then settles the ledger (C1).
* `run` and `look_at` merge the receipt (meter id, root, configuration, prompt hash, usage) into their result on every outcome (C2).
* `ai_registry.envelope` carries usage, meter id and root into the record envelope; `ai_tasks.finish` and priority join output through `publish_output`; reviews link through `review_intent` (C3).
* `ai_consumption.usage` returns None for non-dict, non-int, negative, over-bound, total-mismatch or cached-above-prompt values; `complete_in` then records Unknown liability and an owned alert (C4).
* Existing tests prove the legacy join at ledger, output and review level and call/depth limits for documents, but none asserts that legacy record-envelope usage equals the ledger completion tokens, or exercises missing/malformed usage through the legacy path (C5).

#### Wave 3: Contrarian

* Counter-claim: the stale statement may still hold somewhere. Only the resident chat host calls `_chat` without a receipt (C6); it is excluded and has no output record.
* Defect probe: `_request` sets `receipt.usage` before ledger settlement. If settlement raises, the failure branch settles `provider-unavailable` with no tokens while the caller still holds valid-looking usage, so a record envelope can state tokens the ledger does not hold (C1). To be proved by a failing-first test.
* The assistants path also drops usage with zero prompt tokens (C7); legacy does not. Not changed: different path, no evidence it is wrong.
* Reports read tokens only from ledger completions, so a report cannot show the envelope-only figure; the defect is confined to the retained record envelope.

#### Parent Synthesis and Disposition

* Rejected: new legacy usage capture. The hypothesis is false on current main (C1-C4).
* Accepted: one bounded correction plus legacy proof tests on the text-draft path (`Ai.run` through `ai_tasks.run_text_task`, task `briefing`), the smallest legacy path with a record envelope, output join and human-review join; it shares `_request` with `look_at` and priority.
* Deferred or excluded: `look_at` documents and images, priority, resident chat host, assistants, price, billing and authority work.
* Stale sentence in the tokenomics resource is superseded by this evidence and is to be corrected with a log entry.

#### Cycle Re-entry Evaluation

No re-entry: one code path, sources redundant, no new material question.

## Evidence Log

### Codebase Evidence

| ID | Evidence |
| --- | --- |
| C1 | src/core/src/zava_forward/core/ai.py:151 `_request`; usage into receipt at :200, settle at :202, failure settle at :206 |
| C2 | src/core/src/zava_forward/core/ai.py:246 `run` and :299 `look_at` merge the receipt on all outcomes |
| C3 | src/core/src/zava_forward/core/ai_registry.py:206; src/core/src/zava_forward/core/ai_tasks.py:254; src/core/src/zava_forward/core/store.py:1008 |
| C4 | src/core/src/zava_forward/core/ai_consumption.py:99 `usage`; :754 `complete_in`; :810 `publish_output` |
| C5 | src/api/tests/test_ai_consumption_api.py:460 and :978 (legacy join, limits); no envelope-versus-ledger usage assertion for legacy |
| C6 | src/core/src/zava_forward/core/chat_isolation.py:153 (resident chat host, excluded) |
| C7 | src/core/src/zava_forward/core/assistants.py:452 |

### External Evidence

| ID | Evidence |
| --- | --- |
| W1 | Issue jmservera/ama#432 body and comments, read with `gh issue view`, retrieved 2026-11-12 (read-only) |

### Contradictions / Conflicts

* The issue body and docs/reference/resources/ai-tokenomics.md (lines 77-81) say legacy paths discard usage; current source does not (C1-C4). The resource says its 2026-10-31 section supersedes code-path descriptions, yet the stale sentence remains. Recorded and to be corrected, not silently resolved.
* Installed editable distributions point at another checkout (/home/azureuser/source/ama). Validation uses the worktree src directories first on PYTHONPATH; the baseline `tests.test_ai_consumption_api` passes (32 tests) that way.

## Findings Mapped to Questions and Evidence

| Question | Finding |
| --- | --- |
| Q1 | No restriction conflicts. No authority renewal is needed because tests use synthetic local authority and a loopback provider spy. W1 |
| Q2 | Legacy callers `run` and `look_at` already return usage; only the excluded chat host drops it. C1, C2, C6 |
| Q3 | Yes: validated usage, meter id and root reach the record envelope; outputs and reviews join by root; invalid usage settles Unknown with an alert. C1-C4 |
| Q4 | One ordering defect and one legacy proof gap. C1, C5 |

## Key Discoveries

* The legacy usage-capture gap is documentation-stale, not source-missing.
* The only source defect in the join is statement order in `_request`.

## Alternatives and Decision State

### Selected Recommendation (convergence)

Add no capture. Make the receipt carry usage only after the ledger settled it, and add focused tests on the legacy text-draft path using the existing loopback provider spy: successful join, missing usage, malformed usage, provider failure, settlement failure, and unchanged workflow-only no dispatch. Correct the stale tokenomics sentence and log it.

Rejected: (a) change `_chat` return type: duplicates the receipt and breaks callers; (b) change the chat host: excluded; (c) align the assistants zero-prompt rule: unevidenced; (d) price or report changes: out of scope.

## Open Questions, Risks, and Residual Uncertainty

* The reorder changes behavior only when settlement raises; the targeted suite will show any dependent test.
* Real provider usage shape is unobserved; only synthetic spy payloads are used. No cost is stated.

## Current Decisions

Scope as selected; local only; no push.

## Unresolved Decisions

None for this slice. OD-51, price source, authority renewal, billing reconciliation and the held-out batch remain owner and Finance gates.

## Potential Next Research

Envelope-usage proof for `look_at` and priority; resident chat join (owner-gated).

## Planning Readiness

Ready. Research disposition: executed.

## Closeout Record

Research was read-only; no source edited. The RPI parent continues to Plan.

## Sources

* Issue #432 (W1) and the repository files in the Evidence Log.

## Artifact Self-Check

Questions answered with IDs; three waves recorded; no secrets; no tracking paths in source.
