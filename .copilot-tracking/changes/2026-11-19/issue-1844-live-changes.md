# Changes: issue 1844 (2026-11-19)

Refs #1844. No source change. Tier FOCUSED; only `.copilot-tracking/` artifacts added. Validation: `git diff` review; no tests apply because no `src/` file changed. No browser run was made.

| Criterion | Status | Reason |
| --- | --- | --- |
| 1 failing-first regression, served-byte identity | Unproven | Defined at 320/390 px widths; excluded by the desktop-only demo decision |
| 2 four viewports, both tile states | Unproven | Narrow widths excluded |
| 3 focus, selection, no horizontal overflow | Unproven | Narrow layout work excluded |
| 4 attribution after scroll at short heights | Unproven | Short mobile heights excluded |
| 5 existing map browser/axe checks, manifest hash | Not applicable | No recipe or source change |
| 6 dated RPI artifacts, independent review, hosted CI | Partly proven | Artifacts delivered; independent exact-head review and hosted CI are not needed for the demo |

No criterion is unmet for the desktop-only demo; the narrow-width defect (`.map-home-card` absolute at `style.css`) stays open in the issue.

## Re-run 2 (branch test/code-live-20261119T135807Z)

The per-criterion table above is re-confirmed unchanged. Changed files: this record, the plan, details, critique, review and research artifacts, the state file, the research note `docs/reference/research/issue-1844-live-20261119-2026-11-19.md` and a `docs/reference/log.md` entry. No `src/` file, workflow, dependency, SQL or infrastructure change; no Azure action. Validation: `git diff` review only.
