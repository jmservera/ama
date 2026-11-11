<!-- markdownlint-disable-file -->
# Admission and Plan Amendment: issue 1420 source scope (2026-11-11)

* Additive. The original [research](../research/2026-11-10-issue-1420-choice-csv-research-1110-research.md), [plan](2026-11-10-issue-1420-choice-csv-research-1110-plan.md), [details](../details/2026-11-10-issue-1420-choice-csv-research-1110-details.md), [critique](critiques/2026-11-10-issue-1420-choice-csv-research-1110-plan-critique.md) and the genuine partial witness (launch, research-open, plan-done; verify exit 1) at `c50cfa2a8cbb47186db0a29eede9faf4882df421` stay unchanged. The original work was plan-only; no implementation or Review marker was fabricated.
* Source of admission: coordinator file `admission-1420-source-1111.md`, read in full. Synthetic local demonstration only; not actual-record export, privacy, retention, resident or production approval.
* Target: #1419 (via #1423) and the #80 integration are merged; the re-evaluated target is `main`, not the retired parent branch. Ordinary no-ff merge of fetched main into this topic is admitted; no rebase, amend, reset or force-push. Coordinator checkpoint reference: #1433 `8b21bdee` (assessed by the coordinator; not independently re-observed here).
* Blocking critique findings stay addressed: withhold uncontrolled text; missing or malformed evidence never becomes an absence, consent or readiness claim.

## Decisions (Q1 to Q6)

* Q1/Q2: scope free text and update due date excluded, as are all nested, contact, identity, address, purpose, owner, safe-route, adjustment, evidence, history and retention fields.
* Q3: one row per returned home, current portfolio page only, store order, repeated effective page and count columns. Header-only empty means no returned rows, not no open homes. A re-read at download can differ from the displayed snapshot, and the note says so. No all-pages export, filter, sidebar or per-home change.
* Q4: admitted files: new API serializer module and new test module; narrow `server.py` get-kind and dispatch; `role-screens.js` overview `summary(queue)` link and note; the existing screen-test assertion; the endpoint-inventory entry; API README and a narrowly affected existing resident-choice browser story where needed. Unchanged: core, shared serializer, `LIST_EXPORTS`, sidebar, per-home actions, roles, schemas, Capacity checker, unrelated handoff source and the merged #1419 registry and dispatch additions.
* Q5: display allowlist is the exact keys of checked-in `quality.CHECKLISTS` (Loft insulation, Wall insulation, Heat pump, Solar panels, General). Exact match only; no keyword, substring, alias or fuzzy match; an unrecognised label is never echoed and renders `Measure name withheld` (so `Cavity wall` is withheld). A display rule, not a domain-validity or approval rule.
* Q6: a Declined `Needs human review` is retained after a later Waiting with explicit review wording. Paused, withdrawn and latest-versus-current version, revision and design distinctions stay. Missing or invalid status is `Unknown`; `Not recorded` only when the existing projection supplies it. Incomplete evidence never becomes `None recorded`.

## Exact contract

* Route `GET /api/resident/choice-queue.csv`; filename `resident-choice-queue-page.csv`; `text/csv; charset=utf-8`, attachment.
* Same JSON queue roles and query parsing, no widening; JSON errors (including loader failure) without `Content-Disposition` or CSV.
* Ordered header, exactly eight columns:
  1. Home reference
  2. Measure choices (latest recorded version)
  3. Paused, withdrawn or retained human review
  4. Update commitment status
  5. Homes skipped before this page
  6. Page size limit
  7. Homes in this file
  8. Open homes in total
* Local stable-header empty serialization; primitive safe cells only through the shared `safe_cell`.
* UI: plain attachment anchor, no `download` attribute, adjacent truthful current-page note, no link in the blocked or failed state.

## Guardrails and budget

* Validation focused only; no full API, Core or gate run. One bounded Chromium observation with the existing harness if possible. No real, private or default dataset, provider, cloud, SQL, Docker, deployment or new issue. Initial #1420 implementation with its own finite correction budget (default five); no borrowed budget.
* Before any source edit: record current main and source pins, prove own #1420 changes versus inherited parent `12d3ac842` are tracking-only, and after the merge prove `src`, `infra`, `tools` and `.github` equal current main. A tracking or evidence conflict, or unexpected resident projection, role or query change, stops for the coordinator.
* Result is a clean local candidate for independent exact-head review; no push, PR, issue or board write; whole #80 and #73 and live, privacy, retention and human acceptance stay separate.
