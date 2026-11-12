<!-- markdownlint-disable-file -->
# Admission amendment: issue 134 connected same-home check, slice S1 (2026-11-11)

Prospective amendment, committed before any source write or runtime. It does not edit, replace or relabel the earlier planning candidate, its original critique (verdict Revise, six findings, all applied) or its state.

* Task `134-connected-c5-1111`; parent `134-connected-plan-1111` (planning commit `9de98ff165c8121c0a12542a01222527e9ced870`)
* Branch `docs/demo-connected-walk-plan-134-1111`; last confirmed main `35eb0e559c7d0660ab87594732675b71be7bee67`
* Fetch of `origin/main` before this commit: unchanged at the same SHA, so no relevant source conflict and no integration needed.
* Source of admission: Root direction on 2026-11-11. This is an admission by Root recorded here, not an approval by this agent.

## Correction accounting (conservative)

* This is #134 correction C5 of the original five total. C1 to C4 stay spent.
* C5 covers the connected-check source, test and README implementation and its original final validation and one author Review. Zero corrections remain afterward.
* It is not a new five-cycle allowance and not a #233 grant. A later substantive reviewer correction needs separately reconciled authority and must not be relabelled as in-scope work.
* No second critique is run; the original critique stays the only critique.

## Owned paths

* New `src/api/checks/connected_home_browser_check.py`
* New `src/api/tests/test_connected_home_check.py`
* One short paragraph in `src/api/README.md`
* New dated tracking for this task (research addendum, plan, details, changes, review, state)

Nothing else is edited: no product, API, Store, role, manifest, workflow, prior probe, fixture module or register change; no knowledge base index or log edit unless a genuine need appears; the probe drift from the 14th screen is not repaired.

## Amendments to the earlier plan

| # | Earlier text | Admitted rule |
| --- | --- | --- |
| A1 | Details allowed copying the journey call sequence if the TestCase proved fragile | Use the delivered `StoreJourney` helper and deep-copy the real `store.data` before cleanup. If it cannot be reused safely, stop and return the exact blocker. Never copy or reimplement the business sequence. |
| A2 | `gap` allowed for a screen proven unable to render a Store field | A missing required marker, or a screen unable to show a required Store field, blocks S1 (non-zero exit, blocker recorded). Only explicit out-of-scope deferrals print `gap` or `not-run`. |
| A3 | Pure tests: a few helper cases | Pure regressions must fail for an empty or seed-only snapshot, a missing required marker, sibling leakage and wrong-home evidence. No tests of report labels or constants. |
| A4 | Distinctive sibling markers | Do not use shared generic markers (Accepted, design version 1, person names that may repeat across homes) as unique-home evidence. Scope each marker to its region, home and field or reference. Prove the negative control against distinguishable retained sibling data, not an empty page or a login failure. |
| A5 | Roles | Asset via Programme Manager is a proxy, not an Asset sign-in. All logins share one fixture state. No browser writes, approval, assistive-technology claim, eight-stage consistency or event-order screen acceptance. |
| A6 | Reuse | Confirm signatures and scoped focus behaviour of existing helpers before use. Carry the same home between the two menu screens with no reset. Run-only mutation negatives call the same production predicates. |
| A7 | Install prerequisite | Private HOME, TMP, cache, profile and scratch only. No real HOME, default dataset or `.env`. Install core, agents and api distributions (and the actual Playwright need) only after a recorded missing-import failure. Never install importer or orchestrator. No shared installs. |
| A8 | Preflight | Record exact interpreter, module and test-helper origins, Playwright and cached Chromium match, Node, and the existing pinned axe 4.10.3 (SHA-256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`). No refetch or install of browser or axe without new admission. A missing prerequisite stops the affected validation; it is never a skip that passes. |
| A9 | Browser run | Exactly one nonqueued `flock -n -E99 /tmp/ama-rpi-heavy.lock` with `timeout 900`, one final browser run, after targeted pure tests and static checks are stable. A held lock or missing prerequisite is a recorded blocker, not a queue or retry. A failed browser or test selector is not rerun without Root direction; independent selectors may continue. |
| A10 | Static validation | Run configured Ruff and format on affected files and the full relevant API typing (not only the new module). Run the unchanged core journey helper tests once to establish the factory contract, with selectors and module origins derived from source first (the earlier plan's cwd and module combination was wrong). No full API, core or importer suites; no full gate, images, SQL, provider, model or cloud. |
| A11 | Evidence | Record exact commands, counts, exits, skips and adverse outcomes outside the checkout. Web rules are fetched only if a web-oriented claim is made; there is no web UI edit, review or conformance claim here. |
| A12 | Delivery | One author Review after validation and complete Changes. No fabricated witness or retrospective review. No push, PR, issue or board write, no criterion tick, no closure of 134, 233 or 149. Return a clean frozen local candidate and the handoff to Root, who assesses the actual diff before publication. |

## Tier

Focused tier (new local check, pure test, one README paragraph; no workflow, manifest, Dockerfile, permission, secret, deployment or gate-semantics change). Any need to touch those, or an unresolved impact, escalates and stops for Root.

## Stop conditions (additions)

`origin/main` movement touching relevant source; `StoreJourney` not reusable; a required marker or Store field not renderable; lock held; prerequisite missing; any need for application change; any tempting pass or tick.
