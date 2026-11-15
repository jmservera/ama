---
title: Issue 432 Criterion 6 plan critique
ms.date: 2026-11-13
---

Executed by rubber-duck before code. Verdict: Revise. Dispositions (applied directly):

* Failure semantics: ledger outcome for revoked chat is `returned`; provider failure has tokens None and held True. Applied via parameterised assertions.
* Retries: real worker second attempt is costly; retry join proven at ledger level (core test, retry 0 and 1, report retries and failures) and worker retry value asserted where available. Partially applied.
* Failures: report failure delta asserted per chat mode. Applied.
* Join strength: exactly one reservation, completion and output per call. Applied.
* Privacy: canaries scanned across all records for chat; worker canary scan already existed. Applied.
