---
title: Issue 116 live changes
---

No source change. Added the round 7 research note, an index row and a log entry. Tier: focused; rpi-checks --all not run. Hosted CI not observed.

| Criterion (unticked in issue) | Status | Evidence |
| --- | --- | --- |
| Allowlists at every provider boundary (run/_chat, evidence, look_at, bytes, legacy, reactive, proactive) | Proven offline; live payloads unproven | docs/reference/research/issue-116-live-r7-evidence-2026-11-22.md |
| Ticked criteria (roles x endpoints, contractor view, redaction, OD-14/19, spy tests, bounds, recheck, documents, permissions, reuse) | Not re-proven live this round; offline suites rerun green | same note and r1 to r6 notes |
| Live role gate | Anonymous 401 on /api/cases and /api/ai/status; credentialed sweep unproven this round | same note |
