# Research: issue 146 closure re-verification (2026-11-18, fresh worker)

Research disposition: executed (live read-only Azure, Playwright on the demo app, offline tests). Planning Readiness: Ready.
Scope: synthetic demo, desktop only; tier FOCUSED (documentation only, no src change).
Primary evidence: docs/reference/research/issue-146-live3-monitoring-closure-2026-11-18.md (raw: issue-146-live3-evidence-2026-11-18/).

Findings
* Open criteria: C1 alerts, C2 workbook, C3 runbook owner, T2 tokenomics dashboard. None can be fully closed on the demo.
* New: source job-failure shape (Maximum) did not fire on two fresh failures; Total fired. Follow-up needs the FULL tier.
* New: queue service has an audit diagnostic setting now; poison alert still not installed or readable.
* New: in-app AI usage by capability with unreconciled state proven by Playwright (T2 proven for the demo except Azure cost beside it).
* Earlier stalled worker left tmp146 rules and a job; deleted after recording.
