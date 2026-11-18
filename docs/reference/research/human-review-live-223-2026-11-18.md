---
title: Human-review effectiveness test, demo evidence (#223)
description: What the synthetic demo proves about seeded-defect detection, reviewer retention, effort reporting and automation bias, and what needs real reviewers
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only, owner decisions of 2026-11-18. Evidence folder:
[human-review-live-223-2026-11-18/](./human-review-live-223-2026-11-18/). No source, infrastructure or Azure resource was changed; nothing needed deleting.

## Evidence gathered

* Offline harness `python3 -m zava_forward.agents.review_effectiveness --json` run from the worktree sources (`PYTHONPATH=src:../core/src` in `src/agents`): [harness-report.json](./human-review-live-223-2026-11-18/harness-report.json), `passed: true`, all 11 checks true.
* Targeted tests: `src/agents` `tests.test_review_effectiveness` 37 tests OK ([test-agents.txt](./human-review-live-223-2026-11-18/test-agents.txt)); `src/core` `tests.test_human_review_effectiveness_223` 6 tests OK ([test-core.txt](./human-review-live-223-2026-11-18/test-core.txt)); `python3 -m mypy` in `src/agents` clean (67 files); `ruff format --isolated --line-length 100 --check` clean.
* Live probe on `ca-cutover-test-demo-api` with Playwright sign-in as a Retrofit Programme Manager (credentials read at runtime, not printed): [scripts/live_probe.py](./human-review-live-223-2026-11-18/scripts/live_probe.py), [live-probe.json](./human-review-live-223-2026-11-18/live-probe.json), [screens/01-signed-in.png](./human-review-live-223-2026-11-18/screens/01-signed-in.png).
* The live AI summary on case ZF-2025-0331 returned a template draft (`source: template`, `model: null`): release admission was denied because no approved release exists and the RAI task owner is not appointed (OQ-017). Label "Not reviewed", "Not an instruction".
* A reject with an empty reason returned 400 "Say why." A reject with a reason was stored with `reviewer_action`, `reviewer_reason`, `resolved_by`, `resolved_at`, case version and source versions. This created one rejected review record on the synthetic demo case.
* An early probe attempt used a request context without the `X-ZF-CSRF` header and got an empty 403; the final probe posts from the page with the header, as the SPA does.

## Harness results (scripted panels, same case, same six reviews)

| Panel | Defects detected | Corrections | Gate | Effort units | Workflow-only units |
| --- | --- | --- | --- | --- | --- |
| Competent | 4 of 4 | 3 edits, 1 rejection | pass | 23 | 24 |
| Default accept | 0 of 4 | 0 | fail | 6 | 24 |
| Automation bias | 0 of 4 | 0 | fail | 9 | 24 |
| Unauthorised competent reviewer | n/a | n/a | fail ("no defined authority") | 23 | 24 |

## Per-criterion table

| Criterion (all unticked in #223) | Demo result | Basis |
| --- | --- | --- |
| Seeded critical defects detected and prevented from satisfying a controlled gate | Proven for the offline harness only (wrong, stale, unsupported, incomplete; each missed class fails the gate in sensitivity runs). Unproven on the live demo and with people | Live demo cannot seed defects: live AI is denied by release admission, so only template output exists |
| Reviewer, source and reason retained | Proven live (reject record keeps reviewer, reason, source versions; empty reason refused) and in harness rows (`reviewer`, `source_hashes`, `reason`, audit chain verified) | live-probe.json, harness-report.json |
| Detection, corrections and effort reported against the same workflow-only scenarios | Proven for scripted effort units (comparison block). Unproven for measured reviewer time | `effort_note`: scripted units, not time |
| Default acceptance and citation validity alone cannot pass | Proven in harness (all proposals carry valid citations; default-accept and automation-bias panels fail) | checks `default_acceptance_cannot_pass`, `citation_validity_alone_cannot_pass` |
| Automation-bias test included; reviewer authority and evidence defined (OQ-017) | Test included and proven with a scripted panel. Authority and evidence are defined only as provisional (reviewer, source_hashes, source_reason); OQ-017 owner decision stays open | `evidence.reviewer_authority.status` |

## What the demo cannot prove

* Competence of real reviewers, real automation-bias rates and measured review time: scripted panels are not people. Needs authorised reviewers from the OQ-017 decision and the existing worksheet and pooling tools (`worksheet`, `score_human_session`, `pool_human_sessions`).
* Approved thresholds, sample sizes and reviewer authority (OQ-017, Sponsor, Programme, Safety, DPO/Legal and Assurance). The owner waived DPO/Legal for the demo, so this stays a recorded open item rather than a demo blocker.
* Defect detection on live model output: needs an approved live release, which does not exist.

## Follow-ups

* Appoint OQ-017 reviewers and run one measured human session with the worksheet.
* Appoint the RAI task owner and approve a release so live AI output can be reviewed against seeded defects.
