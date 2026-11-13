<!-- markdownlint-disable-file -->
# Changes: #74 home-case browser verification (issue-74-browser-verification-0410)

Date 2026-11-13. Head under test 6f2918011d55d63ffc52865073ef45bd7ea9197c, tree 3d573c20311d43be2a1c6f3ef8601b638f8e4508, worktree clean before and after (`git status --short` empty). No product, test, check or config change. Only this task's tracking files are added.

Evidence directory (outside the checkout): `/home/azureuser/.copilot/session-state/b0e0aec9-3712-44c6-8da6-ef479f5047af/files/74-browser-verification-0410/` (not committed; hashes below).

## Preflight

* Lock `/tmp/ama-rpi-heavy.lock`: regular, non-symlink, owner azureuser, mode 664, inode 77057; fd inode 77057; acquired non-blocking at 2026-11-13T04:09:42Z; held by the runner through the end at 04:10:11Z (about 29 s); released afterwards (verified by a later non-blocking acquire).
* MemAvailable 5186912 KiB (4.95 GiB), above 4 GiB.
* Interpreter: owned venv Python 3.12.3 (`<evidence>/venv/bin/python`); playwright 1.64.0 imported from the owned venv; `zava-forward-core/agents/api` 0.1.0 installed non-editable from this checkout into the owned venv. The harness points the server `PYTHONPATH` at this checkout's `src/{core,agents,api}/src`, and the traceback of run 1 showed `checks` imported from this checkout's `src/api/checks`. No scratch editable imports.
* Chromium: Chrome for Testing 156.0.8078.4, cache `chromium-1248`, binary SHA-256 377a9fc07b495c3b8d0ab8ec1fdfd153641759f9756fea34d8dfce4de82f5025 (read-only cache, no download).
* axe: owned copy SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb equal to `AXE_SHA256`; the check also asserted it.

## Run 1 (preserved failure)

Selected command in the owned venv before any install: exit 1, `ModuleNotFoundError: No module named 'playwright'` at `home_case_browser_check.py` line 16. No browser or server was started. Log SHA-256 ab72ac7afe79b78cd5ac851f08be0098f56cfd21fa265781e2198c940d7cf307. This is the missing-dependency failure that permitted the declared install.

## Install

`pip install` of `src/core`, `src/agents`, `src/api` and `playwright==1.64.0` (declared in `src/api/pyproject.toml`) into the owned venv only: exit 0. No global, shared or other-worker environment touched; no uv, image, or browser download.

## Run 2 (same command)

Exit 0. 24 `PASS` lines, 0 `FAIL`, 0 skips, final line `COMPLETE: all checks ran, including axe 4.10.3`. Log SHA-256 3215442906bbb79c0318221936c0e71f2cff76daa62bbbb043bee04df405cecf.

Observed counts: 24 PASS = 1 server assertion ("owned server is running and responsive on loopback") + 23 browser/axe assertions. This equals the author-reported "home 24" (23 browser/axe + 1 server) from the PR body; the author figure is now reproduced for this head, not merely reported. Assertions observed:

| # | Assertion | Result |
| --- | --- | --- |
| 1 | owned server is running and responsive on loopback | PASS (server) |
| 2 | home panel is its own labelled region | PASS |
| 3 | building panel is its own labelled region | PASS |
| 4 | building dependency, hold, works and cost appear only in the building panel | PASS |
| 5 | home panel shows this home's decision, stage and cost allocation | PASS |
| 6 | shared building ID does not carry the sibling home's evidence | PASS |
| 7 | ZF-2 shows its own document and quality in the home panel only | PASS |
| 8 | shared system item is in the building panel only on ZF-2 | PASS |
| 9 | version status and no-transfer notice are shown | PASS |
| 10 | manual path to the case and building screens is shown | PASS |
| 11 | read-only: no write controls on the screen | PASS |
| 12 | one h1 then four h2 panels (5 headings listed) | PASS |
| 13 | reflow 320px | PASS |
| 14 | reflow 1280px | PASS |
| 15 | axe file is the pinned 4.10.3 build | PASS |
| 16 | axe 4.10.3 finds no violations: [] | PASS |
| 17 | ZF-3 has its own labelled home and building panels | PASS |
| 18 | ZF-3 shows its own document and quality in the home panel only | PASS |
| 19 | ZF-3 view carries none of ZF-2's own document or quality | PASS |
| 20 | shared system item is in the building panel only on ZF-3 | PASS |
| 21 | ZF-3 own GBP 6000.00 at home, GBP 12000.00 only in building panel | PASS |
| 22 | ZF-3 has one h1 then four h2 panels | PASS |
| 23 | made no non-GET/HEAD/OPTIONS requests: [] | PASS |
| 24 | no JavaScript errors: [] | PASS |

Zero post-sign-in writes and zero JavaScript errors were observed. The earlier "16 PASS" historical figure (#1406, historical head c6637004) is a different, older count and is not reconciled here.

## Cleanup

The harness terminated and waited on its own server and closed its browser in `finally` blocks, and its temporary scratch directory was removed (the owned scratch directory was empty afterwards). A process snapshot after the run found no server, Chromium or check process of this task; the two matching lines were this agent's own CLI command line. No name-based kill was used and no PID needed termination. Existing resources were not cleaned up.

## Added files

* `.copilot-tracking/research/2026-11-13/issue-74-browser-verification-0410-research.md`
* `.copilot-tracking/plans/2026-11-13/issue-74-browser-verification-0410-plan.md`
* `.copilot-tracking/details/2026-11-13/issue-74-browser-verification-0410-details.md`
* this changes record, the review and the state file.
