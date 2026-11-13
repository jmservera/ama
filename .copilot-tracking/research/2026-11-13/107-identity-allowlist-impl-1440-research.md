# Research: #107 identity-field sanitisation (1440)

Disposition: executed. Planning Readiness: Ready. Refs #107, #432.

Evidence:

* `assistants.py` `shape_result` picks provider/deployment/model as exact str; provider/deployment truncated to 120, model via `ai_consumption.bounded_model` (str <= 512). No character restriction.
* `ai_consumption.bounded_model` also feeds `Consumption.complete_in` (ledger stores `reference(safe_model)`, but `model != reservation["model"]` uses the raw value) and `ai.py:200-203`.
* `assistants.py:1576` passes the envelope model to `consumption.complete_in`; `:1704` compares envelope model with released `serving_model`.
* Compatibility matrix: readiness changes record `.copilot-tracking/changes/2026-11-13/107-identity-allowlist-readiness-1143-changes.md` (trusted-proxy, scripted, local-test-double, azure-openai, password, `offline-extractive; zero model calls`, test-model, m-1, etc.): all match `[A-Za-z0-9][A-Za-z0-9._:/@+-]*` except the offline literal, which is allow-listed explicitly.

Decision: one shared `ai_consumption.safe_identity(value, limit)`; non-conforming str -> `unverified-identity`; non-exact-str -> None; secret prefix `sk-` at a token boundary -> `unverified-identity`. Provider/deployment keep truncation to 120 before validation; model over 512 stays None.
