<!-- markdownlint-disable-file -->
# Issue #80 qualified audit correction: research

* Task: `issue-80-qualified-audit-1110`. Date 2026-11-10. Documentation-only correction of the original audit `issue-80-main-export-audit-1110` (commit `5d94c710a0903657192ce98493a1317d49f5cc8e`, preserved, not edited).
* Mode manual; phases advance in order because Root orders the loop. Research disposition: executed (bounded source-only inspection). Planning Readiness: Ready.
* Pinned source `c66370042eb08f07839d054433f4483078703cf2`. `git diff --stat c66370042 HEAD -- src` is empty, so the worktree source equals the pin. These are static reads of that source, not a fresh current-main check and not newly executed checks.

## Reviewer findings addressed (same reviewer, Readiness, approve_with_comments)

1. Medium: totals. Table in the original matrix has eleven distinct CSV paths plus the progress report variant of `cases.csv`, twelve entries, not "12 plus progress" (13). Located controls nine, not located three, not ten. The original handoff's "13 routes and 10 controls" and the matrix verdict line were wrong. No omitted thirteenth row was found: the nine `LIST_EXPORTS` paths (`server.py:165-166`) plus `cases.csv` and `closed-cases.csv` are eleven paths; `cases.csv?report=progress` is the twelfth entry.
2. Medium: literal grep is not proof of absence.

## Bounded source trace of CSV control construction (web/, pinned source)

Search of all `web/*.js` and `index.html` for `csv`, `download`, `.href =`, `setAttribute("href"`, `location.href`, `createElement("a")`:

* Nine located controls, all anchors with a literal or templated `/api/...csv` href: `app.js:758` handoffs, `app.js:805,843` cases (href assigned dynamically as `/api/cases.csv?view=${view}&${qs(listState)}`), `app.js:2206` visits, `app.js:2216` funding, `ops.js:217` checklists, `panels.js:575` finance, `progress.js:189` closed cases (href `/api/closed-cases.csv?${download}`), `role-screens.js:225` stock queue, `role-screens.js:1334` form schemas.
* No generic export helper exists: no shared function builds a CSV URL from a route name. Each control spells its own path. Other dynamic `href` assignments (`app.js:417,1839`, `case-workspace.js:128`, `role-screens.js:278`) build hash navigation links, and `app.js:1708-1709` is login redirect.
* `packages.csv`: the only web consumers of `/api/packages` are `ops.js:366` (paged JSON via `pagedPath`, limit/offset) and mutating calls `ops.js:404,430`. No anchor. Not located by static literal search or by trace of the capacity screen; generic/dynamic controls not ruled out beyond the files read.
* `workorders.csv`: consumers `ops.js:278,367` (JSON) and mutating calls `ops.js:437-453`. No anchor. Same limitation.
* `cases.csv?report=progress`: the only `cases.csv` anchor is `app.js:843`, whose query is `view` plus `qs(listState)`. `listState` holds filters seeded from `me.work_queues.default` (`app.js:461-463`) and user selections (stage, q, area, wave, owner, flag, queue, sort). No code sets `report`. The server reads `report` for `/api/cases.csv` (`server.py:513,535-537`). Whether a server-supplied default could inject `report` was not exhaustively excluded; no evidence suggests it. So the progress variant has no located control, with that limitation.

Conclusion wording used everywhere: "not located by static literal search and a bounded construction trace; generic/dynamic controls not ruled out". No UI defect is asserted, and no runtime or browser check was run to confirm absence.

## Mapping to Root-adopted planning minimum (domain-demo-acceptance-1932)

Planning reference only; it does not narrow "every list" or close the criterion. Demo meanings are synthetic scenario assumptions. Roles, consent, suppression and one-way boundaries apply now; no real-data permission.

| Planning group | Original-audit rows (source-qualified) | Gap or status |
| --- | --- | --- |
| M1 delivery | cases (CSV, control), progress report variant (CSV, control not located), closed cohort (CSV, control, browser-observed historically), packages (CSV, control not located), work orders (CSV, control not located), visits (CSV, control), handoffs pending (CSV, control) | Unaccepted handoffs (`/api/handoffs/unaccepted`) have no CSV: gap |
| M2 resident/control | none exported | Resident choice queue and exceptions: no CSV (gap). Per-case home evidence, decision, quality, defect, handover and history sublists: export status unknown, rendered in case detail; reference-not-bytes contract undecided |
| M3 stewardship | funding, finance, stock queue (CSV, controls) | None missing from the original inventory; building-cost versus home-allocation and grant/invoice/payment state columns not verified here |
| M4 reference/form | checklists, form schemas (CSV, controls; schemas browser-observed historically) | Form candidates and review registers: no CSV (held single-draft JSON only), gap if displayed |
| Later-only (owner-prioritised, outside minimum) | none exported; continuity JSON bundle only | Governance, retention, continuity, data-protection, time rows/reports, assistant registry/proposals, law alerts/cards remain disclosed gaps if surfaced as demo lists; JSON alone does not meet Excel/CSV |
| Excluded | facets, filter vocabularies, navigation; chat and memory | RULE-026 / AC-096 and ADR 0004 for chat/memory; map, briefing, ranking, exposure need classification (signal is not automatically a list) |

Flat current-state CSV does not by itself establish the FR-030/AC-032 history requirement.

## Historical observations carried forward (not newly executed)

API 11/24/14 OK, schema 21 PASS, progress 58 PASS (and the preserved attempt-1 start failure), observed at the original session at pinned base `c66370042`. They are source-qualified historical observations only. Browser coverage covered Closed cases and form schemas only.

## Boundaries

C2 (criterion 2, not a source-correction debit), C4 and #73 stay open. Thresholds stay human/open. No source, test, dependency or config change, no missing control or route implemented, no retention approved, no requirement changed. This work creates no source allowance. Original handoff, matrix, review, raw logs and canonical chain are preserved.
