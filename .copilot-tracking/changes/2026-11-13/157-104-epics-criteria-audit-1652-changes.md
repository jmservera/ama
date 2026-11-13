<!-- markdownlint-disable-file -->
# Changes: #157 and #104 software-provable criteria audit (2026-11-13)

Docs-only audit. No source, test, issue or remote change. Audited tree: worktree HEAD `3ffb8c0e7`; `origin/main` `dad57ef4f` differs only in #131 tenure files, none read here. Strict rule: PROVEN only when code plus a passing test show the whole criterion text; any human approval, measurement or unimplemented element is NOT FULLY PROVEN with the exact gap named. No issue checkbox should be ticked on the basis of a NOT FULLY PROVEN row.

## Tests run (all OK)

The named `/tmp/venv-epics-1652` was deleted by a sibling process mid-run, so `/tmp/epics1652-env` (pip, editable `src/core`, `src/agents`, `src/api`) was used and removed before commit.

| Scope | Selection | Result |
| --- | --- | --- |
| core | `test_chat*.py` | 146 OK |
| core | `test_ai_*.py` | 84 OK |
| core | `test_regulatory_usage.py` | 6 OK |
| core | `test_resident_decisions.py` | 419 OK (149 skipped) |
| agents | `test_chat*.py` | 87 OK |
| agents | `test_paired*.py`, `test_candidate_comparison.py`, `test_ai_eval.py`, `test_review_effectiveness.py` | 31, 19, 20, 34 OK |
| api | `test_ai_boundary`, `test_ai_tasks`, `test_ai_call_site_inventory` | 6, 69, 6 OK |
| api | `test_chat_panel`, `test_chat_isolation` | 58 OK (1 browser opt-in skipped), 32 OK |
| api | `test_assistant_release`, `test_ai_consumption_api`, `test_assistants` | 60 OK (7 skipped), 37 OK, 136 OK (59 skipped) |

Skips are opt-in browser or SQL-prerequisite tests; no SQL or browser coverage is claimed.

## #157

| Criterion | Verdict | Evidence | Gap |
| --- | --- | --- | --- |
| No memory is used as evidence for a controlled decision | NOT FULLY PROVEN | Citing a memory id is refused: `src/core/src/zava_forward/core/chatthreads.py:279-284` (`CM-` prefix, "Memory is never evidence"); lifecycle memory enters a prompt only as `authority=none, evidence=False` (`chat_privacy.py:311-316`); `core/tests/test_chat_memory.py:115`; the proposal path never sends memory text or ids to the model or into the stored envelope (`api/tests/test_assistants.py:1491`, synthetic canary, simulated provider). The served `ChatPanel` declares `memory_used=False` (`chat_panel.py:481`, `server.py:1055`). | The control rejects memory ids, not memory-derived text; `memory_used=False` is a constant the panel declares, not an observed measurement (agents `chat_eval` says the same); the legacy `ChatIsolation.turn/build_prompt` (`chat_isolation.py:105-136`) can put labelled memory in a prompt; no served route or non-test code calls `turn` (grep of `src/api`, `core`, `agents`), only the `chat_eval` component probe calls `build_prompt` (`chat_eval.py:258`), so this is a dormant path, not a proven exclusion; whether a person relies on memory for a controlled decision is outside software. |
| Chat consumption is bounded and reported before activation: calls per request, context size per thread, memory use and per-role limits, with a fallback to the workflow-only path when a limit is reached (BRD AC-103) | NOT FULLY PROVEN | Bounds enforced: one call, no retries, 600 output tokens, `MAX_INPUT_CHARS=16000`, `MAX_HISTORY_CHARS=4000`, 12-message window (`chat_panel.py:260-262`, `chat_isolation.py:31`). Reported before activation by `/api/chat/status` limits (`server.py:1048-1055`; `api/tests/test_chat_panel.py:609` asserts calls and retries; `chat.js:53` renders them). Fallback: over-limit goes to `LIMIT_REACHED` workflow-only reply without dispatch (`chat_panel.py:695,725`; `core/tests/test_chat_panel.py:382`); call, depth, token, money and expiry limits hold dispatch in the ledger (`ai_consumption.py:599-654`; `core/tests/test_ai_consumption_demo.py:15,20`); a model failure also falls back. | No per-role limit exists: one task limit applies to every role. Only calls per turn, per-prompt context and a declared constant for memory are reported; no per-thread usage report. Status limits `context_chars`, `history_chars` and `memory_used` have no Python test assertion (only a JS fixture, `test_chat_widget_focus.py:315`). The chat authority is a synthetic demo record (`chat_demo_meter.py:23`: 20 calls, 100000 tokens, amount 1) and the status calls the caps "engineering caps, not spend authorization". The BRD AC-103 text (`docs/brds/agentic-retrofit-programme-brd.md:1604`, the FR-052 row carrying AC-102 and AC-103) is the value-destination criterion with calls per request and agent depth; the issue's longer list is wider than that text. |

