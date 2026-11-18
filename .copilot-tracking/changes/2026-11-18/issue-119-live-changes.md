---
title: Issue 119 live closure changes
ms.date: 2026-11-18
---

## Changes

* Added docs/reference/research/issue-119-live-r4-map-evidence-2026-11-18.md.
* Updated docs/reference/README.md (index) and docs/reference/log.md (entry).
* Added evidence folder .copilot-tracking/evidence/2026-11-18/issue-119-live/ (refreshed probe JSON, probe scripts, map screenshot, OSM policy text); named screenshots removed.
* No source change; FOCUSED tier. Azure: two read-only `az containerapp show`; nothing created, nothing to delete.

Note: the research note and evidence were authored before this file existed (the opening research artifact preceded them); the witness implement-start call follows this file, with no src edit.

## Per-criterion table

| Criterion | Proven for demo | Unproven / production-only |
| --- | --- | --- |
| Provider licence, cost, coverage and processor terms recorded | Yes for the demo provider (OSMF tiles: ODbL, no charge best-effort no SLA, global coverage, no processor terms; live probe) | No licensed provider selected, priced or contracted; OS plan prices, Azure Maps paid rate, MapTiler commercial terms, DPA unread. Do not tick |
| Screen reader test of the list alternative | No (automated proxies only: landmark, status, labelled list, keyboard, tiles-blocked fallback) | No screen reader run (not needed for demo per owner); production protocol remains. Do not tick |

## Validation

Documentation link and diff review, credential literal scan of the evidence folder, `git diff --check`. Unit tests, mypy and ruff not applicable (no Python source change); hosted CI is read by the coordinator after publication and was not observed here.
