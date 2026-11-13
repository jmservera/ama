<!-- markdownlint-disable-file -->
# Research: #74 home and building evidence integration (issue-74-evidence-integration-0424)

Date 2026-11-13. Research disposition: executed (read-only). Planning Readiness: Ready. Documentation-only integration of completed observations; no new validation campaign.

## Intake (verified, not trusted from the brief)

* Worktree `issue-74-evidence-integration-0424`, branch `docs/demo-home-building-evidence-74`, HEAD `6f2918011d55d63ffc52865073ef45bd7ea9197c`, tree `3d573c20311d43be2a1c6f3ef8601b638f8e4508` (equal to the frozen origin/main pin); status clean before work.
* Frozen sources read only: `issue-74-building-plan-0400` HEAD `232e09aa55effd4f8c0c40e292c1fe68b3c12e2c` (commits `5676f9025` plan, `74daa587e` V1 units, `232e09aa5` V2 mapping) and `issue-74-browser-0410` HEAD `b0c308c8fab63705d3464b9ca2140deb3ca7b34d` (commits `e8dec941d` home browser, `b0c308c8f` building observation). Both worktrees were clean and both diff against `6f2918011` only in `.copilot-tracking` (13 files each, tracking only; no product, test, check or config change).
* Imported byte-for-byte with `git checkout <head> -- .copilot-tracking`: only those 26 finite issue-74 files (research, plans and critiques, details, changes, reviews, rpi-sessions state).

## Raw outputs re-read (outside the repository, not copied)

* Units (`.../2cbb371d-.../74-unit-verification-0408/`): `core.log` `Ran 8 tests ... OK`; `api.log` `Ran 6 tests ... OK`; zero "skip" matches in either. `core-attempt1.log` (missing `zava_forward` package) and the byte-identical `api-attempt1.log` and `api-attempt2-invocation-error.log` (both `No module named 'test_home_case_api'`, a wrong-selector command error; distinct execution count unclaimed). Corrected 2026-11-13 after independent finding IR-001; the earlier text here grouped API attempt 1 with the missing package. The original text is superseded, see the correction amendment. These failures are preserved, not passes.
* Home browser (`.../b0e0aec9-.../74-browser-verification-0410/`): `run2.log` and `run-final.log` are byte-identical (`cmp`), 24 `PASS` lines, final `exit=0`; `run1.log` is the earlier missing-`playwright` failure.
* Building observation (`.../38e61c82-.../74-building-observation-0420/`): `observation.json` (building API status `[200]`, one h1, six h2 sections each count 1 and visible), `preflight.txt` (lock inode 77057, MemAvailable 5106268 KiB = 4.87 GiB, window 04:17:28Z to 04:17:32Z, `group_members_left=0`), `run.log` (`OBSERVATION RECORDED`, `exit=0`). `observe.py` is the superseded never-run draft.

## Chronology (as the records state it)

The unit and browser lanes overlapped in time, in separate worktrees. Commit times (UTC): `5676f9025` 04:00:58, `74daa587e` 04:06:51, `232e09aa5` 04:11:24 (V2 mapping, after the home run ended at 04:10:11), `e8dec941d` 04:11:38, `b0c308c8f` 04:17:58. The V2 mapping did not read the browser worker's files.

1. Planning freeze `5676f9025` (original prospective plan, one independent rubber-duck critique CR-001..CR-005, verdict Revise, applied).
2. V1 units executed in an owned venv: first core `ModuleNotFoundError: zava_forward` (API error files were wrong-selector errors), then editable install of core, agents and api, then 8 core and 6 API named tests pass (`74daa587e`). V2 documentary mapping `232e09aa5`.
3. Home browser: inherited prospective plan and critique reused; the browser plan file was written retrospectively (disclosed); run 1 failed `ModuleNotFoundError: playwright`, declared install, run 2 same command 24 PASS; lock held 04:09:42Z to 04:10:11Z.
4. Building observation: owner did not admit the V2-proposed check edit; narrower owned operational observation with its own prospective plan and one independent critique PC-001..PC-008 (Revise, PC-008 residual); one run 04:17:28Z to 04:17:32Z.

## Adverse and unchanged items to carry forward

CR-003 heading-count limitation (assertions count headings, not levels); building-observation residual PC-008 (harness port-release race, unchanged); axe tarball origin not evidenced beyond hash equality and axe ran on the `main` element of the home route only (not both routes, not full page); G5 / CR-001 home-panel per-item applicability (a ZF-2-only item also appears in ZF-3's building panel with no scope); CR-002 missing or null funding displays as no; CR-003 `buildingView` unobserved by the original author-reported 24 (the later single observation addresses only that one route); outcome tuple has no approved definition; AT and human acceptance not performed; source-history budget unknown (not zero, not exhausted). Self-review is not independent review.

## Gaps for the record

Unit and browser lanes run against different frozen heads but source unchanged from `6f2918011`; no combined test-suite count exists (14 units, 24 check lines and one observation are different instruments). Hosted CI and independent exact-head review not run for these observations.

## Placement

Existing [cut-over evidence pack](../../../docs/architecture/cutover-evidence-pack.md) takes one appended dated section; index row in `docs/reference/README.md`; append-only entry in `docs/reference/log.md`. No new knowledge-base page.
