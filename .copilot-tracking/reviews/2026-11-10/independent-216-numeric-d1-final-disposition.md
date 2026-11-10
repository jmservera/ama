---
title: Record - final independent source disposition of the numeric correction (Refs #216, #208)
description: Faithful record of the independent static review of the numeric delta at 46dfa754
ms.date: 2026-11-10
---

## Source of the record

Session files under `independent-216-paired-report-1110/numeric-d1-final/`: `functional-findings.json` sha256 `470a42896e3a959d46e1699f4b7b90ee3a9e27b9e2293ffd42eca6b601663d59`, `read-ledger.json` sha256 `ca3586dfd56fb42c16384c24f1a61ddea1bbbc71f40dfdd758ce0bd513ced560`. Reviewer `6339ad63-3729-49ea-924b-b9293482c70d`. Nothing is copied or rewritten.

## Disposition as issued

* Supplied head `46dfa75490a96f49dc89eab17fe72451320553ab`, tree `e1b6f51806ad1a0ec05ded63f389dff235ed1142`, base `ab365e53d024e269c9ad4f0b0e33a8361a43e30b`. Verdict `approve`, zero findings.
* Both original Medium findings (derived elapsed ratio overflow to `Infinity`; huge negative integer `OverflowError`) are resolved. No new functional defects. The original `approve_with_comments` assessment of `ab365e53` is preserved, not erased or reclassified.
* Coverage: the complete 19-file delta, both raw seven-event witness logs, the producer red, green, targeted, mypy and strict outputs and both handoffs.

## Limits

* Static review. The reviewer executed no tests and no Git; Ruff and default-byte equality are producer claims, not independently run.
* Explicit `--record` can still overwrite an operator-selected canonical file; this stays an operational risk, not a contract defect.
* The reviewer noted the empty D2 plan and the D1 and D2 process qualifications; they are not source defects.
* This is not a D4 independent approval, a publication grant, hosted CI approval or acceptance of whole #216 or #208. Root will send the final D4 delta to the same reviewer.
