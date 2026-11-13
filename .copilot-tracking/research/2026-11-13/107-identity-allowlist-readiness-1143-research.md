# Research: #107 identity-field allow-list readiness (1143)

Refs #107. Read-only audit; tracking-only write surface. Research disposition: executed. Planning Readiness: Ready.

Required docs read at start (case study original/addendum, reference README, memory). Base `3b05143179`.

## Correction-history evidence

* `gh pr list --search 107`: merged #287, #293, #863 (closed duplicate #860), #915, #1095, #1166, #1253, #1255, #1268, #1271, #1281, #1489, #1495 (feature/test/doc PRs; none labelled a "review-correction cycle").
* `gh issue view 107` comments (owner): 2026-10-15 #287 status; 2026-10-31 closure audit (C6, C8, C10, C13, C15-C17 unmet); 2026-11-07 exact-head review of `7c98d687`; #1255, process-race and restarted-clamp publications; no comment states a numeric count of spent source-correction cycles for #107.
* `.copilot-tracking/` has 20+ #107 review files (2026-10-15 to 2026-11-12). Their "correction" hits are plan-critique corrections or plan/deviation corrections (for example 2026-11-12 process-material-binding critique "required corrections: items 1-3 before coding"), not counted against the 5-cycle default.
* Demo-run ledger: the only wave record for this finding is line 13 (`rpi-107-telemetry` -> `3417239f72`, Conformant-with-findings, "identity-field free strings ... routed"). The ledger's "Final fifth correction spent" at line 14226 concerns #233, not #107. No ledger line gives a #107 spent-correction number.
* Result: documented spent source-correction cycles for #107 = NOT ESTABLISHED (unknown). Not assumed zero. Documented PR/review activity is not a cycle count, so it neither proves nor disproves five spent cycles; HELD rests only on the count being unestablished.

## Source facts (`src/core/src/zava_forward/core/assistants.py:441-452`)

* `shape_result` copies `provider`, `deployment`, `model`, `outcome`, `source` with `pick`.
* `model` goes through `ai_consumption.bounded_model` (`ai_consumption.py:327`): any `str` of at most 512 chars, else `None`. No charset or allow-list check.
* `provider` and `deployment` are only truncated to 120 chars; any string survives.
* Envelope identity feeds the model record (`assistants.py:318`), meter completion (`:1576`) and the serving-model comparison against released `serving_model` (`:1704`), and `simulation_lane.py:500`.
* `runtime_binding` (`:411-423`) defines the trusted values: `provider` (default `azure-openai`), `deployment` (`ai.fast`), `model_version` (default `unattested`).
* Callers: `agents/dispatch.py:242,248` and `Assistants.execute` (`:1844`) only.

## Compatibility evidence (static, no tests run)

Literal identity values in `src/{core,agents,api}/tests` and sources: `model` = test-model(16), offline-extractive(5), none(3), synthetic(2), m1, m-1, m, live, other-model, model-id, unattested, synthetic-adapter; `provider` = trusted-proxy(6), scripted(3), local-test-double(3), azure-openai, password, `offline-extractive; zero model calls` (fixture and paired report only, not demonstrated to pass through `shape_result`); `deployment` = test, capable, d, standard. A strict charset allow-list excluding spaces or semicolons could break the `offline-extractive; zero model calls` string if it reaches `shape_result`. Not proven either way.
