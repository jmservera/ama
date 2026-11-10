# Issue 74 current-main acceptance matrix

Date: 2026-11-10. Subject: the one unmet #74 criterion "Building-level dependencies, holds, works and costs are shown apart from each home's evidence, decision, cost allocation and outcome" (PRD FR-002 wording adds shared systems). Audit only.

## Pins

* Main `c66370042eb08f07839d054433f4483078703cf2`, tree `9f2e4cfbffa11b84ae3b0eb7b0fa1560b6a25137`, equal to fetched `origin/main`. Blobs and PRD/BRD identities: [research](../research/2026-11-10-issue-74-main-acceptance-audit-research.md). PRD v0.21.0 `in-review`; BRD v0.21.0 `draft` (no approved baseline).
* Executed code: own venv `/tmp/ama-74-venv-1110` with non-editable installs of `src/core`, `src/agents`, `src/api` and `playwright==1.64.0`; installed `home_case.py`, `buildings.py`, `server.py` and `web/app.js` hashed equal to the pinned blobs. The browser runner's server child ran the worktree source directly.
* Store/projection: core `HISTORY` versions, JSON `Store` and `SqlStore` (SQLite file) only; no SQL Server, Azure or default dataset. Fixture: `building_fixture.fixture()` and `home_case_data()` (wholly synthetic, owned temporary data).

## Runs (raw logs in Root evidence folder `phase74-main-acceptance-audit-evidence-1110`)

