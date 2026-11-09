---
title: Visible-demo integration checkpoint 440 phase details
ms.date: 2026-11-08
---

## Phase 1 details: pack section

Heading: `## Visible-demo integration checkpoint (2026-11-08, Refs #440 #149 #229 #891)` appended at the end of the pack.

* Identities table: base `6354b13f`, tree `0fddb514`, newly fetched main, PR 1286 `28c6ec11`, PR 1290 `656cafb1`, 6354 only changes `.github/rubric/scores/latest.json`; BRD, PRD, ADR blobs and status; addendum blob; original blob.
* Source movement since 608c: two production modules changed, `chat_eval.py` (component-scope disclosure) and `doc_controls.py` (refusal wording); test, check and README files under `src/` also changed (state this). Audited chat, assistant and admission modules unchanged (actual Git diff).
* AI-invocation table for the visible demo: the five registered assistants through `Assistants.execute`; employee chat `ChatPanel._ask` behind `chat_admission` and the demo-only `ZF_CHAT_DEMO_ACTIVATION` plus `ZF_DEPLOYMENT_PROFILE=demo` switch; rules-only unstored path and workflow-only fallback; UI label selection in `chat.js`; authority ceiling.
* Evidence table by class with date and source.
* Exclusions: unmerged #184 and #1288 candidate work is excluded from main and deployed acceptance; do not assert their source or activation state, which was not verified here; parent #81 (PR 1240) open; resident, IoT and sensor-grounded Quality not accepted.
* Findings: none newly confirmed; F1 stays unowned; F2 qualified by #1284 disclosure, mismatch remains. Ordering defect link omitted (unverified).
* Recommendation and resume conditions with existing owners.

## Phase 2 details

* README: one paragraph after the last checkpoint paragraph linking the new anchor.
* Log: append `## [2026-11-08] update | Issue 440 visible-demo integration checkpoint (Refs #440, #149, #229, #891)`; no earlier line changes.

## Phase 3 details

Commands: `git diff --check`; Python ASCII and anchor check on added lines; `git diff origin/main -- docs/reference/log.md` prefix check (earlier bytes identical to `HEAD:docs/reference/log.md`); `git status --short` and `git diff --name-only HEAD` scope guard (allowlist includes untracked files); `git fetch origin main`.

## Phase 4 details

Changes record lists exact commands and exits; Review is one original author review; state JSON per the RPI contract.
