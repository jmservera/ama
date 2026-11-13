<!-- markdownlint-disable-file -->
# Research: #74 home-case browser verification V1 slice (issue-74-browser-verification-0410)

Date 2026-11-13. Branch test/demo-home-browser-74-0410 from freshly fetched origin/main. Head and origin/main at start: 6f2918011d55d63ffc52865073ef45bd7ea9197c, tree 3d573c20311d43be2a1c6f3ef8601b638f8e4508. Disposition: reused (existing prospective Research executed) plus a bounded source read of the check. Continues task `issue-74-building-separation-0400`, follow-up rank 1 (V1), browser portion only.

## Reuse provenance

Prospective commit `5676f90251f069f63be18147426674b791683aac` (branch `research/demo-building-separation-74-0400`), read through Git objects only, not checked out:

| Artifact | Blob |
| --- | --- |
| research | bc5156ab2657a71f5f8839e90424dfe5b7a256a5 |
| plan | 1da3f33cfb78861c90e62ae96095f6cc323c616a |
| details | cf783f754a76bb03c3eacce3624e9a7aa94daf4f |
| critique (one independent execution, verdict Revise, CR-001..CR-005 applied) | 75ecdcdf0fca588fd6bccaf84bd74f8fa4b34896 |
| state | read; Review conformant with limits, V1 rank 1 |

The critique is reused and not repeated. Research and plan were read for scope (details V1, validation table); the full research body was read only to its first 3500 characters, so later sections are relied on only as quoted in plan and critique.

## Source equivalence and currency

* `git rev-parse 5676f9025^` equals this head 6f2918011d55d63ffc52865073ef45bd7ea9197c; `git merge-base` equals the same; zero commits between the prospective commit and this head.
* `git diff --stat 5676f9025 HEAD` over `src/api/checks/home_case_browser_check.py`, `src/api/checks/design_system_browser_check.py`, `src/core/tests/building_fixture.py`, `src/api/src`, `src/core/src` is empty. The prospective source reading is therefore equivalent to this head for the executed check.
* origin/main was fetched immediately before work and still equals 6f2918011 at start.

## Check source facts (read at this head)

* Component guide: `src/api/README.md` line 4422 prescribes `python -m checks.home_case_browser_check` from `src/api` with `ZF_AXE_JS` set to pinned axe 4.10.3.
* The check delegates to `design_system_browser_check.main`, which writes the synthetic fixture (`building_fixture.fixture()` plus local additions: two fictional homes ZF-2 and ZF-3) into a `tempfile.TemporaryDirectory` under `ZF_BROWSER_SCRATCH` (must be absolute and outside the checkout), binds an ephemeral 127.0.0.1 port, sets `ZF_DATA` and `ZF_STATE` to that directory, `ZF_STORE=json`, a synthetic password, `ZF_BIND=127.0.0.1`, `ZF_AUTH=password`, and passes only PATH, HOME, LANG and bytecode variables from the caller. Fixture isolation is proven from source; no private dataset or default `~/.zava-forward` path is referenced, and no model or provider variable is passed.
* The server child is terminated and waited in a `finally`; the browser is closed in a `finally`.
* The check opens only `#/case-home/ZF-2` and `#/case-home/ZF-3`. It does not open `#/building/<id>` (`buildingView`).
* axe is applied only when `ZF_AXE_JS` is set and its SHA-256 equals `880970c0...8bb`, run with tags wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa on the `main` element only.

## Pinned prerequisites found

* axe 4.10.3: cached package `axe-core-4.10.3.tgz` (SHA-256 0f2b4d7dcdf7d1219df8d1959ad68e565f51d14c3f0d88bb71cd59abeb956292) held in a pre-existing owner-owned temporary directory; its `package/axe.min.js` has SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb, equal to the check's `AXE_SHA256`. A copy was placed in the owned evidence directory; the source file was not modified. The tarball's own provenance (download source) is not evidenced here.
* Chromium: the existing Playwright cache `chromium-1248` (Chrome for Testing 156.0.8078.4, binary SHA-256 377a9fc07b495c3b8d0ab8ec1fdfd153641759f9756fea34d8dfce4de82f5025), used read-only through `PLAYWRIGHT_BROWSERS_PATH`. No browser was downloaded.
* Playwright: `src/api/pyproject.toml` dev extra declares `playwright==1.64.0`.

## Read limits

Not read: other browser checks, #74 issue comments, the full prospective research body, PRD/BRD. No logs, `.env`, SQL or private dataset read. The unit worker's environment was not read or written.
