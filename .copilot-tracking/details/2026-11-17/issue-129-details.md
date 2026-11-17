---
title: Issue 129 plan details (2026-11-17)
description: Phase details
ms.date: 2026-11-17
---

## P01

Test reads the doc by path relative to the test file (repo root is four parents up from `src/core/tests`). Table rows split on `|`; atlas IDs split on ", ". Requirements are cell 3 split on ", ". Target-zero measures are checked by presence of each measure's words in the per-bundle table is brittle, so only the stop rule, comparator, IDs, title and requirements are compared.

## Critique

Single pass, self-critique: brittleness limited to the first table; no new dependency; no source change. Disposition: accepted.
