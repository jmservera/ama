<!-- markdownlint-disable-file -->
# Task Research: issue #108 offline evaluation coverage record (agents only)

* Task id and slug: `108-offline-coverage-0008`
* Parent task: `ai-parent-integration-2333` (exclusive child of the AI parent on `feat/demo-ai-integration-1112`)
* Date: 2026-11-13
* Base: `bbdacadcb` (head of PR #1495, which must not change)
* Research disposition: `reused` (read-only report `rpi-108-local-demo-readiness-2359-result.json`, base `774a91e5`), re-verified on this base with a fresh scripted probe (below)
* Planning Readiness: `Ready`

## Evidence reused and re-verified

* The prior report found that `ai_eval.run_task_checks` claims citation, Unverified and workflow-only checks for "catch-me-up, message, briefing, funding" but never calls `funding_draft` or `read_document`, and the evidence gate carries no per-task coverage, so unexercised registry families are not declared.
* Re-verified on this base with a scratch probe under the external evidence root (no repository write, scripted provider only):
  * `Store.funding_draft` reaches `Ai.run("funding_draft")` and returns `source=ai` under a scripted `_chat`. A cited answer must use labels that the case really has (`Address: T-1 Eval Road`, not the full postal address); a wrong label is correctly reported as unresolved and Unverified.
  * `Store.read_document` does NOT use `Ai.run`. It uses `Ai.look_at`, which returns `task="read_document"` and always cites `Document: <name>`. A spy on `Ai.run` alone can never observe it.
  * `Store.add_document` needs caller metadata (`source`, `source_version`, `reason`) and the local signature scan returns `clean` for a short text file.
  * `Store.briefing` reaches `Ai.run("briefing")` with `source=ai`, but the existing check only asserts `verified and citations` on it.
* Dispatch namespaces differ by path (the critique topic):
  * Retained tasks dispatch through `Ai.run` (bare ids `briefing`, `message`, `summary`, `priority`, `funding_draft`) or `Ai.look_at` (`read_document`). Release records use `legacy:<id>`.
  * The five assistants dispatch through the core assistant planner (`assistants.py`, `planner(..., ai.fast, ...)`), never through `Ai.run` or `Ai.look_at`, and their ids are capability names (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`).
  * `ai_registry.tasks()` holds 13 ids: 5 assistants, 6 retained paths, `chat-case-conversation` and `aftercare-concern-pack`.
* False coverage hazard: `Ai.run` returns the template with `source=template` when the provider is unconfigured, gated, offline or fails validation. A task that only returned the template has not exercised the model path and must not be called covered.

## Selected approach

* In `src/agents` only: `ai_eval` records every `Ai.run` and `Ai.look_at` outcome, keyed by the returned `task`, with whether the scripted `_chat` was actually reached and the returned `source`.
* `evidence_gate` gains a registry-derived `task_coverage` record covering every id in `ai_registry.tasks()` with one of three statuses: `exercised offline`, `template fallback only`, `not evaluated by this harness`. The wording states offline dispatch and control checks only, never held-out semantic accuracy.
* Assistants, chat and the concern pack are fixed as `not evaluated by this harness`. An observation whose task is not a retained id, or is an assistant id, is a namespace error and fails the run.
* `run_task_checks` gains funding draft checks and read document checks with a constructed public text fixture. Honest docstring and README note.
* Recipe hash metadata: not required (no recipe is changed). No dependency, workflow, gate or tool file is touched. Focused tier.

## Boundaries

* No provider, model, network, Azure, budget, threshold, independent label or human acceptance. Actual #108 history stays UNKNOWN, not zero. No renewed correction pool; initial scope only.
* The #108 held-out and human criteria stay unticked; this increment proves none of them.
