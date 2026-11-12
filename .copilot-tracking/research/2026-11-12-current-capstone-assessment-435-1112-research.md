---
title: Issue 435 current capstone deck assessment research
ms.date: 2026-11-12
task_id: current-capstone-assessment-435-1112
---

## Scope and disposition

Research disposition: `executed`. Planning Readiness: `Ready`. Refs #435 only (C5 and C6 partial progress).
Pinned freshly fetched `origin/main` `cd81888e4a81cf4c712d50b357ca900fd5c8c06b`; worktree `issue-435-current-assessment-1112`, branch `docs/current-capstone-assessment-435-1112`, clean at start. The primary checkout is dirty and stale and was not touched.

## Authority and history read

* Issue #435 (open): body plus two comments. 2026-10-27 comment: PR 438 delivered a package; every criterion needs the owner or mentor. 2026-10-31 closure audit: criteria 1-6 unmet; criterion 5 (complete judgement-by-judgement challenge of a rebuilt deck) and criterion 6 (complete delivered-deck and notes statement audit) are missing; only merged, reviewed evidence justifies a tick.
* The issue prose is stale: it cites a 24-slide deck `zava-forward-executive-draft.pptx`, a 795-second 15-minute route and slide 16. The current delivered deck is `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx` (55 slides, 24:30 narration plan in a 30-minute slot, per `docs/capstone/README.md` and `source/validation.json`). The brief `tokenomics-pitch-brief.md` is now under `docs/capstone/history/`.
* Spent history, preserved and not renewed: PR 875 (merged, placement draft, one Review "conformant as draft slice, criteria 1-6 unmet"); PR 1060 (closed unmerged 2026-11-04, slide and Q&A card draft); `.copilot-tracking/*/2026-11-03-issue-435-tokenomics-*`. The deck notes on page 22 record "prior adverse finding preserved" for the owner-requested labelled scenario.
* Repository instructions, `docs/capstone/README.md`, `docs/capstone/pitch/README.md`, `docs/reference/method/ama-capstone-assessment-guide.md` (read in full), `docs/reference/resources/ai-tokenomics.md`, `docs/capstone/history/tokenomics-pitch-brief.md`, `docs/capstone/history/cowork-main-presentation/evidence/{ai-cost-evidence.md,sources.json}`.

## Equivalent-assessment check

No equivalent exists. Existing coverage is summary-level and not the requested artifact:

* `docs/capstone/source/review-2026-11-08.md` "Complete Capstone Criterion Challenge" (one line per criterion, no slide-and-notes citation, explicitly "qualitative scope review", no Tokenomics statement audit, predates slide 13 insertion).
* `docs/capstone/source/review-2026-11-08-cxo.md` "Complete Assessment-Guide Review" (grouped criteria, a preparation assessment; no statement-by-statement audit).
* `tokenomics-placement-draft.md` (2026-11-03) describes a 54-slide deck and old page numbers (S18 is now page 22, B25 page 53).

Open branches and PRs for #435: none other than those above.

## Actual artifact identity (all verified at the pinned commit)

| Item | Identity |
| --- | --- |
| Delivered PPTX | `docs/capstone/deck/zava-forward-cowork-v2-draft.pptx`, git blob `3da73fd2dd480fbbde48326174a834a27e8e87e2`, SHA-256 `949e2077...7fca`; equals `validation.json` `candidate_sha256` and the hash in the generated speaker script |
| Delivered PDF | `...draft.pdf`, blob `5bd67ab6b145fd50beca57060b0e3b9ee192c840`, SHA-256 `e1476330...0504`; equals `validation.json` `linux_preview.pdf_sha256`; 55 pages |
| Source manifest | `docs/capstone/source/slides.json`, blob `20ac61d5908ae6c74758141d28cebf7b3c4a947f`, SHA-256 `70587549...00cd`; equals `package.manifest_sha256` |
| Native baseline | `source/baseline.pptx`, blob `a2a9c528fd77ee5b7d18d8bea169f37428ee1dd4`, SHA-256 `2bab9b79...d5f8`; equals recorded `baseline_sha256` |
| Builder | `tools/capstone/Invoke-Capstone.ps1`, SHA-256 `99ac3da7...4cd4`; equals `builder_sha256` |
| Generated notes | `pitch/speaker-script.md` blob `be548021c57900bbb3c7058ee4617f439c1022cb`; `pitch/questions-and-answers.md` blob `09dca60c49ec67d2f7891710eaeb55fdb040ff14`; SHA-256 values equal `validation.json` `pitch.*_sha256` |
| Validation receipt | `source/validation.json`, blob `264482186ea8741cc5ce235fcc0bebde4b91b170` |

