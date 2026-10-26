<!-- markdownlint-disable-file -->
---
title: Issue 349 main c8d16059 integration research
description: Prospective read-only research before merging current main
ms.date: 2026-10-26
---

## Facts (git and gh, read-only)

* Local was b765120a, clean. Draft PR #437 open, remote head e95c0f51, a normal
  fast-forward of b765120a (is-ancestor true).
* The remote delta is bot-only: .github/rubric/scores/latest.json (6 lines
  changed), score 73 recorded for commit b765120a. Adopt by --ff-only.
* origin/main is c8d16059, one commit (#455, resident read-only feedback preview,
  refs #444) ahead of the merge base. 53 files: src/api resident_preview, src/core
  resident_preview, READMEs, docs, docs/reference/log.md and the generated
  rubric score latest.json.
* Overlap: latest.json changed on both sides (main score for a3ce5984; our bot
  score for b765120a), so a content conflict is expected. log.md changed on main
  only since our last merge, so it should auto-merge with both append-only
  intents kept.
* No main change touches the tenant preflight, its test, the app-registration
  manifest or the auth role maps, so the 13-role contract test needs no change.

## Boundaries

Local only; no heavy gate, install, browser, Docker, live or cloud action. Owner-reported
login and Entra-authoritative roles are context, not re-verified. Historical
2026-10-24 diagnosis stays dated.

## Planning readiness

Ready: ff-only the bot update, then normal merge of c8d16059; on the rubric
conflict keep main's baseline; stop on any other conflict.
