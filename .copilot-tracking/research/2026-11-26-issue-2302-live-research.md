---
title: Research issue 2302 live, AI consumption economics in the management view
ms.date: 2026-11-26
---

## Status

Research disposition: executed. Planning Readiness: Ready.

The canonical findings, live proof and test runs are in [the research note](../../docs/reference/research/issue-2302-live-20261126T232328Z.md). Summary: the Overview route renders `aiEconomicsCard` (`app.js`) from `/api/stats`; six denominators and six cost rows are shown; on the demo every cost renders Unknown with 5 proposals, 0 accepted outcomes and 231 metered calls. Existing core (6) and API (9) tests prove Unknown-not-zero. No source change is needed.
