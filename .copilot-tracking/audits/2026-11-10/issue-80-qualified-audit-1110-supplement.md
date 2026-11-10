<!-- markdownlint-disable-file -->
# Issue #80 qualified audit supplement (2026-11-10)

Supersedes, without editing, the original audit commit `5d94c710a0903657192ce98493a1317d49f5cc8e` (matrix, research, review, external handoff). Pinned source `c66370042eb08f07839d054433f4483078703cf2`; worktree source equals the pin. Research: `.copilot-tracking/research/2026-11-10/issue-80-qualified-audit-1110-research.md`. Static source reads only; this is not a fresh current-main check and no check was newly executed.

C2 (criterion 2, not a source-correction debit), C4 and #73 stay open. C2 is not proven. Thresholds stay human/open. This work creates no source allowance and no tick.

## Corrections to the original claims

| Original claim (where) | Correction |
| --- | --- |
| "12 CSV routes plus the progress report variant" (matrix line 8, verdict) | Eleven distinct CSV paths plus the progress report variant of `cases.csv`: twelve inventory entries. The matrix's own table already held twelve rows; no thirteenth row was omitted |
| "13 routes, 10 controls" (original external handoff) | Twelve entries: nine source-located controls, three not located |
| "none found in web/" and "re-grep confirmed the controlless claim holds" (matrix lines 31, 33-34, 67; research Finding 1 and 5; review line 12; handoff) | Method defect: a literal search cannot exclude generic or dynamically built controls. Corrected wording: not located by static literal search and a bounded construction trace; generic/dynamic controls not ruled out. These are candidate entry-point gaps, not asserted UI defects |

## Twelve-entry table (pinned source)

| # | Entry | Control located | Where |
| --- | --- | --- | --- |
| 1 | `cases.csv` | yes (href assigned dynamically) | `app.js:805,843` |
| 2 | `cases.csv?report=progress` | not located | server `server.py:513,535-537`; no web code sets `report` |
| 3 | `closed-cases.csv` | yes | `progress.js:189` |
| 4 | `packages.csv` | not located | web consumers are JSON only (`ops.js:366`) |
| 5 | `workorders.csv` | not located | web consumers are JSON only (`ops.js:278,367`) |
| 6 | `handoffs.csv` | yes | `app.js:758` |
| 7 | `visits.csv` | yes | `app.js:2206` |
| 8 | `funding.csv` | yes | `app.js:2216` |
| 9 | `finance.csv` | yes | `panels.js:575` |
| 10 | `asset/stock-queue.csv` | yes | `role-screens.js:225` |
| 11 | `checklists.csv` | yes | `ops.js:217` |
| 12 | `form-schemas.csv` | yes | `role-screens.js:1334` |

Eleven distinct paths (rows 1 and 2 share `cases.csv`), nine controls located, three not located.

## Control construction trace (bounded, source-only)

* No generic export helper exists in `web/`; each control spells its own `/api/...csv` path. Other dynamic hrefs (`app.js:417,1839`, `case-workspace.js:128`, `role-screens.js:278`) build hash navigation; `app.js:1708-1709` is login redirect.
* `packages.csv`, `workorders.csv`: capacity screen reads paged JSON through `pagedPath`; remaining calls are mutating. No anchor to the CSV path was found in the files read.
* `cases.csv?report=progress`: the sole `cases.csv` anchor builds `view` plus `qs(listState)`; `listState` is seeded from `me.work_queues.default` (`app.js:461-463`) and user filters. Server-supplied defaults injecting `report` were not exhaustively excluded; no evidence suggests it.
* Limitation: files read are the pinned `web/*.js` and `index.html`; no browser or runtime was used.

## Mapping to the Root-adopted planning minimum

Planning reference only. It does not narrow "every list" or close the criterion; demo meanings are synthetic scenario assumptions; roles, consent, suppression and one-way boundaries apply now; no real-data permission.

| Group | Covered by an export route (control status) | Gap or unknown |
| --- | --- | --- |
| M1 | cases (control), progress report (not located), closed cohort (control), packages (not located), work orders (not located), visits (control), pending handoffs (control) | Unaccepted handoffs: no CSV |
| M2 | none | Resident choice queue, exceptions: no CSV. Home evidence/decision/quality/defect/handover/history sublists: export status unknown; reference-not-bytes contract undecided |
| M3 | funding, finance, stock queue (controls) | Cost-versus-allocation and grant/invoice/payment columns not verified here |
| M4 | checklists, form schemas (controls) | Form candidates and review registers: no CSV (single-draft held JSON only), gap if displayed |
| Later-only | none; continuity JSON bundle only | Governance, retention, continuity, data-protection, time rows/reports, assistant registry/proposals, law alerts/cards stay disclosed gaps if surfaced as demo lists |
| Excluded | n/a | Navigation, facets, filter vocabularies; chat and memory (BRD RULE-026/AC-096, ADR 0004). Map, briefing, ranking, exposure unclassified: unknown |

A flat current-state CSV does not by itself establish the FR-030/AC-032 history requirement. Per-case sublists are not exempt merely for lacking a standalone page.

## Historical observations (not newly executed)

Original session at the same pin: API list export 11, role inventory 24, form staging 14 OK; schema download 21 PASS; progress 58 PASS after a preserved start failure (`FileExistsError`). Browser export-control coverage was Closed cases and form schemas only. A button or token does not prove correct rows, authorization or immutability.

## Remaining scope and Root decisions (nothing implemented)

* Candidate controls for rows 2, 4, 5 and CSV routes for the M1-M4 gaps need an owner scope decision, per-list contracts and their own RPI; any further control search beyond static reads would need a bounded runtime check Root authorises.
* Human gates remain: full "every list" scope (product/issue owner), live access, retention and suppression (record owners, Security/DPO/Legal), Excel transition thresholds (owners). No retention approved, no requirement changed.
