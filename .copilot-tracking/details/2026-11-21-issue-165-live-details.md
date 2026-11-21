---
title: Issue 165 recheck phase details, 2026-11-21
---

## Phase 1

Run `PYTHONPATH=src:tests python3 -m unittest -q` for the needs, manifest, determinism, provenance, audit, traceability and sensor modules in src/core. Success: OK.

## Phase 2

`az containerapp job execution list`, hub `d2c.telemetry` metrics, and a Playwright sign-in reading `/api/cases/{id}/sensors` for one granted, one declined and one uncontrolled home. Mutations: none. Secrets: read at runtime, never printed.

## Phase 3

Note docs/reference/research/issue-165-live-20261121-2026-11-21.md, index row in docs/reference/README.md, log entry.

## Phase 4

Changes record, review, commit with Refs #165 and required trailers.
