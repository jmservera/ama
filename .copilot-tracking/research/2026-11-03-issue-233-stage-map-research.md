# Research: issue 233 same-home journey stage map

Date: 2026-11-03. Disposition: reused existing evidence plus a read of merged work. Planning Readiness: Ready.

* Merged under Refs #233: #671 (trace and checker), #713 (status refresh), #767 and #815 and #838 (guardrails, withheld panels), plus #496 foundation; #495 closed unmerged.
* Unmet criteria after those: complete tracing (one theme deferred by design), tension resolution only a proposed rule, same-home walk (EX-HOME-901 design-only, stage 1 deferred), WCAG 2.2 rendered evidence (#151), design-system component verification (#150). Hypothesis label met.
* Every registered screen renders from `render(c)` for a selected case, so one case id can be carried across screens via `screenHref`.
* Smallest coherent slice: a same-home stage map on `programme-queue` linking stages to the role screens for the selected case. Navigation only; no fixture, endpoint or authorisation change.
* Stacked follow-ups: (1) EX-HOME-901 fixture and per-stage data; (2) stage 1 source-account screen on `resident-choice`; (3) rendered keyboard and assistive-technology checks (#151); (4) component check (#150); (5) user validation (#155).
* Boundaries: profile selection is a view filter, not authorisation; resident consent and human approval untouched; no AI feature involved. Tier: focused (web-only; no security, infrastructure, SQL or deployment change).
