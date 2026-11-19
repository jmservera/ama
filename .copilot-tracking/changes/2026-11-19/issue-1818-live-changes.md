# Changes: issue-1818-live, 2026-11-19

Refs #1818. Documentation and evidence only; no `src/` change (focused tier). Read-only Azure and browser observation; no resource created, so nothing to delete.

| Action | Result |
| --- | --- |
| Employee and resident Playwright probes (unchanged merged scripts) | `/api/map` 200, 3 stale demo homes, 97 restricted, 343 not-loaded; resident view stale, single home |
| Added `docs/reference/research/issue-1818-live-20261119-2026-11-19.md` and redacted evidence folder | retained output in the repository |
| Index and log entries | added |

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 `/api/map` sensor summary | Proven (demo) | research note |
| 2 Map card, list, filter | Proven (demo) | research note |
| 3 Resident `#sec-sensors` | Proven (demo) | research note |
| 4 Tests and browser checks on exact HEAD | Unproven here | ticked by #1826; no source change |
| 5 Live Hub to SQL to UI walkthrough | Proven for the demo (retained observation); sender and receiver fix not on main | the Hub to SQL leg was not re-run; landing it is FULL-tier SQL work, not attempted |

Validation: link and diff review only; credential-line scan of new files found no match.
