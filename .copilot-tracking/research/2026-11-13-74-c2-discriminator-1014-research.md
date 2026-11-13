---
title: Issue 74 criterion 2 populated-building discriminator research
description: Research for one external-runner probe of home_case_view with populated building rows and two homes with distinct values
ms.date: 2026-11-13
---

## Scope

Continuation of commit 2c2c5821 (original files preserved unchanged, including pre-critique test run, author-only OK, tail-exit limitation and the original missing-review-file finding). Source-correction history: UNKNOWN; no grant or renewal. Not repeated: own-home negative controls, the three prior tests, null-funding.

## Recovered facts

* `building_fixture.fixture()` gives ZF-2 and ZF-3 SYN-B1 with identical decision and allocation, empty dependencies and holds, one work and one cost; `hold()` helper provides a valid hold row.
* `home_case.view` (home_case.py:119) returns `building` from `buildings.view` (homes removed) and `home` with decision, stage, closed, funding_confirmed, documents, quality, cost_allocation.
* Building rows validated by `buildings.record` (dependencies/holds/works need id, label, status, owner, source, case_ids, package_ids).

## Probe design

External runner in /tmp, in-memory Store and SqlStore on temp folders. Populate one dependency, one hold, existing work and cost; set ZF-2 and ZF-3 to different decision status, allocation amount, funding, documents and stage. Assert per home own values, building rows identical for both homes and containing none of the home values, and that swapping values would fail. Outcome adequacy (stage, closed, quality) is not decided.
