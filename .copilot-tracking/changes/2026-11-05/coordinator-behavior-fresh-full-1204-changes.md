<!-- markdownlint-disable-file -->
# Changes: fresh full behavior run (issue 1204)

* Source file unchanged: blob acefb44a4d254ede6d86413343127b763dec42cb before and after.
* Added: research update, plan, details (written before any action); sandbox 002 (run-state, design, test-log, run-index, test-review, mutant diffs and copies, raw-storage manifest for the 69 existing files, new-run raw manifest); behavior report 004; state; review.
* Commands: no-model strace probe (exit 1 from invalid model, agent path opened once); 22 native `copilot --model auto` children under strace (all exit 0); no rpi-checks, heavy lock, SQL, browser, scanner, cloud.
* Not done by design: no archive, move, normalization, deletion, gitattributes change or exemption; no existing raw file modified; the 97-test repeat waits for the final tracked candidate; range `git diff --check origin/main..HEAD` remains OPEN until root-approved lossless replacement.
* Divergence: the frozen F-P2b expectation was too narrow; recorded, not altered.
* Preserved: report 003, 001 sandbox, controls, grade-role deviation, cbebe refs, /tmp/h1204.
