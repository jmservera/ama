<!-- markdownlint-disable-file -->
# Issue #80 C2 current-main acceptance and inventory matrix

Base `c66370042eb08f07839d054433f4483078703cf2` (= fetched `origin/main`). Research: `.copilot-tracking/research/2026-11-10/issue-80-main-export-audit-1110-research.md`. Audit only; no source change; no tick; no allowance.

## Verdict

C2 ("Every list offers an Excel or CSV export; Excel stays one-way read-only") is NOT proven by current main and cannot be proven mechanically: "list" is undefined. 12 CSV routes plus the progress report variant exist and are shared-serializer, values-only. Browser proof of an export control exists for 2 of those (Closed cases, form schemas). Distinct unexported source-supported registers and 3 controlless exports are listed below. C4 thresholds stay HUMAN/OPEN. No AT, human or live approval is claimed.

Proof levels: S source read; A targeted API test covers the route class or role gate; B browser check drove the control; N none. A, B here do not prove row correctness for every list unless stated.

## Check outcomes (raw logs under Root `checks-80-main-export-audit-1110/`)

| Check | Result | Covers |
| --- | --- | --- |
| Owned venv, import origins | Pass: core, agents, api all resolve under this worktree (`origins.log`) | environment only |
| `test_list_export_api` | 11 tests OK | `LIST_EXPORTS` set, finance/stock parity with JSON, role limits, formula safety, denial, read-only |
| `test_role_endpoint_inventory` | 24 tests OK | every server route has a role expectation (route and role gate, not rows) |
| `test_form_staging_api` | 14 tests OK | form-schemas CSV and staging API |
| `schema_download_browser_check` (flock -n) | exit 0, 21 PASS | form-schemas control: keyboard, saved file, authorized, denied roles refused, no leak |
| `progress_browser_check` attempt 1 | FAILED to start: my pre-created `--out` dir existed (`FileExistsError`); no check ran; log kept as `browser-progress-attempt1-out-exists.log` | none |
| `progress_browser_check` attempt 2 (flock -n, fresh out path) | exit 0, 58 PASS, 0 FAIL | Closed cases CSV: page bytes equal JSON page, filters kept, empty/reset, read error offers no link, non-manager gets no attachment |

No check was BUSY or skipped. The second attempt is a divergence from "once per check" caused by my argument error, not by a check failure; disclosed in the changes file.

## Exported lists

| Route | Roles (source) | Source / filter / order / paging | UI control | One-way note in UI | Proof |
| --- | --- | --- | --- | --- | --- |
| `cases.csv` | staff | `list_cases` view/filters, same as JSON | yes `app.js:805` | label only | S, A (role) |
| `cases.csv?report=progress` | staff | `core.progress.export_csv` | none | n/a | S |
| `closed-cases.csv` | managers | current filtered page only, bounded limit | yes `progress.js:189` | yes | S, B (rows = JSON page, denied reader) |
| `packages.csv` | staff | `list_packages`, unpaged | none | n/a | S, A |
| `workorders.csv` | staff, not contractors | `list_work_orders`, optional case, unpaged | none | n/a | S, A |
| `handoffs.csv` | staff, own or manager rows | `pending_handoffs` | yes `app.js:758` | label only | S, A |
| `visits.csv` | staff; `view=all` per JSON contract (observation, not judged) | `visits(view)` | yes `app.js:2206` | no | S, A |
| `funding.csv` | staff | `funding_list` | yes `app.js:2216` | yes | S, A |
| `finance.csv` | finance roles | `finance_queue`, parity with JSON | yes `panels.js:575` | yes | S, A (parity) |
| `asset/stock-queue.csv` | managers | `stock_queue`, parity with JSON | yes `role-screens.js:225` | yes | S, A (parity) |
| `checklists.csv` | staff | constants, no case data | yes `ops.js:217` | yes | S, A |
| `form-schemas.csv` | forms read rights | `SCHEMA_EXPORT_FIELDS` projection | yes `role-screens.js:1334` | yes | S, A, B |

Version, source and history columns are a per-list row contract; the shared serializer provides values-only output with formula neutralisation and no read-back path. Blob proof: none of these routes touches a blob; none is claimed.

## Source-supported lists without CSV or Excel export

`handoffs/unaccepted`, `resident/choice-queue`, `exceptions`, `retention`, `governance` registers, `continuity` (JSON bundle only), `data-protection`, `time/mine` and `time/report`, `assistants/proposals` and registry, `law/alerts` and `law/cards`, form-candidates and form-review lists. Role, shape and consumer detail: research Finding 2. Whether each is in scope, and each one's fields and suppression contract, is undecided.

Unknown (not counted, not narrowed): `finance/exposure` (a signal), `ranking/snapshot`, `map`, `briefing`, per-case sublists, and the 48 `ul` and 24 table nodes in `web/`.

## Exclusions

* `chat/threads` and `chat/memory`: excluded by RULE-026 and AC-096.
* Unmerged #1395 and #1400 UI; retained `d8ce761a` and `9b2572cf`; #303 importer export (not re-audited).
* Facets, filter vocabularies and navigation lists are not business registers (classified from source).

## Not established by these checks

A button or token does not prove correct rows, authorization or immutability. Browser proof does not extend beyond Closed cases and form schemas; the other controls rest on S and static tests. Row content and order for packages, workorders, visits and funding beyond staff parity is untested. No UI review or design change was done: the Web Interface Guidelines source was fetched but the response was truncated at 6,000 characters (rest unread), so no guideline-based UI finding is made; repository Fluent 2, WCAG baseline and plain-language standard take precedence and were not re-read for this audit.

## Exact owner decision needed

The issue owner defines (1) the in-scope list register for "every list", (2) the exclusions beyond chat and memory, and (3) each in-scope list's role, projection, suppression, retention and one-way wording contract. Until then C2 stays unmet and is not deemed blocked.

## Remaining scope for Root (not implemented, no allowance claimed)

1. UI controls for `packages.csv`, `workorders.csv` and progress `cases.csv` (distinct, evidenced entry-point gap).
2. CSV routes for any register the owner puts in scope (table above); each needs its own RPI, role/projection/retention contract, API test and browser proof.
3. Wider browser proof of existing controls if Root wants it.
Dependencies: owner definition of list; parent #73 is hierarchy only with no implementation dependency; C4 thresholds independent and human/open.