| Check | Command (cwd) | Exit | Result | SHA-256 of log |
| --- | --- | --- | --- | --- |
| Env install | `pip install ./src/core ./src/agents ./src/api playwright==1.64.0` | 0 | installed; `playwright` was absent from system Python | `1bc632eeb2d12e02bab21ccdcbd020a095645d7023c330c15c1462f347132b11` |
| Core | `python -m unittest discover -s tests -p test_home_case.py -v` (`src/core`) | 0 | 7 ran, 7 ok, 0 skips | `00fc5d1b34f92533935c61604b77c84e7c9ceb02ac310c06056c86ef6b16f402` |
| API | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_home_case_api.py -v` (`src/api`) | 0 | 3 ran, 3 ok, 0 skips | `54a285e909aeba95c0d0139703af4cf60b950e5b0bb42e690a623b5a61810bc6` |
| Browser | `ZF_BROWSER_SCRATCH=/tmp/zf74b ZF_AXE_JS=/tmp/axe-4.10.3.min.js flock -n -E 99 /tmp/ama-rpi-heavy.lock python -m checks.home_case_browser_check` (`src/api`) | 0 | lock free (not 99); 17 PASS lines, `COMPLETE ... axe 4.10.3`, zero axe violations, no writes, no JS errors | `6dfcd77b9d9b4b2b8d614f844e57220ed6f64da9e1f9d512ed39fb49ca79f273` |

The axe file hash equalled the pinned `AXE_SHA256` inside the check. No check was skipped, edited or weakened. No private dataset, SQL, image, cloud, provider or model was used.

## Field matrix (role = Retrofit Programme Manager, finance view, unless stated)

Status: LO local-observed (asserted by a maintained check that ran here, constructed fixture); IU implemented-unverified (present in pinned source, no maintained check asserts it); UK unknown.

| Field | Side | Status | Evidence | Exact remaining action |
| --- | --- | --- | --- | --- |
| Shared systems | building | IU | `homeCaseView` renders `shared("systems")` under the building region (`app.js:1284`); fixture has SYS-1 but no check names it | Maintained assertion that SYS-1 is in the building region and not in the home region |
| Dependencies | building | LO | Browser: `DEP-1` in building region text, not in home region; fixture dependency is added by `home_case_data()` | None for criterion; role coverage below |
| Holds | building | LO | Browser: `HOLD-1` building only | Same |
| Works | building | LO | Browser: `WORK-1` building only | Same |
| Costs | building | LO | Browser: `GBP 12000.00` building only; core: `costs[0]` 12000.00 on JSON and SQLite stores | Same |
| Evidence documents | home | IU | Source renders `home.documents` (`app.js:1275-1276`); core asserts `links.document_ids` only; no check asserts the rendered list, though sibling evidence absence from `main` is asserted | Maintained assertion of an own-home document in the home region for two homes |
| Decision | home | LO | Browser `Decision: Accepted` in home region; API `home.decision.status` Accepted | None |
| Cost allocation | home | LO | Browser `GBP 6000.00` in home region; core: ZF-3 allocation 6000.00 (JSON and SQLite) | None |
| Outcome | home | partly LO | `Stage:` token present in home region (stage value, closed and funding values not asserted); quality outcomes (`app.js:1277-1278`) not asserted at any level for the rendered list (ZF-2 has no quality row; ZF-3 never opened in browser) | Owner definition of "outcome" (stage/closed/quality assumed here); maintained assertion that a populated quality state appears only in its own home region |
| No same-building transfer | both | LO (criterion 3, preserved) | Browser: sibling tokens absent from `main` for ZF-2; core: sibling document and quality absent from ZF-2 links; two-store replay | None |
| Building version | building | IU | Rendered when present (`app.js:1283`); core asserts `building_record_version` 1 in a version event only | Optional |

## Role matrix

| Role | Observed here (maintained) | Not covered by a maintained check |
| --- | --- | --- |
| Retrofit Programme Manager (finance) | API 200 view, no `homes`; browser region split for ZF-2 | Cost values over HTTP |
| Resident Liaison Officer (non-finance) | Core only: `cost_allocation_restricted`, `costs_restricted`, JSON and SQLite | HTTP and browser rendering of "Restricted to authorised Finance roles" |
| Contractor | API 403 for view and version POST; core PermissionError | Browser (no screen access expected) |
| Anonymous | API 401 | None |

## Exact coverage gaps (reported, not repaired)

* G1 shared systems not asserted in either region.
* G2 own-home evidence documents and quality outcome never positively asserted in a maintained check; ZF-3 is never opened in the browser, so the per-home split on the same building is only observed for one home.
* G3 non-finance restricted-cost rendering has no HTTP or browser check.
* G4 HTTP checks assert no building or allocation amounts.
* G5 the screen lists every building item without displaying each item's `case_ids`/`package_ids` applicability; applicability enforcement is in `buildings.blockers`, not this view. Whether the criterion needs it displayed is an owner question.
* G6 region token containment proves listed tokens only, not that each category is its own labelled heading; the source does give each category an `h3`.

## Focused UI review of `homeCaseView` only (`app.js:1253-1297`, blob `c735acad...c80f`)

Guidelines source fetched fresh 2026-11-10 from the skill URL (retrieval complete, one request). Local Fluent 2, WCAG baseline, plain-language and ASCII conventions take precedence over generic Title Case, curly quote, ellipsis and `Intl` rules.

* `app.js:1264-1290` heading order h1, h2, h3 is hierarchical; both split panels are `section` with `aria-labelledby`; pass.
* `app.js:1258-1259` empty and unknown states handled with plain text; pass.
* `app.js:1295` error has `role="alert"` and a next step; pass.
* `app.js:1290` version timestamp `x.at` printed as stored (no `Intl.DateTimeFormat`); note only, ISO text kept by local ASCII/plain-language precedence; empty `at` or `reason` leaves double space.
* `app.js:1281`, `app.js:1288` amounts printed as server decimal strings, avoiding float rounding; note only.
* `app.js:1262`, `app.js:1276` long labels and identifiers have no wrapping or `translate="no"` in this component; the 320 px reflow passed only for the fixture's short values.
* No interactive controls other than two links; keyboard, focus and AT behaviour were not manually tested. Automated axe 4.10.3 zero violations is engineering evidence only, not conformance.

## Evidence classes

Everything above marked LO is constructed local fixture behaviour on JSON/SQLite stores. Not established: real customer or resident acceptance, human or AT review, live Azure or SQL Server behaviour, hosted CI for this head, independent review, human approval. Parent #73 and the durable-store epic remain open and are not asserted complete.

## Suggestion for Root

Literal criterion: dependencies, holds, works and costs (LO), decision and cost allocation (LO) hold in constructed local evidence for the finance role. Shared systems, own-home evidence and quality outcome, and non-finance rendering do not have maintained assertions, and "outcome" has no owner definition. A tick is therefore not recommended on this evidence alone; Root decides after independent review. Do not close #74.

> Correction 2026-11-10: the browser output in the Browser row above has 16 PASS lines plus one COMPLETE line, not 17 PASS lines; see [the qualified audit supplement](2026-11-10-issue-74-qualified-audit-matrix.md). The original text above is preserved.
