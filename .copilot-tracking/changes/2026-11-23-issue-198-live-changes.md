# Changes 2026-11-23 issue 198

Tier: focused; no `src/`, workflow or registry change. Review conformant.
Added: docs/reference/research/issue-198-rubric-live-20261123T010043Z-2026-11-23.md and raw outputs; README index row; log entry; RPI artifacts.

## Per-criterion table

| # | Criterion | Status | Why |
| --- | --- | --- | --- |
| 1 | Baseline recorded | Proven (ticked) | #292, latest.json, 2026-11-21 note |
| 2 | src coverage registry PR | Proven (ticked) | #292 |
| 3 | Per-PR dual-window totals | Unproven, owner-gated | PR bodies record test counts, not totals; scoring moved to main (#748); cannot be created retroactively |
| 4 | Cut-over registry PR and ordering | End state proven, ordering unproven, owner-gated | No mvp or prototype glob (grep exit 1, 0 tracked files); no single PR after an old-registry-scored deletion |
| 5 | README and failures reassessed | Proven (ticked) | #705; 84 passed, 0 failed now |
| 6 | Lock recompiled | Proven (ticked) | #748 |
| 7 | Before and after comparison | Proven (ticked) | #880: 47 to 79 now |

Live: revisions 0000054 and 0000026 active, unrelated to the registry. Open: owner waiver or rewording of 3 and 4. Azure change, browser and sign-in checks not applicable.
