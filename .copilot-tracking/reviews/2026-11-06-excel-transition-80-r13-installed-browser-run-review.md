---
title: Issue 80 r13 review, owned installed environment and schema download browser run
description: Separate later author Review after the actual browser run and Changes commit; not independent acceptance
ms.date: 2026-11-06
---

* Review execution: executed once after the browser run and the Changes commit e8190f801. Boundary: the r13 Changes and the external evidence in `/mnt/ama-gates/e80-r13-r67-1106/`. Author review, not independent. The independent plan critique (six findings, five accepted, one rejected with reason) is recorded in the plan.
* Outcome: no findings that block the stated observation. Open items are listed below.

## Evidence assessed

* Prospective chronology: Research, Plan, Details and the critique were committed as 472ae7da before any venv, install or run step.
* Parent environment is pip-installed from the candidate's own wheels in an external venv; four concrete modules resolve in the venv with bytes identical to the checkout. Initial failures (missing aiohttp, wheel build a1, provenance script a1 and a2) are preserved.
* The prepared module ran unchanged: exit 0, 21 PASS, COMPLETE, stderr empty, under the nonqueued lock and the unmodified `worker_limit(1)`.
* Ignored-inclusive status stayed empty; production, harness and check hashes did not change.
* Web guidelines: no web file was changed or reviewed in r13, so the guideline source was not refetched.

## Open items

* The child server runs checkout sources by harness design; the parent is installed. Parent and child bytes were shown identical for four modules only, not every module.
* The wheel route deviates from the guides' editable wording; the stated reason is checkout cleanliness.
* No axe scan, WCAG, assistive technology, Fluent, concurrency, every-list export, owner threshold, main or live acceptance. FULL on the final frozen head needs a new admission, then independent exact-head review and hosted CI. Nothing was ticked, closed or published.
