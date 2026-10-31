---
title: Resident advisory assistant prototype
description: Managed-identity bounded model assistance, permanent spend controls and activation limits
ms.date: 2026-10-31
---

## Current scope and AI contract (2026-10-31)

Refs #466. The owner explicitly confirms own-home sensor gauges/history and an
advisory resident assistant with AI in scope, using the existing synthetic data.
IoT remains a standing priority. Resident AI stays off in deployment behind the
existing activation settings; this direction does not authorize Azure changes,
paid inference, tariff renewal or live acceptance.

Earlier merged #474 already supplies synthetic temperature/humidity gauges,
history charts and equivalent text/table information for the signed-in home.
CO2 was an illustrative issue example, not an available generated channel.
The assistant explains own-case status, requested documents and form completion
with an advisory notice. It cannot submit forms, give consent or decide.

The current [API contract](../../src/api/README.md#preserved-bounded-azure-advisor-469)
extends the dated sentence-selection implementation below. Eligible typed
status, form, home and repair questions can receive short AI-generated answers
grounded only in the authorized case's plain-language update and host guidance.
Document questions retain locally rendered facts and references; AI may select
approved explanatory guidance but cannot replace those facts. Protected safety
and other workflow-only questions retain explicit human routes and rules labels.
Record-use permission is separate from sign-in, works consent and submission;
authorization is checked again before returning an answer.

The model/cap/credential decision remains the 2026-10-27 choice below: regional
Standard `gpt-4.1-mini` 2025-04-14, permanent USD20 inference reservation ceiling
inside USD30, managed identity only. No new choice or allocation is made here.
Default-off behavior, SQL accounting prerequisites and the existing
2026-11-01T00:00:00Z inference/tariff expiry are unchanged. The only assistant
settings remain `ZF_DEMO_ASSISTANT_ENABLED` and `ZF_DEMO_ASSISTANT_ENDPOINT`,
using the existing SQL managed-identity settings. No key or developer credential
chain is introduced.

Local synthetic/scripted-transport tests can exercise AI routing, text
rendering, isolation and honest off/outage fallback without credentials or model
calls. They cannot establish actual-model answer quality, current billing
headroom, authenticated live readiness, human accessibility or full WCAG
acceptance. Preserve those separate approval and verification gates.

## Current owner decision and implementation (2026-10-27)

Refs #469 and #466. Owner approval selects Azure OpenAI in existing RG `ama`,
managed identity only and a **USD20 inference ceiling**, within resident USD30
and renewed overall USD700 through 2026-12-31. This supersedes the older USD5
proposal below, not the resident-access, privacy or human-approval boundaries.

The optional `AzureAdvisor` performs actual Azure OpenAI inference to select
relevant explanatory sentences for the three existing questions. It is not
free-text chat or unrestricted generated advice. Mandatory own-case status,
closed/unknown facts, next step and document/form limitations are rendered
unchanged. The model sees only the safe mapped answer and approved optional
guidance, never email, address, raw stage, case ID, other cases, sensors,
uploads, credentials or conversation history. It can return only known
sentence IDs. Invalid, inconsistent, truncated or unavailable output returns
the deterministic answer labelled "Summary by rules - AI unavailable or usage
limit reached". Successful output says "AI suggestion, not approved".
Unknown requests are rejected before inference, with the human route retained.
No eligibility, legal, safety, financial, submission or consent authority exists.

Current model: `gpt-4.1-mini`, version `2025-04-14`, deployment `resident-mini`,
regional **Standard**, capacity 1, Sweden Central. UK South lacked an ordinary
small-model Standard option. ARM rejected nano Standard; its advertised SKU
was fine-tuned-model only, while ordinary 4o-mini Standard was retired.
Mini is the smallest current non-reasoning regional candidate verified here.
No silent GlobalStandard substitution or automatic model upgrade is enabled.

The [Azure retail prices API](https://prices.azure.com/api/retail/prices),
retrieved 2026-10-27 with service `Foundry Models`, region `swedencentral`,
returned regional mini input USD0.000484/1K and output USD0.001936/1K tokens.
The entire serialized request, including instructions and response schema, is
limited to 4096 ASCII bytes, conservatively bounded by 8192 input tokens
including protocol overhead, plus 256 output tokens, n=1, no retries, tools or
streaming. Worst-case estimated charge is USD0.004460544 per attempt.
Reserve **USD0.01 permanently before credentials/HTTP**, substantially above
that bound; the atomic lifetime limit is 2000 cents. No timeout, process death,
completion error or deployment refunds/reset the ledger. This is intentionally
conservative admission, not a claim that actual billing reaches USD20.
The cap controls this application's calls, not unrelated subscription callers.
Tariff approval and inference expire at 2026-11-01T00:00:00Z; funding renewal
does not extend the earlier configured showcase/session/SQL admission window.

The separate `resident_ai` SQL schema stores cumulative reserved cents and
attempt UUID, stable SHA256 of the authorised case ID, DB UTC time and nullable
actual input/output token counts. It stores no prompts or answers. Global
row locking serializes reservation and five-attempt rolling-hour admission
per synthetic resident mapping across instances, sign-ins, signing-key rotation
and restarts. The app gets only EXECUTE on `reserve` and `complete`; existing
case data stays SELECT-only through the resident view. Missing/corrupt/unreachable
accounting fails closed to rules without acquiring an inference token.
Counts-only usage logs omit resident identifiers, prompts, answers and tokens.

`ManagedIdentityCredential(client_id=<existing resident identity>)` is the
only credential route, scoped to `https://cognitiveservices.azure.com/.default`.
No keys or developer credential chain are supported. Explicit runtime settings
are `ZF_DEMO_ASSISTANT_ENABLED=true` and `ZF_DEMO_ASSISTANT_ENDPOINT`; the
existing `ZF_SQL_AUTH=msi` and `ZF_SQL_CLIENT_ID` bind the same identity.
Default is disabled. See the [API guide](../../src/api/README.md#resident-advisory-assistant-prototype-469)
and [infra runbook](../../infra/README.md#resident-azure-openai-469).

Actual ARM provisioning succeeded for `aoai-resident-469`, its `resident-mini`
deployment and the existing `id-resident-demo` identity's account-scoped
Cognitive Services OpenAI User assignment. No other resources, ingress,
groups or role assignments were changed. Provisioning is not live activation:
SQL migration, running-image/configuration readiness and authenticated
managed-identity inference must be evidenced separately.

## Historical prototype decision requested

Refs #469, part of #466. **For owner decision, not activation approval.**
Recommend a local rules-based assistant now. The separate resident panel offers
three questions: case status, documents to send and help filling in a form.
It is a bounded prototype, not free-text chat or an AI-generated answer service.
No paid/external model calls or Azure changes were made to deliver it.

| Option | Value and limits | Disposition |
| --- | --- | --- |
| Local deterministic provider | No inference cost, reproducible, no prompt disclosure; fixed topics only | Default prototype |
| Azure OpenAI GPT-4.1 nano deployment | Candidate small-model topic selector; availability, quality, regional processing and tariff unverified | Owner may evaluate later |
| Azure OpenAI GPT-4.1 mini deployment | Alternative if smaller model fails evaluation; no verified cost or quality advantage here | Owner may evaluate later |
| Free-text generated answers | Wider language support but greater leakage, invention, cost and evaluation surface | Deferred |

Model names are candidates, not claims of provisioned capacity or approved
deployment. The [Azure pricing page](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
retrieved 2026-10-27 describes region/offer-dependent estimates, but returned
`$-` for prices. No numeric tariff has been verified. Re-check actual account,
region, deployment/API compatibility and processing terms before any activation.

## Budget through 2026-10-31

The additional ceiling is **USD 5 total**, not per resident, day, worker or
restart. Spend for this prototype is USD 0. Propose at most USD 4 for inference,
keeping USD 1 headroom for other incremental charges. These are allocations,
not observed charges or a price quote.

The disabled adapter defines one fixed request: ASCII enum prompt <=512 bytes,
max_tokens=16, one completion, no tools, history, retries or streaming.
Before credentials or HTTP, a future host must atomically reserve a conservative
USD upper bound for that exact envelope at a reviewed tariff, across all
instances/restarts, with an aggregate inference cap <=USD 4. Input accounting
must include provider message overhead. Timeout/error attempts retain their
reservation until billing is reconciled; there is no automatic refund/retry.
Reject when insufficient, unknown or after 2026-11-01 00:00 UTC. Azure budget
alerts alone are not a hard cap.

The adapter requires an explicit reservation callback with these limits, not
an in-memory balance. This PR supplies no durable ledger or activation wiring.
Until its implementation and tariff are independently accepted, keep the real
provider disabled. All tests use fake token/reservation/HTTP functions.

## Credentials and configuration

Prefer a host-supplied `ManagedIdentityCredential` token callback for
`https://cognitiveservices.azure.com/.default`, with only the required Azure
OpenAI inference role on the selected resource. This follows Microsoft's
[managed identity guidance](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/managed-identity)
(page dated 2026-08-04, retrieved 2026-10-27). Do not use a default credential
chain that silently selects a developer account in a deployed service.

If a key is unavoidable, the owner must separately approve a Key Vault-backed
host adapter, least-privilege retrieval, rotation and retention. That route is
not implemented here. Never place keys in browser code, source, prompts or logs.
No secrets, .env, private dataset or existing verifier file is read for this work.

The Azure adapter is configured in Python with endpoint, deployment, explicit
enabled flag (default false), short-lived bearer-token callback and durable
reservation callback. Endpoint is restricted to an HTTPS Azure OpenAI hostname,
redirects refused. There is no environment-based auto-enable switch. The
shipped resident app always uses the deterministic provider unless a future
reviewed host explicitly injects a different provider. Existing deployed app
configuration and infrastructure remain unchanged.

## Grounding and isolation

The assistant endpoint obtains the signed-in resident's existing session-bound
view, including a fresh case fetch and admission check on every request.
Only that view's authoritative progress/next-step/closed text enters the local
answer builder. There is no case ID in the request or provider interface, no
cross-case retrieval, vector index, document corpus or conversation history.

The provider receives only `status`, `documents` or `forms`, and may return only
the identical topic. A real model is deliberately just a replaceable constrained
selector; it adds little value here and is not recommended for activation.
Resident facts, addresses, email, measures, identifiers and question text never
enter its prompt. All answer text is composed locally. Invalid model output
is rejected, not displayed or substituted as a successful AI answer.

Status uses the same constant plain-language mappings as the resident page.
Closed/unknown status remains explicit. The current projection has no requested
document facts: the assistant says it cannot tell which documents were requested,
not that none are needed. Form help is generic; it never invents or fills
personal details. Connecting to #467's future document requests needs its own
authorization and contract review.

## Advisory and human boundaries

Visible notice: advisory only, cannot submit forms, give consent, book works or
make decisions. Rules output says "Summary by rules"; an injected AI selector
must say "AI suggestion, not approved". The resident can speak to their housing
officer or visit/write to the office without using the panel. No contact details,
appointments, response times, legal, safety or financial determinations are
invented. The panel cannot record or forward a question.

Native labelled question control, submit button and live result/status regions
reuse Fluent 2 token foundations, visible keyboard focus and reduced motion.
Text provides all information without colour or images. This is not completion
of Fluent component adoption or WCAG/screen-reader/user acceptance.

## Threats and verification

* Prompt injection: arbitrary input is not a prompt. Reject unknown topics and
  extra keys; malicious model replies cannot become resident-facing text.
* Leakage: test two different own-case sessions and forged body/query/header
  case selectors, revocation, expired sessions and delayed replies after logout.
  Prompts contain only fixed topics; no payloads or provider exception messages
  are logged. No question/answer storage or analytics is added.
* Unauthorized requests: reuse same-origin/CSRF checks, bounded JSON bodies,
  signed expiring cookies and the existing concurrency limit.
* Cost/exfiltration: default false, expiry and atomic reservation before token
  acquisition/HTTP; fixed prompt and output ceiling; no redirects or retries.
* Reliability/accessibility: test explicit unavailable errors, retry, keyboard
  interaction, live status, 320px reflow and reduced-motion mode in local Chromium.

Unit and focused browser results are recorded in the PR. Hosted CI/rubric/review,
real-user comprehension, screen readers, real identity and privacy/DPIA approval
remain separate. No live resident service or consequential automation is accepted.
