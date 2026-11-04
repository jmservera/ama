---
title: Issue 151 focus not obscured research
ms.date: 2026-11-04
---

## Prior delivery

Merged: #244, #427, #857 (target size), #1000 (error identification). Ticked criteria: automated CI checks, statement draft.

## Findings

* WCAG 2.4.11 and 2.5.7 had no audit row. The fixed chat launcher/widget (chat-widget.css, 2 fixed rules) can cover a focused control; html had no scroll padding.
* No script binds drag or touch handlers; the map has a list alternative.
* Planning Readiness: Ready. Slice is static CSS plus tests; no security, infrastructure, SQL or deployment change (focused tier).

## Unmet criteria after this slice

Target level decision (owner O-1); full audit (rendered overlap, reflow, zoom, screen-reader status messages); manual screen-reader and keyboard checks per role; human check of map, chart and table equivalents (#119).
