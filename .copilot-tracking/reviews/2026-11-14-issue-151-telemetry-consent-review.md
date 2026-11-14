---
title: Issue 151 telemetry consent review
ms.date: 2026-11-14
---

## Review

Execution: executed once (self-review, not independent). Outcome: conformant for the core slice; open work routed below.

## Acceptance criteria

* Withdrawal stops collection and flags downstream views: proven by unit tests.
* Refusal or withdrawal does not block repairs or safety: structurally proven (no case writes, test asserts cases unchanged); statutory workflow integration untested.
* Plain-language notice: text drafted, not yet surfaced to residents or approved.

## Follow-ups

1. Wire notice and withdrawal into the API and resident UI (web guidelines apply).
2. Resident-engagement and legal review of the notice wording and reading level.
3. Independent exact-head review, hosted CI; use `Refs #151`, not `Closes`.
