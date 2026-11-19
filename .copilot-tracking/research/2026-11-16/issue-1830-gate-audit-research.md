---
title: Research for issue 1830 full-gate critical path and targeted preflight
ms.date: 2026-11-16
---

## Scope

Issue #1830: measure the local full-gate critical path and design a change-specific preflight that is never a receipt. Branch `ci/gate-preflight-benchmark-1830`, base `main` 18d3de459f20018e91fab3af87ab0d89123661c6, clean worktree `/home/azureuser/source/ama-wt/issue-1830-gate-preflight`. Staged handoff: Research and Plan only. Implement and Review are deferred because #1297 modifies `tools/rpi-checks.py` and `src/README.md` and has not merged. This is not a completed issue and not a publication candidate.

## Research disposition

`executed` (direct inspection, no heavy gate run, no cloud, no paid model). The opening stub was persisted before the `research-open` witness (seq 2) and this file replaced it with the findings. Planning Readiness: `Ready` for the standalone helper, the timing analyzer and the method document. Planning Readiness: `Blocked` (dependency on #1297) for any edit to `tools/rpi-checks.py` or `src/README.md`.

## Sources read

* Issue #1830, #1297 and #1828 (`gh issue view`), PR #1829 (open; head `3a7c655603eeae861c476eca1268a0188efde9bc`, read through `gh` only).
* `.github/copilot-instructions.md`, `.github/agents/ama-backlog-delivery-coordinator.agent.md` (Step 5 phase-witness rules), and the repository starting documents `docs/case_study_48_original.md` and `docs/case_study_48_addendum.md`. This issue changes no problem specification, so none of them is edited.
* `src/README.md` "Local RPI gate" (lines 62-143), "Gate speed controls (issue #470)" (line 280) and "Measuring full-gate scheduling" (line 365 onward, including the 2026-11-02 attempts table).
* `tools/rpi-checks.py` at base: `dependencies` (707), `changed_groups` (723), `test_paths` (891), `extra_selector` (1540), `browser` (2382), `sql` (2481 onward), `dispatch` (2731), `schedule` (2771), `heavy_lock` (3226); `tools/ci-affected.py` and `.github/workflows/src-ci.yml` for hosted coverage.
* One receipt: `<gate-output>/receipt.json` (sha256 `9852ce3f...05e51`, equal to its `receipt.sha256`), its `0000..0216-*.log` command logs and `<gate-output>.log`. No other receipt was read: `<gate-output>` has no `receipt.json` and belongs to the active #1297 lane, so it was left alone.

## Gate structure (what the receipt can and cannot prove)

* Schema 4, scope `full`, `--jobs 2`, `image_cache: fresh`, 17 required groups, 217 commands, head `132f0b1ca1a229556f7c48a5b9e64f63a556f5de`, base and merge base `18d3de459f20018e91fab3af87ab0d89123661c6`, status `passed`, sealed 2026-11-16T16:14:17.9Z.
* The scheduler runs at most `--jobs` groups at a time. Edges (`dependencies`, `schedule`): `static`, `infra`, `migration`, `logo-0600` and every `image-*` need `namespace`; `browser` and `mssql` need `project-api`; `project-api -> browser -> mssql` and `static -> infra -> migration` are forced chains because they share one environment; images wait for `infra` and `migration`; `mssql`, images and `logo-0600` share one docker lock. Groups are dispatched in `required_groups` order, never by expected duration.
* The receipt records no host CPU, memory, load or queue data. Host comparability therefore has to be recorded outside the receipt.

## Measured observations (one receipt, descriptive only)

Window arithmetic: command span 2732.9 s (first command start to last finish). The runner log shows `Lock queued 15:28:29.546` and `acquired 15:28:29.547`, so lock queue wait was about 1 ms. Lock acquired to `sealed` was 2748.4 s, so 15.5 s fell outside command spans (4.3 s before the first command, 11.2 s after the last). Group durations overlap and must not be summed.

Test counts and unittest-reported times (retained logs):

| Suite | Tests | Reported time |
| --- | --- | --- |
| core discovery | 3526 | 1298.6 s |
| API shard 1 / 2 / 3 | 1234 / 1056 / 1412 | 795.5 / 735.6 / 950.3 s |
| agents | 484 | 147.9 s |
| infra | 677 | 188.4 s |
| SQL (`test_mssqlstore` set / sensor / staff intake) | 334 / 10 / 63 | 531.8 / 3.8 / 144.1 s |
| orchestrator / importer / static | 142 / 121 / 108 | 21.6 / 16.1 / 27.0 s |

Critical path by timestamp (seconds from first command), obtained by following what each group waited on:

| Segment | Start | End | Duration | Cause |
| --- | --- | --- | --- | --- |
| Serial environment setup (6 venvs, pip installs, namespace import checks, Playwright download) | 0 | 194 | 194 | no test runs until every environment exists; one command at a time |
| `project-api` waits for a worker slot (tests, not setup) | 194 | 348 | 154 | `core` and `agents` hold both slots at `--jobs 2`; the API venv was ready at 106 s |
| `project-api` three shards, then ruff and mypy | 348 | 1314 | 966 | longest shard 954 s (ends 1303); shards end 1088, 1148, 1303; API `mypy` 11 s ends the group at 1314 |
| `browser` waits for a worker slot | 1314 | 1509 | 195 | prerequisite met, but orchestrator, importer, static and infra took the free slot while `core` held the other until 1509 |
| `browser` | 1509 | 1731 | 222 | longest command 103 s |
| `mssql` | 1731 | 2436 | 705 | 533 s plus 145 s suites; waits for browser because both mutate the API venv |
| four fresh image builds, scans and checks | 2436 | 2717 | 281 | serial under the docker lock |
| `logo-0600` | 2717 | 2733 | 16 | |

The segments add to the 2733 s span. `project-core` (ends 1509 s; 1307 s command) is the longest single command but is not itself the critical chain: it delays the end only by holding a slot that the browser group was waiting for.

Concurrency histogram of command overlap: exactly four commands for 740 s (core plus three API shards on a machine that admitted `--jobs 2`), two for 765 s, three for 60 s and one or none for 1167 s (42.7 %). Two single-command stretches dominate: the 194 s setup prelude and the 961 s tail from 1772 s to 2733 s (`mssql` then images). The tail is policy-bound: the README states that one heavy lock, one owned SQL container and serial image builds and scans stay in force.

Mandatory cost versus setup: summed `pip`, `venv`, `playwright install` and `docker build` command time is about 450 s of 5,657 s total summed command time (the 5,657 s is overlap-inflated and is used only as a ratio base). Fresh `--no-cache` image builds are 52, 39, 42 and 38 s, plus checks and Trivy 15 to 30 s each. These are mandatory by the full-tier policy (`image_cache: fresh`, Trivy per image).

## Evidence-backed optimization hypotheses (not conclusions)

None is applied. Each needs a controlled A/B on a comparable host with the benchmark method in the plan. Upper bounds come from this single receipt and ignore CPU contention, which is real when four suites run at once.

* H1 queue wait for `browser`: up to 195 s (7.1 %) if the scheduler preferred groups on the longest remaining chain (`project-api -> browser -> mssql -> images`) over short independent groups. Coverage is unchanged.
* H2 late API start: up to 154 s (5.6 %); the 242 s gap between the API venv being ready (106 s) and shards starting (348 s) is the H2 plus H3 range if the slowest chain started first instead of in list order. H1 and H2 overlap and are not additive.
* H3 setup prelude: the API environment was ready at 106 s but API tests began at 348 s; overlapping environment builds with test execution could save up to 242 s on this chain. It changes runner scheduling semantics.
* H4 shard balance: shards are balanced by git blob size, not duration. Per-test cost differs by 0.64 to 0.70 s, and shard time ranged 735 to 950 s against a mean of 827 s. An upper bound of about 123 s exists only if durations can be balanced with the same coverage.
* H5 SQL and images (about 986 s, 36 %): not candidates without owner policy, because they are the required real-SQL and fresh-image controls.
* Combined H1 to H3 upper bound is about 450 s (16 %): with no slot waits the chain `setup -> api -> browser -> mssql -> images` is about 2296 s (106 + 966 + 222 + 705 + 281 + 16) and `core` (ends 1509 s) is off it. Treat this as a hypothesis, not a forecast.
* Redundancy: no coverage duplicate was found. Repeated work is small: two `pip install --require-hashes -r src/api/requirements.txt` runs (3 s and 2 s), a second `playwright install chromium` (1 s), and editable `src/core` installs per project. The single-test `test_chat_panel` browser selector (3 s) is intentional because discovery skips it without `ZF_BROWSER_TESTS=1`. Mandatory groups: all 17 required groups, SQL, browser/axe, scanners, fresh images, clean-input guards.

Comparability limits: the README's 2026-11-02 attempts (core 443 s command time at `--jobs 1`, the AMD EPYC 9V74 host recorded in the README) are failed or partial and not a baseline. The research machine reports an AMD EPYC 7763 with 4 vCPU and 15 GiB, but the receipt does not record the host it ran on, so no host claim is made for it. Core grew from 443 s to 1307 s across suite growth, host and concurrency changes that cannot be separated. Historical #470 ("23 to 26 minutes serial") is on an older suite and host and must not be used as before/after. Issue acceptance criterion 1 asks for several retained receipts; only one verified comparable receipt exists, so the multi-receipt part stays open until the method in the plan produces more.

## Preflight design inputs

* Reviewed selector grammar already exists: `extra_selector` accepts `PROJECT:test_module[.Class.method]` matching `(core|agents|api|orchestrator|importer):test_[A-Za-z0-9_.]+`, and `dispatch` requires the module to be a tracked `src/PROJECT/tests/MODULE.py`. The helper should reuse that grammar, not widen it.
* Test import paths come from `test_paths`: own `tests`, plus `core/tests` for api, agents and orchestrator, plus `agents/tests` for api. Browser unit tests need `ZF_BROWSER_TESTS=1`; they skip without it ("opt-in local Chromium"). Zero-test or all-skipped output must fail.
* Browser harnesses: gate commands for `design_system_browser_check`, `case_journey_browser_check`, `employee_chat_browser_check` and `regulatory_ux_check` use `BROWSER_ENTRY` (scratch directories redirected to `TMPDIR`) and a pinned axe 4.10.3 file with `AXE_SHA256` `880970c0...a68bb`. The 320 px, 390 px and 1280 px widths live in these checks (`design_system_browser_check.py:173`, `case_journey_browser_check.py:1532`, `employee_chat_browser_check.py:312`, `regulatory_ux_check.py:504`). Browser group output paths are bounded to 58 bytes.
* `map_fullscreen_browser_check` (#1828) is not in the gate browser group and not run by `src-ci`; it is a local-only direct check (`--axe` and `--out` required). A path under `src/api/checks/` selects the gate `browser` group in `--changed`, but that group does not run this harness. Coverage claims must therefore be per check, never per directory.
* SQL: the gate starts an owned container (`--publish=127.0.0.1::1433`, label `ama.rpi.owner`), sets `ZF_TEST_MSSQL=1` and `ZF_SQL_*`, and verifies cleanup. A preflight must not start Docker or a database; it accepts only explicit loopback environment supplied by the caller and refuses otherwise.
* Heavy lock: `heavy_lock` uses `/tmp/ama-rpi-heavy.lock` with `flock`; the browser and SQL preflight paths must take the same lock and never run beside a gate.
* New files under `tools/` are unmapped by `changed_groups` (`tools/rpi-checks.py` and its test are the only mapped tool paths), so a local `--changed` run falls back to the full matrix, and the `src-ci` path filter lists tool files individually, so hosted CI does not run a new helper's tests. A new helper is therefore a direct local check until a reviewed workflow decision adds it.

## Worked cases (source-bound recipes; not executed here)

* #1828 map check (actual command from the PR #1829 changes record): from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests python -m checks.map_fullscreen_browser_check --axe <pinned-axe-4.10.3.min.js> --out <short external dir>` under `flock -n /tmp/ama-rpi-heavy.lock`; PR #1829 reports 330 PASS, 0 FAIL, 14 axe scans, 0 violations. The preflight adds exit mapping, the pinned hash check, the lock and a non-receipt label around this same command.
* #1297 320 px case: the 320 px viewport assertions are in the checks above (`design_system_browser_check.py:187` "wide data table scrolls with keyboard at 320px", `case_journey_browser_check.py:1545` "320x800 summary within one viewport scroll", `regulatory_ux_check.py:520` 200 percent text at 320 px). The exact failing check and head from the active #1297 lane were not read, because that worktree and its in-progress output are out of bounds. The recipe is `python3 tools/rpi-preflight.py --python <venv>/bin/python --browser-check design_system_browser_check --browser-check case_journey_browser_check --axe <pinned> --out <dir>` against the #1297 head after it is available. Replaying the real regression on that head is an Implement-phase acceptance item, not a claim made here.

## Dependency on #1297

* Overlapping source: `tools/rpi-checks.py` and `src/README.md`. Neither file may be edited for #1830 until #1297 merges; the plan's standalone helper, timing analyzer and method document touch neither, so they could in principle proceed first, but this staged handoff defers all implementation until #1297 merges and the branch is rebased (see the plan Dependency gate). Any runner scheduling change (H1 to H4) and any `src/README.md` cross-link belong to a later phase after a rebase on merged #1297 and, for runner changes, owner approval.
* `docs/reference/log.md` is append-only and a likely textual conflict point if #1297 also appends; resolve at rebase and never rewrite earlier entries.

## Risks and unknowns

* Helper results can be mistaken for a receipt: mitigated by fields and labels that the verifier schema cannot accept.
* An editable-install virtual environment is a caller prerequisite; the helper cannot create or modify one (no installs, no source mutation).
* Performance numbers depend on host load; a before/after claim needs two verified full receipts per arm and a recorded host manifest.
* Unknown: the real #1297 320 px failure and its head (deferred); whether the owner will approve scheduling changes (deferred).
