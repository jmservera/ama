---
title: Issue 100 live details
ms.date: 2026-11-19
---

# Phase details

* Helper returns `{denominators: [[label, count]], costs: [[label, text]]}`. Counts are real integers (0 is a valid denominator). Cost fields render `Unknown` for null, undefined, empty, `Unknown` or numeric 0; a priced value renders with the currency.
* Missing `ai_consumption_economics` renders every cost Unknown and a notice, never a blank card.
* Markup: `section.card` with `h2`, `dl` for denominators, a table with caption for costs, and the non-benefit notice as plain text. No colour-only status, no new motion.
* Web guidelines fetched 2026-11-19: semantic table with caption and `scope`, `Intl.NumberFormat`, empty-state handled.
