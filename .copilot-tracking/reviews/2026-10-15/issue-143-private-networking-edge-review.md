---
title: Issue 143 review
date: 2026-10-15
---

## Review (single pass)

Execution: done. Outcome: conformant with open items.

| Criterion | Result |
| --- | --- |
| PE and DNS coverage listed and checked | Met (README table, test) |
| Front Door Premium, WAF, Private Link origin | Met (defined, optional; not deployed) |
| Custom domain, TLS, Entra callbacks | Met in code (managed cert, `entraRedirectUri`, forward proxy); DNS steps are owner actions |
| Dev public access blocked in production | Met (existing guard plus edge guards) |
| Evidence from production deployment | Open: no deployment was run |

## Routed follow-ups

* Deploy the production profile with `enablePublicEdge=true`, approve the private endpoint connection and record evidence.
* Owner: custom domain, DNS and pilot edge go/no-go; confirm Private Link support and pricing in uksouth.
