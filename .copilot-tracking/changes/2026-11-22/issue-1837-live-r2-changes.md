---
title: Changes issue 1837 live r2
ms.date: 2026-11-22
---

No source change; focused tier (evidence only). Base `2893d5098d`. Refs #1837.

Files added: [evidence note](../../../docs/reference/research/issue-1837-live-demo-evidence-2026-11-22-r2.md), its artifact folder `docs/reference/research/issue-1837-live-2026-11-22-r2/`, a log entry in `docs/reference/log.md`, and the r2 RPI artifacts.

Fix state: main already carries the fix (#2110 and earlier); no open PR overlaps. No Azure resource created or changed; no credential recorded.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Failing-first coverage, three submissions, valid challenge target | Proven (earlier record) | Failing-first run at 9da3fcd; 66 tests pass on current main |
| Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | Route forms run POST 200, 200, 200; a live write would add irreversible shared-demo records |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven | 66 unit tests; live probe 400, 403, 400, 404, 400; case unchanged after probes |
| Browser journeys with axe, zero unexpected skips | Proven locally | Three journeys passed, zero violations; one color-contrast incomplete needs human review |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven | Dated artifacts exist; independent review and hosted CI unavailable to this worker |
| Full tier receipt | Not applicable | No src change; `rpi-checks.py --all` not run by instruction |

Qualification: the live form probe once reported the case JSON changed around a rejected submit; controlled repeats showed no difference and the cause is not isolated (shared demo activity suspected).
