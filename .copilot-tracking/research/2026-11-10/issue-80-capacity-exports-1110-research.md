---
title: Issue 80 capacity page export controls, research
description: Source contract research for two contextual CSV download anchors on the Capacity page (issue 80 criterion 2, bounded source increment)
ms.date: 2026-11-10
---

## Scope and disposition

* Task: `issue-80-capacity-exports-1110`, parent `issue-80-entrypoint-followup-1110`. Research disposition: `executed` (source reading only; no new runtime observation is needed or admitted).
* Root admission: one source increment of exactly two contextual anchors. Not admitted: progress-variant change, more observations of the three missed stages, API/core/permission/serializer/store/route/default/filter change.
* Evidence boundary: the parent follow-up run (commit `00ad79a9`, pin `583d4fbd`) observed, for synthetic `pam` in a populated fixture, that `#/capacity` rendered Packages and Work orders with no download control and that direct GET of both CSV routes returned 200 `text/csv`. That is bounded scenario evidence, not universal UI absence and not every-list proof. Three driver stages timed out (cause undetermined) and stay unobserved.
* Preparation baseline: ordinary merge of `origin/main` `6d4cd624` into `00ad79a9` gives `181da535`. The delta `00ad79a9..6d4cd624` touches only `.copilot-tracking/` and `docs/reference/` paths; no `src/`, `infra/`, `tools/` or `.github/` path. The web source files are unchanged by it.

## Web guideline and precedence retrieval (before any web edit)

* Skill `web-design-guidelines` loaded. Source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` fetched raw on 2026-11-10 in one call, complete (the response was not truncated; it ends with the Output Format section).
* Applicable installed skills selected: `web-design-guidelines` only. `design-taste-frontend` is for public pages, not app screens, so it is not applied. No redesign skill applies; this adds two native links.
* Precedence read: [design system](../../../docs/reference/research/ux/design-system.md) (owner-selected Fluent 2, native semantics, non-colour signals, visible focus, `.btn alt` and `.row` helpers, state belongs to the enclosing request), [WCAG baseline](../../../docs/reference/research/ux/wcag-conformance-baseline.md) (headings, target size, keyboard row; no conformance claim) and [content standard](../../../docs/reference/research/ux/content-standard.md) (plain words, active voice, ASCII punctuation, name the actor). The fetched Vercel rules yield to these where they conflict (for example Title Case buttons: the project uses sentence-case "Download for Excel").
* Rules that bear on the change: anchors for navigation/downloads, not `div onClick`; specific labels (accessible name equals visible text); headings stay hierarchical; empty states must not render broken UI; no `transition: all`, no new focus suppression. The existing `.btn` rules already supply `:focus-visible`, hover and 2.5rem target size.

## Source contract at the pin (commit `181da535`)

* Page: `capacityView` in `src/api/src/zava_forward/api/web/ops.js`. It returns "Only a manager sees capacity and work orders." unless `isManager()` (`app.js`: Retrofit Programme Manager or Programme Support Officer). It loads `GET /api/packages?limit=&offset=` and `GET /api/workorders?limit=&offset=` (paged, `{items,total}`); a load failure throws before any render and shows the existing error plus "Try again".
* Render: `h2 "Packages"` then `pagerControls`, then package cards or "No packages yet."; a `section.card` with `h2 "Work orders"` then `pagerControls`, then a list or "No work orders yet.".
* Export routes: `server.py` `LIST_EXPORTS` includes `/api/packages.csv` and `/api/workorders.csv`. The handler checks `projection.allowed(u, kind)` (both are in `STAFF_GET`; a Contractor gets 403) and then `list_rows`, which calls `s.list_packages(u)` and `s.list_work_orders(u, case)` with no limit, so the CSV is every record the store returns for that user, unpaged, with `Content-Disposition: attachment; filename="packages.csv"` or `"workorders.csv"`. The `case` query selector is not set by the page. Rows are produced by `list_export.to_csv` (existing serializer, formula neutralised per `test_formula_text_is_neutralised`).
* One-way: the exports are GET only; `test_export_is_read_only` exists. No import route exists for these lists.
* Existing link pattern to follow: `ops.js:246` and `panels.js:575`: `h("p", {}, h("a", { class: "btn alt", href, download }, "Download for Excel"), " The file is a read-only copy; changes in it are not imported back.")`.

## Design findings that shape the change

* Breadth: the page is paged (default page size from `CAPACITY_PAGE`), the CSV is not. The label must say the file holds every package or work order the person can see, not the current page.
* Two identical "Download for Excel" links on one page would have the same accessible name in the links list. Use specific visible text, "Download all packages for Excel" and "Download all work orders for Excel", so the visible label and the accessible name match (WCAG 2.5.3 label in name) with no extra ARIA.
* Withhold when misleading: a zero total means the file would hold only a header row, so show no anchor (the existing "No packages yet." text remains). On a load failure the view never reaches the render, so no anchor is shown. The decision uses the response `total`, the same value the pager uses.
* Not a role grant: the page stays manager-only; no role change.
* Fixed hrefs: do not append the current page or a `case` filter, so the link cannot imply page parity.

## Existing checks selected (focused tier)

* `src/api/tests/test_list_export_api.py`: existing API tests for the two routes (registry, role limits, CSV vs JSON rows, formula text, read-only).
* `src/api/checks/capacity_browser_check.py`: existing browser check with the seeded synthetic store (`PKG-SYN-001`, `WO-SYN-0001`), an `empty capacity` scenario, loopback ephemeral port, scrubbed environment, and its own non-blocking `flock` on `/tmp/ama-rpi-heavy.lock` (BLOCKED on busy). It therefore must not be wrapped in another `flock` of the same file. Its `capacity()` helper and the empty scenario are the places to assert the two anchors.
* Static: `node --check` for changed JS; `ruff` for the changed check if the project configures it.

## Unknowns and limits

* No rendered-layout, screen-reader or user-acceptance evidence. A synthetic Chromium check proves DOM, a real download and its bytes for one seeded fixture; it does not prove deployed behaviour, assistive technology or acceptance.
* Every-list criterion remains UNPROVEN; progress variant, the other registers and owner thresholds remain open and out of scope.

## Planning Readiness

Ready. No unresolved dependency.
