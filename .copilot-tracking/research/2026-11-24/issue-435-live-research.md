# Research: issue 435 live 2026-11-24

Disposition: executed. Planning Readiness: Ready.

## Goal

Place the "decision model first" Tokenomics point in the capstone pitch and add a dated, labelled comparison of decision model, small GPT model and large LLM. No invented prices or savings.

## Findings

* Prior passes (2026-11-18 to 11-23) already settled placement (owner 2026-11-13: slide 22 / S18 plus B25 and B27), the batch (#432, 12 synthetic proposals, usage only) and a statement audit. Nothing yet explains why yes/no checks avoid a model.
* Repository evidence of deterministic yes/no checks (read 2026-11-24): `src/core/src/zava_forward/core/gates.py` (pass, fail, unknown; unknown never passes), `doc_controls.py` (scan status clean or not), `form_validation.py` (deterministic validation, "Not evaluated" without approved rules), `ai_decision.py` (continue/narrow/pause/retire by ordered limits). Speaker script page 17 already says known gates and arithmetic do not need generation. Local scanner is dev-only; Defender scanner is not proved against a real account.
* Public sources retrieved 2026-11-24:
  * OMG DMN 1.7 beta, published September 2026: decision tables are an executable expression language; interchange by XML. Beta, informational.
  * OpenAI model selection guide: "GPT-6 Luna for small, repeatable tasks", e.g. extracting fields when the expected result is clear; "keep the lightest setting that meets your quality bar".
  * OpenAI API pricing page (standard tier, USD per 1M tokens): gpt-6-luna input 0.10 / output 0.50; gpt-6.2-astra input 8.00 / output 40.00 (short context). List prices, not Zava's deployment price.
  * Microsoft Learn model router (ms.date 2026-11-18): simple prompts to small models, deep reasoning to frontier models. Microsoft Azure OpenAI pricing page fetched but prices render as "$-" without a browser, so no Azure price is used.
* A decision model has no per-token price. Its cost (hosting, authoring, review) is not measured here: label Unknown.
* No acceptance-quality comparison exists between a model and the rules on Zava checks, so no saving can be stated.

## Acceptance criteria baseline

Criteria 2 (mentor) is unprovable without the mentor. Criterion 3 tick is unsupported (computed timing only). Others as in the 2026-11-23 records.
