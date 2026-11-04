---
title: Research for #462 slice 2, 320px resident journey review
ms.date: 2026-11-04
---

* Disposition: executed. Planning readiness: Ready.
* Prior work checked: merged #455, #463, #465, #478, #479 (criteria 3, 4 and 8 ticked on the issue). Slice 1 is open PR #1042 (sensor wording, cold-start notice); this slice is stacked on its branch (`feat/issue-462-r6`) because both edit `demo.js`.
* Owner decision 2026-11-04: resident demo authority runs to end of January 2027. Scope: review login page, own-case summary, history, assistant and sign-out at 320px for plain language, accessibility and clarity. No SQL, employee app, role, network, cost or credential change.
* Method: rendered the real static assets through a loopback fixture server (fake data, fake password, no SQL) in Chromium at 320px and read the text and screenshots; read `index.html`, `demo.js`, `assistant.js`, `demo.css`.
* Findings, ranked by value:
  * Gap 1 (first screen): two synthetic banners fill about 335px of a 700px screen at 320px before the page title. Wording was longer than needed. The Legal and Data Protection Officer review statement must stay.
  * Gap 2 (login clarity): the signed-out page opened with "Your home and works records are read-only ... Nobody will call you", which reads as signed-in text and mentions callbacks before sign-in.
  * Gap 3 (login errors): an empty field gave one generic message and no field was marked invalid, so screen reader users were not told which field.
  * Gap 4 (history): sensor times showed "UTC" and a US-style default locale format; callbacks already use UK time. Chart axis numbers were about 10px at 320px.
  * Gap 5 (sign-out): the failure message was long and passive.
  * Not changed: assistant panel length (copy sits in the shared chat widget and consent and data-saving notices must stay in full); launcher overlap with the footer is already padded. Routed to later work.
* Boundaries kept: no change to authentication, session, CSRF, case mapping, consent, approvals or AI behaviour. Manual callback path and AI-unavailable text unchanged.
* Validation tier: focused. No security, infrastructure, SQL or deployment change. Live deploy not needed for this slice; it is a later owner or coordinator step.
