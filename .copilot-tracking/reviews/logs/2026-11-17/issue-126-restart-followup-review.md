<!-- markdownlint-disable-file -->
# RPI Review: issue #126 restart follow-up (six-module batch and three evidence-quality gaps)

* Execution: executed once, independent `code-review` sub-agent, read-only, 2026-11-17, scoped to the follow-up changes record, the additive "Restart Follow-Up Update" section of the 22-row table, the follow-up plan/details/critique/research/state, the external evidence under `evidence-restart-126/` and the witness log. Assessed boundary: start commit `23eca3a5551fe355969f07651660d1b2ce40ae5c` plus uncommitted `.copilot-tracking` changes.
* Outcome: Partial (reviewer verdict). One factual overstatement (MAP-01) remains in the reviewed text; no closure, acceptance or readiness is implied by this review.
* Not repeated in this task (one-pass rule). The original parent Review (`.copilot-tracking/reviews/logs/2026-11-17/issue-126-residual-source-assessment-review.md`) is a separate, unchanged record.

## Reviewer verdicts (condensed, original findings preserved)

| Criterion | Verdict |
| --- | --- |
| A batch C log supports claims (125 run, OK, 0 skipped, per-module 32/5/29/22/18/19, exit 0, log SHA-256; 11 installed modules hash-equal to start blobs) | Pass |
| B six modules are in `src/core/tests`; orchestrator `test_source_monitor` is a separate file and correctly excluded | Pass |
| C seven per-row dispositions cite tests that ran `ok` (16 distinct names each found once), tiers unchanged, synthetic qualification stated, no over-claim | Pass |
| D MAP-01 label and MN-3.2 rationale accurate; candidate tests exist | Fail on one claim (finding 1); MN-3.2 rationale matches the tier rule |
| E verifier reproducible (68 references, 42 symbols, 42 blobs, 27 test ids, 23 test names; output byte-identical on rerun) | Pass |
| F table diff additive (38 insertions, 0 deletions), original Review unchanged, only `.copilot-tracking` paths, no `log.md` or `memory.md` change | Pass |
| G no readiness or approval claim; absent approvals stated; no issue ticks | Pass |

## Findings

1. Medium: the MAP-01 explanation said the cited paired-equity test "does not exercise `core/ranking.py` `_support`" and that no test run exercises that behaviour. The cited test calls `_rank_with_policy` (the ranking function), whose `reasons()` calls `_support` (`ranking.py:124`) and whose `support` rule lambda (`ranking.py:83`) can too. `_support` is therefore exercised indirectly. What is not asserted by that test or by any executed batch is the `support_unknown` reason code or the "Unknown sorts with No" behaviour. The tier (insufficient) and the "context only" label stand; the wording needed to say "not asserted" rather than "not exercised".
2. Info: parent batch A/B logs are not retained at their original location, so test ids from those batches are verified for existence only. Already disclosed.
3. Info: the stray first witness record in `evidence/issue-126/issue-126/events.jsonl` is retained and disclosed.

## Routing and post-Review handling

* Finding 1: wording in the follow-up table section and the changes record corrected after Review (recorded as a post-Review correction in the changes record); this review text is unchanged. The candidate `support_unknown` assertion tests remain for later work.
* Findings 2 and 3: disclosure only; no further action in this task.
* Remaining work (not done here): run the candidate ranking tests (`src/api/tests/test_ranking_policy.py`, `src/agents/tests/test_cohort_manifest_draft.py`) in an authorised later batch; all qualified owner, DPO, Legal, Finance, real-model, witnessed-restore, Azure and EU-applicability evidence and approvals remain absent.
