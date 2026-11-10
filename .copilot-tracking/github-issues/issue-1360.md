---
title: Generic importer transfer outcome can claim nothing was recorded after an SQL commit
description: Non-blocking follow-up from the independent Functional review of parent #73 head af7b20a3
ms.date: 2026-11-10
ms.topic: reference
---

## Created Issue

* Issue: #1360, https://github.com/jmservera/ama/issues/1360
* Created: 2026-11-10, filed by the coordinator under owner decision D5.
* Template: generic; no assignee, label or type.
* Parent context: #135 (child of #73). Refs #73, #135.

## Summary

The Importer transfer handler at `src/importer/src/zava_forward/importer/__main__.py` lines 160-161 prints "Nothing was recorded" for any OSError or ValueError. `SqlStore.save` commits before its final refresh and converts only RuntimeError into `CommittedReloadError`, so an OSError or ValueError raised during the post-commit refresh could reach the generic handler although the refusal was saved.

## Evidence and status

* Source: independent Functional review b8c5a215-e1dd-484c-aed5-60e02cadc5ac, finding 1, Medium, non-blocking, head af7b20a37eb08ce71b9c480fe6d8de1d452918f4.
* Static concern only; not reproduced. No loss of idempotency identified.
* Suggested direction from the review: report generic outcomes as unconfirmed with the idempotent retry, or distinguish a committed outcome, and add a regression through the real `SqlStore.save` with a post-commit OSError.

## Boundaries

* Not fixed here. Source 135 C5/5 has zero left and this issue grants no fresh repair allowance or budget. Any work needs a new owner-approved scope.
