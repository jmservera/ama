---
title: Issue 135 exception screen r2 quarantine label correction research
ms.date: 2026-11-07
---

* Task: `issue-135-exception-screen-r2-quarantine-label`. Parent task: `issue-135-exception-screen` (original artifacts and Review preserved unchanged). Frozen start HEAD `26ce7c711ebffb37129fe0ca24b7b94c0d8356e1`, tree `ccf89ee645b2cb00c9662ae6d42ded586e4ea9c7`; main and parent #73 topic `23b26a7f3a4693cd20dcf0447303d97491096cb3`.
* Research disposition: executed (source reading and the preserved r1 observed outputs; no server, browser or model run in this phase).
* Planning Readiness: Ready.

## Trigger (observed, preserved)

* The r1 focused gate passed (receipt sha256 `9e37ae4202dfd2b4d5d2230acfd486070618dec99594d2d670400c2cd495e9a1`) but did not exercise the new feature. The external r1 real-DOM story (`/mnt/ama-gates/g135-browser-1107/logs/story-run2.*`, exit 1) failed at "quarantined AI shown with reason". Run 1 failed for a separate helper expectation error (expected 2 failed-AI rows, actual 3 because a real briefing fallback is emitted at sign-in). The two are kept apart.

## Contract evidence

* `core/ai_tasks.py:39` `QUARANTINED = "Quarantined"`; set as a record status at `ai_tasks.py:281`. `exception_feeds._ai_failure_reason` tests `rec.get("status") == QUARANTINED` and raises `failed_ai_run` with `original_source.status` copied unchanged, so the endpoint returns `"Quarantined"`.
* Fallback items are AI-mode requests with `source != "ai"` and a non-empty `fallback_reason`. Their `original_source.status` is the record status (for example `"Not reviewed"`) and `error` is that reason. A returned failed-AI item with no reason is outside the feed contract and must stay Unknown, not be called a fallback.
* `core/tests/test_exception_feeds.py:128` already constructs the canonical `"Quarantined"`.

## Defect

* `role-screens.js:876` compares `original_source.status === "quarantined"` (lowercase). The real value never matches, so quarantined results are labelled "Fell back to rules or template".
* `test_exception_register_screen.py:27` constructed lowercase `"quarantined"`, so the unit test hid it. The fallback fixture used `status: "fallback"`, also not a returned value.

## Decision

* Smallest fix: compare the canonical value case-insensitively (`typeof status === "string" && status.toLowerCase() === "quarantined"`), keeping lowercase fixtures compatible. The file has no shared status-normalisation helper, and none is added.
* Do not describe an item as a fallback unless it carries a reason; otherwise say how it failed is Unknown (no success or fallback claim).
* Test: use the real `"Quarantined"` and `"Not reviewed"` values, keep one lowercase compatibility case and add one reason-less item.
* Reserved paths only: `role-screens.js`, `test_exception_register_screen.py`. No backend, auth, store, schema, model, control or role change; F3/F4/F5/F6 untouched.
* Web Interface Guidelines fetched successfully (HTTP 200, `command.md`) before edit; refresh before Review.
