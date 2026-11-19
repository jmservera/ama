---
title: Human-review effectiveness test on the demo (issue 223)
description: Recorded 2026-11-18 run of the review-effectiveness gate and live review retention on the synthetic demo, with a per-criterion proven or unproven result
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 223
  - human review
  - automation bias
  - OQ-017
estimated_reading_time: 6
---

Refs #223. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Production-only criteria stay deferred (#1905-#1908). Nothing here is human-participant, production or resident evidence.

## Method

* Offline gate: `python3 -m zava_forward.agents.review_effectiveness --json` from `src/agents` (`PYTHONPATH=src:../core/src`). Output kept as `harness.json`. Seeded wrong, stale, unsupported and incomplete proposals with citations that resolve, plus two correct controls, go through the real `Store.ai_run` and `Store.review_ai`.
* Focused tests: `tests.test_review_effectiveness` (37 tests, OK) and `tests.test_human_review_effectiveness_223` (6 tests, OK).
* Live demo: Playwright Chromium, 1366 by 900, signed in with the employee demo account (Entra, role `Retrofit Programme Manager`) on `ca-cutover-test-demo-api`. The driver `live_review_proof.py` calls the app's own routes with in-page fetch and the `X-ZF-CSRF` header, scrubs email addresses and writes `live_review_run5.json`. Credentials were read at run time, never printed; a literal scan of every evidence file found no credential value.
* Evidence folder: `.copilot-tracking/evidence/2026-11-18/issue-223-live/`.

## Results

Offline gate (scripted panels, one case, six proposals):

| Panel | Defects detected | Corrections | Uncorrected defects | Gate |
| --- | --- | --- | --- | --- |
| Competent | 4 of 4 | 3 edits, 1 rejection | 0 | Passed |
| Default accept | 0 of 4 | 0 | 4 | Failed |
| Automation bias (accepts confident, cited output) | 0 of 4 | 0 | 4 | Failed |

Further controls in the same report all hold: an unauthorised reviewer fails, four panels that each miss exactly one defect class fail, an over-rejecting reviewer fails, and the audit chain verifies. Effort is 23 scripted comparison units for the competent panel against 24 for the workflow-only run of the same case; these are units, not measured time.

Live demo (case ZF-2025-0331, synthetic):

* A summary task with mode `workflow-only` and one with the default mode both returned `source: template`, `model: null`, `verified: true` with three resolving citations. No live model task is activated, so a model-generated defect could not be observed.
* Rejecting a proposal without a reason returned 400 "Say why."
* Rejecting with a reason naming a source returned 200, status `Rejected`, and retained `reviewer_action`, `reviewer_reason`, `resolved_by`, and `review_evidence` with `reviewer`, `disposition`, `reason`, `compared` (AI and workflow output), `source_hashes` and `case_version`.
* A second review of the same record returned 400 "This AI output has already been reviewed."

## Per-criterion result

| Criterion in #223 | Result for the demo | Evidence and limit |
| --- | --- | --- |
| Seeded critical defects are detected and prevented from satisfying a controlled gate | Proven for the scripted competent panel only | Offline gate: 4 of 4 detected, 0 uncorrected through the gate. Unproven with a competent human reviewer, and unproven on the live app, which has no seeded-defect set and no activated model task. Seeding the live store needs a source change (FULL tier) and would add synthetic records to a ledger table. |
| Reviewer, source and reason are retained | Proven for the live review path | Live record keeps reviewer, reason, source hashes and compared outputs; offline report verifies the audit chain. The source label in the reason is a free-text convention checked by the offline gate, not by the live route. Retention for a real appointed reviewer is not shown. |
| Detection, corrections and total review effort are reported against the same workflow-only scenarios | Proven as reporting mechanics, unproven as measurement | `comparison` reports detection, corrections and effort beside the workflow-only run of the same case. Effort is scripted units. The manual `--worksheet` and `--score` route measures seconds, but no person completed a sheet in this run, and filling one as an agent would fabricate human evidence. |
| Default acceptance and citation validity alone cannot pass | Proven for the offline gate | Default-accept fails (0 of 4), automation-bias fails, and every seeded proposal has a citation that resolves. Not shown against live human reviewers. |
| Automation-bias test included; reviewer authority and evidence defined (OQ-017) | Test proven offline; authority unproven | The automation-bias panel and the sensitivity panels are in the report. The authority record in the golden file is provisional; no OQ-017 holder is appointed, and an owner decision is still needed to name one. |

No acceptance criterion is ticked on #223 by this note. A competent real participant, an appointed reviewer holder and measured paired effort remain open, as the closure comments of 2026-10-31, 2026-11-05 and 2026-11-16 state.

## Observed incidents (kept as adverse evidence)

* Run 1 saw zero cases because the driver read the wrong response key (`cases` instead of `items`); run 2 and run 3 got HTTP 403 on writes from the Playwright request context even with the CSRF header; run 4 lacked the `record_id` key. The in-page fetch route, which the web app itself uses, worked in run 5. The failed JSON outputs are preserved beside the passing one.
* The workbench screenshot `live-workbench.png` shows the signed-out landing page; the proof is in the JSON, not the image.

## Resources and residue

* No Azure resource was created, changed or needs deleting.
* The demo store keeps five synthetic AI summary records for ZF-2025-0331 (one diagnostic call, two from run 4 and two from run 5); one is rejected and four are unreviewed. They are synthetic demo data.
* No source files changed; validation tier is the focused tier.

## Remaining human work

* Appoint OQ-017 reviewer holders and have a competent person complete `--worksheet` and `--score` for the demo scenarios.
* Decide whether the demo needs a seeded-defect trial on the live app, which would be a source change under the FULL tier.
