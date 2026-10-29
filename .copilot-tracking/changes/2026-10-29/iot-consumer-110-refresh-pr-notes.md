---
title: PR 508 refresh notes for coordinator
description: Local PR-body addendum, not yet published
ms.date: 2026-10-29
---

## Current-main refresh

Refs #110 #184 #185 #187 #188 #189.

Rebased feat/iot-consumer-110 onto b0364e4b326936715d69ab1d75040c4528282af7.
Resolved only knowledge-base index/log conflicts, preserving both main's
new entries and the original IoT entries. Main's .github/rubric tree and
scenario manifest remain byte-identical; all four pinned source hashes match.
Topic source and prior 2026-10-27 RPI evidence are preserved.

## Local validation

Using /tmp/mv with this worktree's installed editable core/agents/API
distributions and declared SDK pins:

* Core Ruff lint/format and mypy pass: 106 formatted, 159 checked files.
* API Ruff lint/format and mypy pass: 58 formatted, 109 checked files.
* Focused core replay/consumer/stock/fault/privacy/backfill/manifest/inventory:
  121 tests pass, including one existing opt-in SQL skip.
* API IoT stream/ingestion: 66 tests pass.
* Full API discovery: 1295 tests in 464.666s, pass, 316 skips, under held
  nonblocking shared heavy lock. Skips are not live SQL/browser acceptance.
* pip check, main ancestry, original-evidence byte comparison and source-pin
  verification pass. Existing backfill ResourceWarnings are retained.

Full local publication receipt and independent exact-head assessment remain
separate gates. The complete runner invokes az bicep version/build/lint;
this task permits az only for read-only cost lookups, so no complete runner
execution or receipt is claimed here. Coordinator must complete the gate in
an authorized context, fetch main, verify the external receipt and obtain the
independent exact-head assessment before publication.

## Estimated smallest paid IoT Hub cost

Official Azure Retail Prices API, retrieved 2026-10-29, USD consumption meters
for UK South: Basic B1, one unit, is the smallest paid Hub SKU at an estimated
**USD 10.00/month** (meter "B1 Unit", unit "1/Month"). This is Hub-only retail,
not an approved purchase, bill, subscription-specific quote or complete
solution estimate. Tax, networking/private endpoints, Event Hubs routing,
monitoring, storage and other resources are excluded. No Hub was created.

Source:
https://prices.azure.com/api/retail/prices?%24filter=serviceName%20eq%20%27IoT%20Hub%27%20and%20armRegionName%20eq%20%27uksouth%27%20and%20priceType%20eq%20%27Consumption%27&currencyCode=USD

## Review and publication boundary

Original independent implementation Review for this refresh:
**Complete / Conformant with justified divergence**. No source defects.
RV-001 and RV-002 retain the complete-publication and fresh-hosted-result
gaps as coordinator-owned follow-ups. This is the single original Review,
not the later independent exact-head publication assessment. Dated Research,
Plan, details, critique, changes and state use the stable slug
iot-consumer-110-refresh under .copilot-tracking/ and date 2026-10-29.
Earlier adverse and later bounded correction outcomes are not rewritten.

This task makes no push or remote PR edit. Coordinator owns publication of
the rebased history and fresh hosted checks. Historical rubric scoring
produced no verdict, and its attempted comment failed HTTP 403; local
source checks cannot establish the next hosted verdict. No permissions,
rubric policy or protection settings were changed.

Existing actual Hub/credential lifecycle/SQL/model/budget and OD-43 gates
remain unproven. No issue criterion or operational approval is newly granted.