Source and delivered deck agree on identity through the receipt hashes. The manifest alone is not the delivered text: 55 of 55 manifest notes differ from the delivered notes because the builder rewrites page references after the added slide 13 and applies the owner-approved 2026-11-08 cost status-only edits (`cost_status_revision`), for example page 22 and 53 control wording and `CURRENT ROUTE TIMING` lines; the delivered text lives in the builder plus manifest. Generated notes match delivered notes for every slide checked (sentence-level match: 54 of 55; page 28 is the question index and is not in the generated notes).

## Method and limits

* The `powerpoint` skill was loaded first. Its extraction scripts need `python-pptx` and `uv`, which are not installed; no installation was made. The PPTX was read read-only with Python standard-library zip and XML parsing in presentation order, giving slide text and speaker notes for all 55 slides (`/tmp` working copy, not committed). That is content-only evidence.
* The committed PDF text of page 22 was read with `pdftotext` and matches the PPTX text.
* No rendering, visual inspection, native PowerPoint, projector, accessibility or audience check was performed here. The Linux preview images are stored outside the checkout; `validation.json` records them (renderer LibreOffice 24.2.7.2, `human_acceptance: false`, `native_powerpoint_validation: false`, `rehearsal_performed: false`). Visual and craft judgements therefore rest on content extraction plus those recorded results and are labelled so.

## Tokenomics statement findings

Statements reside in visible text and notes of pages 6, 10, 22, 33, 35, 39, 44, 45, 49, 50, 53, 54, 55 (and cross references on 5, 21, 28, 37, 48). The central facts:

* Method: unit is total attributable cost divided by human-accepted proposals above a quality floor (pages 22, 53 notes). Not measured.
* Observation: 6,884 tokens across five operator runs, mean 1,376.8; no human acceptance (pages 10, 22, 39, 53). Source `ai-tokenomics.md` and E19.
* Assumptions: 10x task size and 20 tasks per home (pages 6, 22, 53); 15,600-home cohort is modelled (60,000 x 26%).
* Price: USD 1.60 per million tokens, a secondary-source "reported GPT-4.1 mini output rate" dated 2026-10-23 (`ai-cost-evidence.md`). The 2026-10-31 official pricing retrieval recorded unavailable numerical rates, and `ai-tokenomics.md` 2026-11-07 records the configured demo deployment as `gpt-4.1-nano` (history `gpt-4.1-mini-2025-04-14` for the five runs). The deck prices the mini rate without verifying the deployed model, region or currency.
* Derived figures shown to the audience: USD 0.44 per home, USD 6,873 across 15,600 homes, USD 0.88 doubled (pages 6, 22, 53). Labelled "planning scenario", "assumed workload", "not current verified price", but still a price-derived figure. Criterion 6 of the issue (no price claim) and the brief's "Claims to Keep Out" are in tension with it; the placement draft flagged this on 2026-11-03 and no owner decision is recorded.
* Missing: billing, applicable price, denominator (OD-51), quality floor, accepted-outcome count, full TCA ("P" unpriced, page 33), measured savings or payback. Page 22 and 53 state accepted-outcome cost unknown and no saving or payback established.
* Controls wording differs across pages: page 44 visible "hard stops are designed" versus page 55 notes "no longer merely a proposed hard-stop design ... source-coded"; page 22 visible lists money budgets under "HELD". Source basis `src/core/README.md` AI consumption ledger (not re-run here).
* Visible slides expose internal tracker labels (`#435 not accepted`, E-codes) on pages 22 and 53.
* Page 28 notes still say "All 54 page numbers"; page 22 original `TIMING` lines use the 23:45 clock while `CURRENT ROUTE TIMING` carries the operative 24:30 windows (documented retained provenance).

## Unknown, not invented

Mentor meaning of Tokenomics; owner placement decision; spend authority; any actual participant, rehearsal timing or approval; actual assessor score; masterclass attendance and artifact submission (floor prerequisites).

## Constraints carried into the plan

* Documentation only, one assessment file in `docs/capstone/pitch/`, plus a pitch README link and a knowledge-base log entry. No deck, source, placement, builder, PPTX, PDF, source-code, issue or settings change; no model, cloud, private-dataset call.
* Judgement-by-judgement coverage of A1-A7, B1-B7, C1-C3, D1-D3 and the floors and overlap rules, with per-criterion evidence, gaps and assumptions; no numeric score.
* Statement-by-statement Tokenomics register with source, evidence label and classification.
* Findings are routed to later owner decisions, not applied; C5 and C6 remain partial.
* Local validation: focused documentation review, link check and diff only. No uv; no installation.
