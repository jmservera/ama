<!-- markdownlint-disable-file -->
---
title: Issue 349 image-scan correction 1 plan
description: Test the stale-cache hypothesis; change source only if disproved
ms.date: 2026-10-26
---

Research: ../../research/2026-10-26/issue349-image-scan-correction1-research.md
Details: ../../details/2026-10-26/issue349-image-scan-correction1-phase-details.md

* [x] Phase 1: Research (retained evidence, source and runner read).
* [x] Phase 2: Critique executed once before any build: Revise (2 blocking). Applied: representatives of both final-stage RUN variants (api, standing for orchestrator, and importer, standing for agents) are rebuilt and scanned; a follow-up plain build verifies the next gate would not reuse a stale layer; apt-cache policy and installed versions recorded to separate mirror lag from cache; no Docker prune is performed here, any prune is left to the coordinator with exclusivity. No repeat critique.
* [x] Phase 3: Probe heavy lock once; one fresh api build with --no-cache and exact configured scan, output under /mnt/ama-rpi-gates/issue349-image-correction1.
* [x] Phase 4 (review below): Decide: confirmed means no Dockerfile change and a cache-refresh recommendation; disproved means smallest Dockerfile fix in the shared pattern. Focused image tests, independent review, commit artifacts.

Constraints: no ignore/baseline/threshold/scanner change; no full gate; no push; preserve all old outputs and receipts; one correction cycle only.

Outcome: hypothesis confirmed for all four images; no Dockerfile or runner change was needed (see changes record).
