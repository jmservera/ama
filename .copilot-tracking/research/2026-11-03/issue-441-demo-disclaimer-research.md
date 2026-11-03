---
title: Issue 441 demo disclaimer research
date: 2026-11-03
task_slug: issue-441-demo-disclaimer
---

Disposition: `executed`. Planning Readiness: `Ready`.

Merged work already delivered (not redone): #442 (BRD, PRD, addendum, unregistered proposal), #454, #686, #726 (rechecks), #766 (owner packet), #463 (synthetic showcase). Criteria 1-4 and 6-8 are proven by those. Criterion 5 (FR-044/AC-084 owner disposition) and 9 (exact-head review, gates) remain unmet.

Owner decision 2026-11-03: ship the optional resident portal demo with a demo-only disclaimer that Legal/DPO review is outstanding (same basis as #766).

Findings: both resident pages (`resident_demo/web/index.html`, `resident_preview/web/index.html`) already carry a `role="note"` synthetic banner, a manual-help route and no AI dependency. No page said Legal/DPO review is outstanding. Existing tests assert the banner phrases, which stay unchanged.

Smallest slice: add one sentence to each banner, a CSS rule, two test assertions, an API README note and one log entry. Not security, infrastructure, SQL or deployment: focused tier.

Overlaps: no open-PR overlap was checked beyond the branch base origin/main 9a9f9dada; log.md is append-only with union merge.
