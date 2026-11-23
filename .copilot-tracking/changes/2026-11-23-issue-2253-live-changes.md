# Changes: issue 2253 live (2026-11-23)

Tier: focused (no src change). Basis: documentation and evidence only; the local wiring test (15 tests) passes; hosted CI not observed (not pushed).

## Files

* docs/reference/research/issue-2253-live-2026-11-23.md (new)
* docs/reference/research/issue-2253-live-2026-11-23/live-0000026.json and .png (new)
* .copilot-tracking research, plan, details, changes, review, rpi-sessions records (new)

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Labels sized like body text | Proven live (0000026) | 16.8 px vs 16 px |
| No 'Latest stored' / 45 overlap | Proven live | 0 overlaps |
| Circle markers as the legend states | Proven live | 8 circles, legend updated |
| Not one thick stroke | Proven live | 1 of 8 pairs touch |
| Narrow-screen rule | Unproven | out of scope, desktop-only demo |
| Owner-gated | None | n/a |

Root cause: rem text in SVG user space plus dense markers; fixed in a6c0910c97, no remaining gap. Revision 0000054 (API) Healthy, serves the unchanged data path.
