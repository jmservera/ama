---
title: Issue 1288 r14 research
date: 2026-11-23
---

Refs #1288. Demo, desktop only. Task r14, Research disposition: reused (r13 research and r12 live probe) plus one targeted code read. Planning Readiness: Ready.

## Evidence

* Unticked criteria 3 to 8. The r13 note records criterion 4 and 8 blocked by the absent approved release record (OQ-017); owner-only, no code gap.
* `review_flag` in `src/core/src/zava_forward/core/assistants.py` downgrades a flag for impossible readings present at capture time only. A cited reading whose current content is now impossible (a corrected row keeps its id) is reported only as `changed_since_capture`, and the flag stays an autonomous L4 `review-suggested` flag. This is the r13 rank 2 follow-up and the only remaining code gap found.
* The previous session state file was malformed (duplicate keys from a merge); it is rewritten cleanly.

## Plan inputs

* Downgrade to `implausible-readings` when the current successful capture shows a cited reading with an impossible value.
* One test in `src/api/tests/test_quality_sensor_grounding.py`.
* Live legs carried from r12 unless a read-only probe is possible; Azure is not changed.
