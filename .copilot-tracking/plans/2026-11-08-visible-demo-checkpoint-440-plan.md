---
title: Visible-demo integration checkpoint 440 plan
ms.date: 2026-11-08
---

## Objective

Add one concise dated section to the existing `docs/architecture/cutover-evidence-pack.md`, one index paragraph in `docs/reference/README.md` and one appended entry in `docs/reference/log.md`. Docs only. Research: [research](../research/2026-11-08-visible-demo-checkpoint-440-research.md). Details: [details](../details/2026-11-08-visible-demo-checkpoint-440-details.md).

## Phases

* [x] Phase 1: write the pack section after the existing last section, with these subsections: identities and covered changes; where AI is invoked and the authority ceiling for the visible demo; evidence table by classification; traceability; sensor and unmerged exclusions; findings, owners and gates; recommendation.
* [x] Phase 2: add one index paragraph and one appended log entry, leaving every earlier log line byte-identical.
* [x] Phase 3: focused validation: `git diff --check`, frontmatter, ASCII and em-dash check on added lines, relative links and anchors, protected prefix check of the log and of the pack, scope guard (three docs files plus `.copilot-tracking`), final `git fetch` and diff of `origin/main` against the pin.
* [x] Phase 4: changes record, one original author Review against the #440 acceptance criteria, state, commit.

## Decisions

* Section is concise. It cites existing prior sections instead of restating architecture, and copies no raw gate archives, identities, tokens or account values.
* Historical evidence is source and date qualified, never fresh acceptance. 891 model observation is one generic synthetic answer.
* The #81 recommendation-ordering link is omitted because it was not verified (research). No issue is created.
* No ticks, closures, issue or board writes, pushes, PRs, rebase, force. No test suite, SQL, browser or model call.
* If `origin/main` moves beyond the pin before commit, compare with actual Git, record the move and any source diff; do not assume equivalence and do not rebase.

## Acceptance for this task

* Pinned base, tree, newly fetched main, covered PRs, document blobs and status recorded.
* Five agent responsibilities and ceilings visible; WHERE AI is invoked, what deterministic services do.
* Classification of every evidence item; adverse qualifications preserved; no claim of five-agent, sensor-grounded, current-main-deployment, cost/privacy acceptance or approval.
* Continue recommendation with owners and resume conditions using existing issues; explicit statement that no new defect was confirmed.
* Existing records unchanged except the intended new appended text.

## Validation tier

CI-first focused documentation only. Existing applicable documentation checks: none repository-wide (repository guidance); Markdown, link and Git diff review.
