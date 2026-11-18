---
title: Issue 117 live plan
description: Plan to prove or bound the criterion "Uploads are scanned before availability" on the demo
ms.date: 2026-11-18
---

## Plan

Tier FOCUSED, docs and evidence only, no source change. Refs #117.

* [x] Phase 1: Run one signed-in Playwright script against `ca-cutover-test-demo-api`, reading credentials at runtime, that: reads `/api/me` role (reduced), `/api/retention`; uploads (a) the synthetic malware test marker as a `.txt`, (b) a `.pdf` whose bytes are not a PDF; expects both refused; re-reads the case documents to show neither was recorded. No clean file is uploaded, so no demo record or blob remains.
* [x] Phase 2: Retain raw redacted output under `docs/reference/research/issue-117-raw/`.
* [x] Phase 3: Write research note `docs/reference/research/issue-117-live-scan-evidence-2026-11-18.md` with a per-criterion table; update index and log.
* [x] Phase 4: Commit; run link and diff review.

## Critique (executed once)

Full critique: `.copilot-tracking/critiques/2026-11-18-issue-117-live-critique.md`.

Verdict: compatible. Risk: an upload could leave a blob if the delete failed; mitigate by listing documents after and reporting any residue. A clean-file upload is excluded to avoid leaving demo state. Live Defender scanning cannot be proven: it is disabled and enabling is a production-grade change excluded by the brief. Applied directly.
