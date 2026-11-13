---
title: Independent plan critique for the final criteria of #891 and #107
description: One final-candidate critique by the rubber-duck agent with direct dispositions
ms.date: 2026-11-13
---

## Execution

* Executed once, independently, by the `rubber-duck` agent against the research, plan and details artifacts. Verdict: proceed-with-changes. No finding conflicts with a confirmed owner decision, so none needed a user decision.

## Findings and dispositions

| # | Finding | Class | Disposition |
| --- | --- | --- | --- |
| 1 | Case sources reach the prompt without `redact`, so a question-only personal-data canary is too narrow | Blocking | Accepted and narrowed. Sources are an allowlist projection (`export_fields.chat_case`, role-scoped) that excludes resident name and phone by design; the test places canaries in resident name, phone and the question and asserts the provider bytes carry none of them, and the claim is stated as masking of input plus allowlisted projection, not redaction of every source |
| 2 | `by_capability` has no charge field, so charge per assistant cannot be asserted from the report | Blocking | Accepted. Per-assistant charge and tokens are recomputed from raw reserved, completed, output and review events; report fields (tokens, accepted, tokens per accepted) are compared separately; billing cost is not asserted beyond the supported report values |
| 3 | Guardrail tests could pass vacuously (uncited `ok`, zero calls only) | Blocking | Accepted. A baseline cited model answer must succeed first; budgets are patched before authority seeding; the exact `token-budget-limit` and `money-budget-limit` holds are asserted from ledger alerts or the envelope reason |
| 4 | Retention coverage incomplete | Non-blocking | Accepted. A configured period with an aged thread is purged under the switch and an unaged one is kept; revocation during transport withholds the model answer |
| 5 | Fenced opener and quality scope | Non-blocking | Accepted. Chat is dispatched through `Ai._request` (`urlopen` patched, as in `ChatDemoMeterOnSqlStore`); the assistants test uses the existing local HTTP fixture; quality-evidence is run reactively and the proactive request uses a non-quality assistant |
| 6 | Telemetry absence needs positive controls | Non-blocking | Accepted. Sentinels are asserted present in the provider request before absence is asserted in ledger, report, logs and task events |
