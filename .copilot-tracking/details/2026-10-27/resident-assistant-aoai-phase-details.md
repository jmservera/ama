---
title: Resident assistant Azure OpenAI phase details
ms.date: 2026-10-27
---

## P01

P01-T01: Separate resident_ai schema in the existing SQL database, budget row
with cumulative reserved cents, reservation rows containing pseudonymous
resident handle, DB UTC time and nullable actual token counts. Two fixed
procedures reserve and complete; object-level EXECUTE only. No refunds or
balance reset on deployment. Missing ledger fails closed before credentials.
Host obtains stable handle from the verified session, never request fields.

P01-T02: Retain FakeProvider and legacy adapter compatibility. Add a bounded
advisor receiving Topic and CaseProgress only. Model chooses sentence IDs from
the current own-case catalogue; validate IDs, uniqueness and mandatory coverage.
Never pass address/email/raw stages/history/user prose. Label successful
inference AI; errors explicitly label rules fallback without provider details.
Reauthorise after inference so revocation/expiry is not bypassed by latency.

## P02

P02-T01: Standalone resident-assistant.bicep, enable=false; existing identity
id-resident-demo. RG ama guard; nano 2025-04-14 Standard capacity 1 in
swedencentral. Disable local auth, version auto-upgrades and dynamic quota.
Only account-scoped Cognitive Services OpenAI User role; no app/ingress patch.
App enablement is an explicit host configuration, default rules.

P02-T02: Update existing architecture page, API/infra READMEs and knowledge
index/log. Record verified tariff and conservative one-cent reservation,
expiry, ledger bootstrap permissions and rollback. SQL migration remains an
explicit administrator operation using existing Entra tooling, no keys.
Account/deployment resource listing is the source for cloud evidence; never
claim the old app revision runs newly written code. Live unauthenticated probes
are allowed; authenticated smoke requires an already available session, never
read the owner credential or stored secrets.

## P03

P03-T01: API provider mocks test exact prompt, malformed usage/output, cap/rate
before token and transport, identity mode, timeout retention and no retries.
Own-case HTTP tests retain forged selector, fresh auth and CSRF coverage.
SQL contract tests verify atomic locking and hardcoded ceiling; real SQL
integration is required for activation, and is reported blocked if unavailable.
Use /tmp/ama-rpi-heavy.lock with timeout 0; never cloud-build around a local
Docker blocker.

P03-T02: Independent reviewer reads plan, changes, diff and tests, writes one
dated Review, leaves human gates open. Preserve adverse outcomes. Commit
candidate with privacy-safe identity and supplied trailer. Execute changed-path
gate on exact clean candidate, verify external receipt against fetched main.
Publish only when applicable gate passes; no force push, merge or closing words.

## Current Implementation Amendment

P02-T01 uses gpt-4.1-mini 2025-04-14, deployment resident-mini, Standard
capacity 1 in swedencentral after ARM rejected nano Standard. The full request
bound costs USD0.004460544 at the retrieved mini regional tariff, covered by
the unchanged USD0.01 reservation. No GlobalStandard substitution.
