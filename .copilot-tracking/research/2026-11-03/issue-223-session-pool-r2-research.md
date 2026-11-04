---
title: Issue 223 session pool research
date: 2026-11-03
---

Disposition: executed (reuses prior evidence).
Base: origin/feat/issue-218-rai-control-stack (6ef54161f). Parent epic #218.

Already delivered (merged): #428 protocol, #638 scripted panels and gate, #701 reviewer authority, #817 manual human-session intake, #855 per-session class, automation-bias and effort report.
Gap found: score_human_session scores one sheet only. Criterion 3 asks for total review effort and detection reported against the same scenarios; no way to pool sessions or to show that a repeat reviewer is not independent. Golden authority lists only EV-01, so a second reviewer cannot yet pass (OQ-017 open).
Smallest coherent slice: pool_human_sessions plus multi-sheet --score. No security, infrastructure, SQL or deployment change.
Planning Readiness: Ready.
