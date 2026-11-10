# Profile-main checkpoint research (issue 440, 2026-11-10)

Task: `profile-main-440-1110`. Parent: `aftercare-main-440-1110`. Research disposition: executed (read-only git, read-only GitHub and Root session file reads). Planning Readiness: Ready.

## Trigger and scope

* PR 1414 `test: add bounded specialist keyboard and evidence probe` (issue 134 child, `Refs` only, no closing references) is MERGED 2026-11-10T17:58:44Z as `main` `b23c08e33e4ebdb0aaa1dfd8fa586999448d8ca6`, tree `0bdc704b78b9a3ed95926b5915ae93ae9148032d`. PR head `124af0b63b727d3d8889d6900a0bca7d6b70578c`. All 19 PR-head checks read SUCCESS; Source projects CI run 42867523237 and Capstone Rubric Scorer run 42867523337 both completed success on that head. The earlier 77/78 hosted B6 failure (run 42864188813) is preserved as an adverse record. This is a PR-head observation, not a main-head result: the scorer run on `b23c08e33` was still in progress when read.
* A child merge is not whole journey acceptance. This checkpoint records scoped current-main integration before any closure or dependent expansion of #134, #73 or #440. The independent #108 and #184 lanes may run read-only metadata work with no functional dependency. This is not a source repair cycle, reset, new QA campaign, cloud, transport or model budget; the existing #134 correction counter (C4 spent, five total, one left) is untouched.
* Local `origin/main` read after `git fetch`: `b23c08e33e4ebdb0aaa1dfd8fa586999448d8ca6`, equal to this worktree base and HEAD at launch. Topic branch `docs/profile-main-checkpoint-440-1110`, clean at launch.

## Source identity (read 2026-11-10)

| Item | Identity |
| --- | --- |
| Probe `src/api/checks/specialist_keyboard_browser_check.py` | `e8b7d9f16200896373c86d6b31d728c0d773c28a` |
| Probe test `src/api/tests/test_specialist_keyboard_check.py` | `228a5390221b64d9ffb0bd3ecb286308a5e50c7d` |
| `src/core/src/zava_forward/core/journey_acceptance.py` | `e3466b6eafc07d319ce3f2ee835d832b58f34032` |
| `src/core/src/zava_forward/core/perspective_walkthroughs.py` | `f1828b2eb805078421731170c91a3218cc56a411` |
| Trees at `b23c08e33` | `src` `901a74c62a8b980b3cbe0b925db2e69f00003a91`, `src/api` `ed94d555101aa9b1be04be32787576a3bbb46960`, `src/core` `0d3caa315d9194e2551de5a95b0d76a75958dd5d`, `infra` `f7f31c0934cfe0bafb4505408706e55aa8ab61e7` |

The four blobs equal those validated in C2 at `cb01c33c42ceef31ee699649ecceedadc487945d` (direct `git rev-parse` comparison). `git diff --name-only cb01c33c42 b23c08e33` outside `.copilot-tracking` lists only `.github/rubric/scores/latest.json`, `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md` and `src/api/README.md`; the only `src` change is the C4 README rewrite. C3 and C4 therefore changed README and RPI files only.

## Documents (blob at `b23c08e33`)

| Document | Revision and status |
| --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md` | BRD 0.21.0, `draft`, blob `34d88395de861e9799eb9e24121a21c92c7a5adc`. Its AC-034 is a Finance grant-reconciliation criterion, not the PRD AC-034 |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | PRD 0.21.0, `in-review`, `exercise_status` author-complete-unsigned-pending-review-and-owner-acceptance, blob `c788b917bafaede215f326f0efc71e071a687f1c`. PRD AC-034 to AC-043 (lines 2130 to 2139) and the slice check table (lines 2251 to 2260) |
| `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md` | Accepted with amendment by the project owner 2026-10-15, blob `d60645397b20fb70ac3d1dc47c7a6c8671201306` |
| `docs/adrs/0006-src-layout-and-cutover.md` | Accepted 2026-10-15, blob `956da1a3b804c803041fe2e8a312bd9f400273ae` |

Draft and in-review are not approval; nothing here approves a requirement or decision.

## Bounded probe to partial journey requirements

`journey_acceptance.REGISTER` records PRD AC-034 to AC-043 as `partial` (AC-034, AC-037, AC-039, AC-040, AC-042, AC-043) or `deferred` (AC-035, AC-036, AC-038, AC-041) with no `passed`. The keyboard probe is named evidence only for AC-034 (constructed-fixture keyboard reach, focus visibility and DOM status text for the first listed home) and informs AC-036 only as text presence of owner or next-action wording, not label agreement. `perspective_walkthroughs.py` records eleven perspectives with five elements each and zero elements met.

## Retained historical observations (not re-run as new proof)

Root session files under `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/`:

* `134-keyboard-c2-evidence-1110/` (`api-static-unit.log`, `core-static-unit.log`, `probe-run1.log`) and `handoff-134-keyboard-c2-1110.md`: C2 on `cb01c33c`: API helper tests 6 OK, Core 16 OK, one browser run exit 0 with 714 PASS, 15 negatives and 15 declared no-table walks. HISTORICAL.
* `handoff-134-keyboard-c4-1110.md` and `phase134-keyboard-c4-evidence-1110/`: C4 canonical seven witness events, verify exit 0 with disclosed timing notes. The response to the hosted B6 failure was a README rewrite only.
* Older C1 and C2 and original chains keep their failed or qualified outcomes; not waived.

## Currently active neighbouring facts (do not duplicate)

Sensor and Quality facts below are coordinator-supplied and not re-read here; only the issue states were read live.

* Sensor C2 PR 1412 is MERGED as `0da7b8573`; its current 179c23 chain is canonical with seven ok records and verify 0, independent Readiness 0. Older 806 and c218 chains stay qualified. Quality 1331 (merged `1b7a1719`) and Quality-main 1336 (merged `3bc20719`, 2026-11-09) are already recorded; no Quality checkpoint or live call is repeated.
* #134 OPEN (`status:not-started`), #73 OPEN (`status:partially-delivered`), #440 OPEN (`status:partially-delivered`), #108 and #184 OPEN (`status:partially-delivered`). Nothing is ticked or closed here.

## Local tooling and admission (read before the run)

* Python 3.12.3. Playwright Chromium cache exists at `~/.cache/ms-playwright` (`chromium-1248`, `chromium_headless_shell-1248`). `/tmp/ama-rpi-heavy.lock` exists; `fuser` reported no holder at research time. Memory was tight (about 2.8 GB available of 16 GB); admission is rechecked at run time.
* No private environment exists for this worktree. Other worktrees' editable installs are not reusable as source proof. The plan is to try the existing selectors first, record any actual missing-dependency failure, and only then restore dependencies into a private environment outside the repository from this worktree's `src` packages. No browser install and no global install.
* The existing probe is `python -m checks.specialist_keyboard_browser_check` from `src/api` with short `ZF_BROWSER_SCRATCH`, under non-queued admission (`flock -n /tmp/ama-rpi-heavy.lock`) per the `src/README.md` guidance (`--lock-timeout 0`, check the actual holder).

## Planning readiness

Ready. Planned scope: one dated section in `docs/architecture/cutover-evidence-pack.md`; own RPI files only. Out of scope: any shared knowledge base file (`docs/reference/README.md`, `log.md`), source, tests, probe, manifest, infra, tools, workflow or rubric; Azure, live, IoT, SQL, model or private data; image builds; gates or `--changed`.