## #104

| Criterion | Verdict | Evidence | Gap |
| --- | --- | --- | --- |
| AI never approves, executes, ranks or mutates controlled records | NOT FULLY PROVEN | Hostile-output tests leave controlled fields, ranking and the funding approval chain unchanged for the retained tasks, human review and document reading (`api/tests/test_ai_boundary.py`, 6 tests); chat cannot change a case record or approve (`api/tests/test_chat_panel.py:271`); proposals stay unapproved and domain data unchanged (`test_assistants.py:446,1491`); the registry prohibits ranking, approving, signing or sending (`ai_registry.py` `PROHIBITED_PURPOSES`). | Counterexample to the literal wording: `Store.funding_draft` (`store.py:1177-1200`) writes model text to `funding.draft` and moves `funding.status` from Not started or To prepare to Draft ready with no review step; `test_ai_boundary.py` allows this by name (`ALLOWED_DRAFT_FIELDS`, `FUNDING_STATUS_CEILING`). A second AI-written field: `Store.read_document` stores model text in `doc["summary"]` with no review step (`store.py:820-824`), also allowed by the same test. Approval and submission still need a person (`funding_step`). "Unchanged" is proven only for the tested paths, not every capability or deployment. |
| #432 is complete, or its gap is recorded: Total Cost of AI and cost per accepted proposal are reported beside the quality floor, or stated as Unknown with the missing inputs named | PROVEN for the gap branch; completion not demonstrated | #432 is OPEN with four unticked criteria (per-call join, Azure reconciliation, held-out batch, capstone feed). The gap is recorded in `docs/reference/resources/ai-tokenomics.md` (criterion table, "cost remains Unknown": no applicable rates or billing record, OD-51, real quality and TCA inventory, held-out authority). Software states Unknown: the ledger report keeps `token_cost`, `cost_per_accepted_proposal`, each of the five TCA components and `total_cost_of_ai` Unknown without billing and inputs (`ai_consumption.py:1203-1267`; `core/tests/test_ai_consumption_demo.py:25`) and reports them beside quality measures and status; `paired_trial.cost_per_accepted_check` returns Unknown with every missing input named (`paired_trial.py:121`). | Do not read this as #432 delivered: no price, billing or reconciled cost exists. The ledger names Unknown fields and coverage gaps rather than listing each missing input in one list; the paired-trial measure is per accepted chat check, not per proposal. |
| No registered AI capability is enabled beyond the exercise without finite, owner-approved call, token and budget limits and an owned alert (BRD NFR-012) | NOT FULLY PROVEN | Fail-closed gates: dispatch is held for unknown authority, price or liability, expiry, request call and depth limits and call, token and money budgets, each raising an owned alert (`ai_consumption.py:599-654`; `authority` requires 1-8 finite budgets and an owner, `:452-478`); `authorizes_live` is false unless every authority is a validated person, except the demo-only switch with `ZF_DEPLOYMENT_PROFILE=demo` (`ai_registry.py:173-188`; registry text records no approval); `test_ai_call_site_inventory.py` fails an unclassified provider call site; assistant `Limits` default off without authority, finite allowance and expiry (`test_assistants.py:1344`). No beyond-exercise breach was found. | "Owner-approved" cannot be verified by software: owners and approvals are opaque references, and the only live authority is the synthetic demo record. The legacy assistant `Limits` path has call and token allowance but no money budget or alert of its own. Real owner approval, OD-51 budgets, and named alert owners are human gates. |

## Gaps and follow-ups (not actioned here)

* Decide whether `funding_draft` should stop advancing `funding.status` automatically (and whether `read_document` summaries count as controlled data), or the #104 criterion should name the draft-field exception.
* Add per-role limits, per-thread usage and a measured (not constant) memory-use report to chat status if AC-103 is read as the issue lists it; add Python assertions for the status limit keys.
* Keep #157 and #104 criteria unticked until human approval evidence (owners, budgets, alert owners, Legal and DPO) and #432's open criteria exist.

## Non-actions

No push, no GitHub issue edit, no source or test change. Disclosure: no web design work; no SQL, browser or Azure checks ran.
