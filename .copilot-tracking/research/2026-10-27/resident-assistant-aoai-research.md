---
title: Resident assistant Azure OpenAI research
ms.date: 2026-10-27
---

<!-- markdownlint-disable-file -->

## Research Brief

Implement #469, refs #466, with Azure OpenAI in existing RG ama, managed
identity only, a hard USD20 inference ceiling and deterministic fallback.
Audience: owner and implementation reviewer. Output mode: convergence.
Posture: focused, selected for the explicit bounded implementation request.
No interaction is needed: the owner explicitly requests the full ordered loop.

## Research Parameters and Direction Controls

Scope: own-case status, required documents and form guidance; advisory only.
No ingress changes, resource groups, keys, unrelated roles or mvp changes.
Owner decision dated 2026-10-27 supersedes the older USD5 proposal: resident
USD30 within renewed USD700 through 2026-12-31; model ceiling USD20.
Branch feat/resident-assistant-aoai already exists in the requested worktree,
clean at 885ee05f, with merged #474 ancestry. #466 is an issue, not a PR.
Target main because the parent implementation is merged.

## Extension Registry and Participation

Repository instructions and RPI phase skills apply. Research is inline:
this is one coupled runtime/infra trace, not independent research lanes.
No web changes are planned; existing visible advisory notice is retained.
Specialist delegation is reserved for independent plan critique and Review.

## Candidate Areas and Questions

* Existing resident provider, own-case boundary, deployment and storage.
* Azure OpenAI Standard quota, model price, identity authentication.
* Durable atomic budget reservations, per-resident limit, error fallback.
* Safe reachable live smoke and unchanged ingress.

## Research Cycle Log

### Cycle 1: Wider

The existing assistant is a topic echo adapter, not generated assistance.
The host only accepts three topic enums; status is mapped locally from a fresh,
session-authorised case. The deployed resident identity has no state volume.
Reflection: a process-local balance cannot enforce a lifetime ceiling.

### Cycle 1: Deeper

UK South advertises GlobalStandard only for the two small candidates.
Sweden Central advertises Standard for gpt-4.1-nano 2025-04-14 and gpt-4o-mini.
The public retail API returns regional nano input USD0.000121/1K and output
USD0.000484/1K. Select nano Standard capacity 1, subject to deployment success.
Use the existing SQL service for a separate, atomic accounting schema and two
fixed procedures. Grant only object EXECUTE, no database role membership or
Azure role beyond OpenAI User. No case data is stored in accounting.
Reflection: reserve USD0.01 before every attempt; 2000 attempts exhaust USD20.
This intentionally overestimates a <=4096-byte prompt plus <=256 output tokens.
Keep failed reservations; log actual token counts, never prompts or replies.

### Cycle 1: Contrarian

Model instructions alone cannot guarantee no eligibility/legal/safety/financial
advice. Preserve fixed topic UX and use schema-constrained sentence selection
from the own-case authoritative answer plus approved guidance, not unrestricted
model prose. Unlike the prior echo, the model chooses and sequences explanatory
sentences. No user prose or raw SQL fields enter the prompt; validated sentence
IDs are rendered locally. Deterministic output remains available on every error.
Azure budgets are alerts, not a hard cap. Atomic SQL reservations survive scale
to zero, concurrency, restart and redeploy; missing SQL procedures fail closed
to rules before credentials or HTTP. No persistent app volume or new storage
role is needed.
Reflection: live activation requires the accounting migration and a rebuilt app;
the current live revision lacks both. No ingress change is authorised here.

## Evidence Log

* C1: `src/README.md:66` documents local RPI tier and publication receipts.
* C2: `docs/architecture/resident-assistant-prototype.md` is the prior design,
  to be reconciled against the new owner decision.
* C3: `src/api/src/zava_forward/api/resident_demo/app.py:312` enforces topic,
  session, same-origin and CSRF boundaries.
* C4: `src/core/src/zava_forward/core/resident_assistant.py:53` composes only
  local authoritative status and approved process guidance.
* C5: `infra/sql/resident-showcase.sql:100` denies writes in the case schema;
  accounting must be separate, retaining the read-only case projection.
* C6: `src/api/src/zava_forward/api/resident_demo/__main__.py:20` is the single
  runtime composition point.
* W1: https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/managed-identity
  retrieved 2026-10-27: custom subdomain, bearer auth and resource-scoped role.
* W2: https://prices.azure.com/api/retail/prices
  retrieved 2026-10-27, filter Foundry Models / swedencentral / 4.1 nano:
  regional input 0.000121 and output 0.000484 USD per 1K tokens.
* W3: Azure CLI model list, 2026-10-27: Sweden Central supports nano Standard;
  UK South supports only GlobalStandard for these candidates. Usage queries
  returned empty arrays, not proof of available quota.

## Alternatives and Decision State

Accept bounded model-selected explanatory sentences, SQL atomic reservation,
managed identity only and a standalone default-off Bicep module. Reject
unrestricted prose, ephemeral accounting, automatic refunds, API keys and a
silent GlobalStandard substitution. The resource-group location does not
force the account's location; Sweden Central preserves regional Standard.
No actual resident data is authorised.

## Risks and Residual Uncertainty

Actual regional deployment quota and SQL migration reachability require live
execution. Existing resident revision currently has null ingress; another
session owns ingress. Do not claim a live authenticated smoke without one.
Accounting grants are narrow SQL object permissions, not Azure role assignments.

## Planning Readiness

Ready for implementation planning. Research disposition: executed. One complete
focused three-wave cycle; material architecture questions are evidence-backed.
No additional cycle is justified before implementing and observing live results.
Self-check: scope, constraints, code and external evidence, alternatives, risks,
participation and readiness recorded. Parent continues to Plan.
