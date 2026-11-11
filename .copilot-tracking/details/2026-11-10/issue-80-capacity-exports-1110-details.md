---
title: Issue 80 capacity page export controls, details
description: Phase details for the two Capacity page CSV anchors
ms.date: 2026-11-10
---

## Phase 1: UI change (`ops.js`, `capacityView`)

* Add a local helper after the `inp` helper:

```js
const exportLink = (path, file, label, what) => h("p", {}, h("a", { class: "btn alt", href: path, download: file }, label),
  ` The file has every ${what} you can see, not only the ones on this page. It is a read-only copy; changes in it are not imported back.`);
```

* In the `show(...)` call, after `h("h2", {}, "Packages")` add the conditional child `pkgPage.total ? exportLink("/api/packages.csv", "packages.csv", "Download all packages for Excel", "package") : null`.
* Inside the Work orders `section.card`, after `h("h2", {}, "Work orders")`, add the same conditional for `/api/workorders.csv`, `workorders.csv`, "Download all work orders for Excel", "work order".
* Use `cond ? link : null`, not `total && link` (a numeric 0 would render as text in `h`). See critique finding 1.
* Link text is the visible and accessible name; no ARIA, no new CSS (reuses `.btn alt`, which has hover, `:focus-visible` and a 2.5rem target).

## Phase 2: regression assertions (`capacity_browser_check.py`)

* In the seeded scenario after `capacity()` and the axe scan, add one small local helper `export_download(name, endpoint, expected_id)` that:
  * finds `a[download='<name>'][href='<endpoint>']`, expects exactly one visible link with the label text and the read-only sentence nearby;
  * focuses the link and presses Enter inside `page.expect_download()` (keyboard activation of a native anchor);
  * asserts `download.suggested_filename == name`, reads the saved bytes as UTF-8, parses with the `csv` module and asserts a header row plus the same number of data rows as `len()` of the unpaged JSON list from `context.request.get(base + endpoint-without-.csv)`, and that the seeded id appears;
  * asserts the page URL is unchanged and no new POST was made (`len(posts)` unchanged), so the control is read-only.
* In the `empty capacity` scenario assert both anchors have count 0 while the existing "No packages yet." and "No work orders yet." texts stay.
* Not asserted, disclosed: breadth beyond one page (seed has one package and one work order), 503/403/401 states (the view throws before render by construction and the existing scenarios cover the error text), screen-reader announcement.

## Phase 3: validation commands

1. `node --check src/api/src/zava_forward/api/web/ops.js`.
2. `ruff check` and `ruff format --check` on the changed check, only if the project configures them (check `pyproject`); use the owned venv or installed tool.
3. `python3 -m unittest tests.test_list_export_api -q` from `src/api` with the existing `PYTHONPATH` pattern.
4. `python3 -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` from `src/api` in the owned venv. The check takes `/tmp/ama-rpi-heavy.lock` itself with `LOCK_NB` and clears the environment except `PATH HOME TMPDIR LANG LD_LIBRARY_PATH`; it builds its own `tempfile` store, loopback ephemeral port. Do not wrap it in another `flock`. Record that the owned-data assertion is the check's own tempdir (no `ZF_DATA` is set because the store is constructed directly, not through the default data path).

## Phase 4: records

Changes record lists exact files and results; self-review is native and labelled not independent.
