---
title: Issue 151 live r2 changes
ms.date: 2026-11-18
---

No `src/` change. Tier FOCUSED (documentation and evidence only; basis: no executable, workflow, dependency or deployment file touched).

Files: `docs/reference/research/issue-151-live-r3-wcag-evidence-2026-11-18.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (entry), tracking artifacts and `.copilot-tracking/evidence/2026-11-18/issue-151-live-r2/`.

Divergence: the research note is named r3 because an r2 note already existed on main. A cleanup `rm -rf` briefly removed tracked files under `.copilot-tracking/research/2026-11-18/`; they were restored with `git checkout`.

Live Azure: read-only; nothing created, nothing to delete. Credentials never printed; literal scan of retained evidence found no match.

## Per-criterion table

| # | Criterion | Ticked in issue | Demo status | Basis |
| --- | --- | --- | --- | --- |
| 1 | Target conformance level and scope decided | yes | not re-tested | prior |
| 2 | Audit covers keyboard, focus, name/role/value, status, contrast, reflow, target size, errors | yes | not re-tested; corroborated (axe 0 violations, contrast heuristic only disabled controls, reflow, error alert on resident sign-in) | r3 note |
| 3 | Automated checks in CI | yes | not re-tested | prior |
| 4 | Manual screen-reader and keyboard checks per role workflow | no | keyboard partly proven (one employee role, resident); screen reader unproven (person-run, production-only #1907); other roles unproven (no accounts) | r3 note |
| 5 | Map, charts, tables accessible equivalents (#119) | yes | not re-tested | prior |
| 6 | Accessibility statement draft lists gaps | yes | not re-tested | prior |

Unmet: criterion 4. Production-only: person-run AT testing, DPO/Legal, billing, mobile.

Validation: documentation link and diff review; secret scan; `git diff --check`.
