---
title: Research, issue 153 content-audit live run 2
ms.date: 2026-11-18
---

Refs #153. Research disposition: executed. Scope: synthetic demo, desktop only (owner decisions 2026-11-18).
Only unticked criterion: "Resident-facing wording is reviewed by a named human before any use".

Existing evidence reused: `docs/reference/research/ux/content-standard.md` (standard, glossary, earlier audit slices) and
`docs/reference/research/plain-language-live-153-2026-11-18.md` (first live audit: 13 staff views, resident page,
findings F1 to F5). This run adds case-page tabs on three cases, four more staff views and the whole resident page.

Method and result: Playwright Chromium 1440x900 against `ca-cutover-test-demo-api` and `ca-resident-demo`, read-only;
visible text scanned for banned terms; screenshots redacted in the DOM before capture. Findings N1 to N6 (Unassigned,
Held and envelope, jargon in a refusal) and holds P1 to P5 are in
`docs/reference/research/content-audit-live-153-2026-11-18.md`. Raw page text not retained; hit summary and 43
screenshots are.

Collision notes: the existing `issue-153-live-state.json` and prior 2026-11-18 live artifacts (plain-language-live,
`2026-11-18-issue-153-live-*`) were left untouched (the state file was briefly overwritten by mistake and restored
from git before any commit). This run uses state `issue-153-live2-state.json` and slug `issue-153-content-audit`.
A credential-file read was done in scripts only; no value was printed.

Planning Readiness: Ready. Open follow-ups: fix N1 to N3 and N5 wording in source (needs FULL tier if source changes,
not done here).
