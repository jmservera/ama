---
title: Issue 119 details
description: Phase details
ms.date: 2026-11-17
---

## P1

Record sections: Status (Proposed; no provider selected), Decision (demo: OSM standard tiles under the owner's scoped approval; production: none, empty `ZF_TILE_URL` loads no tiles), Decision gate (owner, DPO, procurement, legal; finite costed plan under the USD 700 October ceiling), Criteria for choosing, Accessible alternative requirement (FR-020, AC-023, AC-067; the map is never the only route; list `details.maplist`), Evidence of test status (automated only), Unmet items. Plain ASCII, no keys.

## P3

Test: file exists; links resolve; states no provider selected; no key-like URL query; cited test modules exist; code facts: production `tile_config` has no OSM fallback and app.js carries the list alternative text; REQ ids cited exist in PRD.
