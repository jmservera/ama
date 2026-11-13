<!-- markdownlint-disable-file -->
# Independent readiness review: #74 home and building evidence candidate (issue-74-evidence-review-0435)

Date 2026-11-13. Fresh-context, read-only documentation review by Claude Sonnet 5.5 (model label asserted, no host attestation). Not the author's Review, not a human approval, no correction authority, no publication approval.

## Research and plan (bounded)

* Research: read the whole diff, the 36 paths, the frozen blobs of `232e09aa5` and `b0c308c8f`, and the safe raw outputs named in the brief (unit logs, home `run1/run2/run-final`, building `observation.json`, `preflight.txt`, `run.log`). No `.env`, private data, SQL logs or native 149 AI log read.
* Plan: identity and cleanliness, byte-for-byte preservation, claim-by-claim comparison of the pack section to artifacts and raw outputs, links and anchors, append-only log, scope. No test, browser, SQL, Docker, install, cloud or provider call.

## Identity (before and after, unchanged and clean)

* Candidate `1d105e37fef55001b45f922fbd2bfdd3c4973ce6`, tree `799f88127297cd540977eceaf3c56c9e59de5314`, branch `review/demo-home-building-evidence-74-0435`, merge-base and reviewed base `6f2918011d55d63ffc52865073ef45bd7ea9197c` (tree `3d573c20311d43be2a1c6f3ef8601b638f8e4508`). `git status --short` empty before and after; author worktree `issue-74-evidence-integration-0424` status empty, not written.
* Diff 36 files, 976 insertions, 1 deletion (the README `ms.date` line). No file outside `.copilot-tracking`, `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Verdict: REVISE (narrow). No Blocked condition; no High finding.

### Findings

| ID | Severity | Location | Finding |
| --- | --- | --- | --- |
| IR-001 | Medium | `docs/architecture/cutover-evidence-pack.md:7938`; same claim inherited at `.copilot-tracking/research/2026-11-13/issue-74-evidence-integration-0424-research.md:14` and `:23`, and in the original `.copilot-tracking/changes/2026-11-13/issue-74-building-separation-0400-v1-unit-changes.md:16` | The pack says "core and API attempt 1" failed `ModuleNotFoundError: zava_forward`. The raw `api-attempt1.log` (04:05:32Z, before the pip install ended 04:05:46Z) is byte-identical (`cmp`) to `api-attempt2-invocation-error.log` (04:05:55Z, after install) and both show `No module named 'test_home_case_api'`, the selector error. Only `core-attempt1.log` shows the missing `zava_forward`. So the API had two selector errors and no evidenced missing-package failure, and "a later first API invocation" is garbled. The author re-read the logs and did not detect it; the original record is the source of the error. Correction: state core attempt 1 missing package; API attempts 1 and 2 both wrong selector, identical logs; the dependency install is evidenced by the core failure only; leave the preserved original files unedited and add the qualification in the pack. The 8 and 6 passes and zero skips are unaffected (`core.log` Ran 8 OK, `api.log` Ran 6 OK, no "skip"). |
| IR-002 | Low | `.copilot-tracking/plans/2026-11-13/issue-74-building-observation-0420-plan.md:12-14` | Original observation plan phases stay unchecked after execution (original, preserved; not altered). The pack could note the plan is prospective and unreconciled. Optional. |
| IR-003 | Low | pack `:7927` | "Maintained regression check" is accurate, but axe scope (ZF-2 `main` only, confirmed at `home_case_browser_check.py:152` before the ZF-3 navigation at `:161`) is stated only in Limits (`:7950`); acceptable, no change needed beyond optional proximity. |

No Medium or High finding on current-source qualification, counts, or scope.

### Verified (performed)

* Preservation: all 26 original files have identical git blob IDs at `HEAD` and at `232e09aa5` (13) and `b0c308c8f` (13). Both frozen heads differ from the pin only by added `.copilot-tracking` files (no non-tracking path). Commit times 04:00:58, 04:06:51, 04:11:24, 04:11:38, 04:17:58 UTC match the pack. This proves preserved bytes, not that those runs succeeded; success was assessed separately from raw logs.
* Counts: unit 8 and 6 OK, zero skips. Home: `run2.log` equals `run-final.log` (`cmp`), 24 `^PASS`, 0 FAIL, 0 skip, `exit=0`; run1 `ModuleNotFoundError: playwright`; the pack's 1 server + 23 browser/axe split matches the assertion list. Building: API `[200]`, h1 1, six h2 each count 1 visible, markers as stated, home-only sentinels true on home and false in building main, sibling sentinels false on home (so correctly described as proving nothing), controls 0, non-safe 0, foreign 0, JS errors 0, lock 04:17:28Z to 04:17:32Z, 4.87 GiB, `group_members_left=0`.
* Qualifications: self-reviews labelled; browser plan file retrospective disclosed; inherited prospective plan and critique; no criterion tick, closure, whole 74/440, WCAG, AT, outcome, production or live claim; no summed count; no raw bundle copied; G5, CR-002, outcome, AT, human acceptance, unknown source history stated open, with the authority-research conclusions not used. The model label in the integration review is an asserted label.
* Links and anchors: every added relative link in the three docs resolves; the README and log anchor equals the slug of the new heading (`...-2026-11-13-refs-74-440`, line 7907); added lines ASCII; `git diff --check` clean. Log change is append-only (6 added lines at the end, no earlier line changed). README change is one row and the `ms.date` bump.

### Not performed

Documentation tests such as `tests.test_live_doc_links`, `rpi-checks`, hosted CI, any browser/unit/SQL run, re-execution of raw logs, reading the author-private raw `venv` or `observe.py`; review of source history/authority. Pack lines 7907-7963 were read in full; the 36-path ledger below is complete. Process-snapshot and cleanup claims rely on the records and `preflight.txt`/`scratch-after.txt` only.

## Read ledger (36 paths, all read)

Docs: `docs/architecture/cutover-evidence-pack.md` (added section), `docs/reference/README.md`, `docs/reference/log.md`.
Original unit lane (13): building-separation-0400 research, plan, critique, details, changes, v1-unit-changes, v2-mapping-changes, review, v1-unit-review, v2-mapping-review, and the three state files (`-0400`, `-v1-unit`, `-v2-mapping`; the state files were parsed for mode, phase, status and blockers only).
Original browser lane (13): browser-verification-0410 research, plan, details, changes, review, state; building-observation-0420 research, plan, critique, details, changes, review, state.
Integration (7): evidence-integration-0424 research, plan, critique, details, changes, review, state.
All 36 were read; original plan and research lines were skimmed truncated at 600 characters per line, so long table cells (for example the G5 row) were not read to their end.

## Routing

Author-owned correction of IR-001 in the pack and integration research (not applied here); then re-review of only the changed lines. Publication, hosted CI, human approval and merge remain with the owner.
