---
title: Changes issue 1837 live 2026-11-23
ms.date: 2026-11-23
---

No src change; focused tier (evidence only; no workflow, dependency, Dockerfile or gate file touched). Base `342fad401d`. Refs #1837. No Azure resource created or changed; no credential recorded.

Files: [evidence note](../../../docs/reference/research/issue-1837-live-demo-evidence-2026-11-23.md), folder `docs/reference/research/issue-1837-live-2026-11-23/`, `docs/reference/log.md` entry, 2026-11-23 RPI artifacts.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Failing-first coverage, three submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](../../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); 66 tests pass on main |
| 2 Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | Route forms run POSTs 200 x3; a live write adds irreversible shared-demo records, so none attempted |
| 3 Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests; live revision 0000054 probe 400, 400, 403, 400, 404, 400, case unchanged |
| 4 Browser journeys with axe, zero unexpected skips, unit tests | Proven locally with a qualification | Three journeys passed with zero violations; nomination needed a third run after two load-induced client timeouts |
| 5 Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | Dated artifacts exist; independent review and hosted CI are coordinator/owner steps, not run here (no push) |
| 6 Full-tier classification and receipt | Not applicable | No src change; focused tier; `rpi-checks.py --all` not run by instruction |
