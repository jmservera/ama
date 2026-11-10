# Profile-main checkpoint changes (issue 440, 2026-11-10)

Status: implementation complete (documentation only). The skeleton was written before `implement-start`; this file records the actual results. Raw outputs: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/profile-main-440-observation-1110/` (`01-identity.txt` to `08-post-run.txt`).

Plan: [plan](../plans/2026-11-10-profile-main-440-1110-plan.md). Details: [details](../details/2026-11-10-profile-main-440-1110-details.md).

## Planned changes

* `docs/architecture/cutover-evidence-pack.md`: one new appended dated section. No earlier section altered.
* Own RPI files under `.copilot-tracking/` (research, plan, details, critique, changes, review, state).
* No other path. Shared knowledge base files, source, tests, probe, manifest, infra, tools, workflows and rubric are not changed.

## Observations (actual)

| Step | Exit and result |
| --- | --- |
| Identity | HEAD `b23c08e33e4ebdb0aaa1dfd8fa586999448d8ca6`, tree `0bdc704b78b9a3ed95926b5915ae93ae9148032d`, four blobs equal C2; fetch at 2026-11-10T18:07:12Z shows origin/main `88a17f8b6d3da6dcfcb8b0db19f481f9e257f61e` (rubric score file only) |
| A1, A2 system Python selectors | Exit 0 (6 and 16 tests) but Core resolved to the separate primary checkout `/home/azureuser/source/ama/src/core`; classified not current-main proof, preserved |
| Private venv `/tmp/ama-440-profile-venv-1110` and editable install of this worktree's `src/core`, `src/agents`, `src/api` plus `playwright==1.64.0` | Exit 0; restore after the wrong-source finding, no global or browser install |
| B1 API helper tests, B2 Core journey, scenario and perspective tests | Exit 0; 6 and 16 tests OK; modules inside this worktree |
| Admission | No lock holder, MemAvailable about 2.75 GiB, cached Chromium present |
| C1 one existing browser walk | Exit 0, 714 PASS, 0 FAIL, 38 role-screen walks, 15 negatives, 15 declared no-table walks, case `ZF-4` only, about 29 seconds |
| Cleanup | No leftover process; empty scratch `/tmp/z440p` removed; venv and ignored editable metadata retained; `__pycache__` removed |
| Documentation checks | `git diff --check` exit 0; no non-ASCII added; all section links resolve (the review link after the review file exists) |

## Divergences and amendments

* Divergence from the details plan: A1 and A2 were not missing-dependency failures. They passed but imported another checkout, so the wrong-path restore condition added by the critique applied. No other divergence.
* The pre-existing primary-checkout editable install was not used as source proof and was not modified.
* No failure, retry or repair occurred. Nothing was waived.

## Erratum 2026-11-10 (correction chain `profile-correction-440-1110`)

Prompted by independent Readiness `aa570f67` (approve_with_comments, one Medium). The quoted original line above, "No failure, retry or repair occurred. Nothing was waived.", is INACCURATE HISTORICAL as written at head `2df576f7879ca05d9296013ff07d36fc54ed9cc9`. It is kept unchanged for traceability. This erratum is based on existing raw outputs only; no check, test, browser walk, install or gate was run or rerun to write it. Raw root `ROOT` is `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files`.

Corrected account:

* Product checks: no product-check failure and no repeat of the browser walk. A1 and A2 (wrong checkout, not current-main proof), B1, B2 and the single C1 browser producer each exited 0 (C1 in `ROOT/profile-main-440-observation-1110/07-browser-run.txt`: exit 0, 714 PASS, 0 FAIL). No repair was made and no check was waived by a test, probe or source change.
* Adverse harness result 1: `ROOT/profile-main-440-observation-1110/06-admission.txt`, section "chromium load check (version only)", printed `AttributeError: module 'playwright' has no attribute '__version__'` and then the cached chromium path. It was an admission version probe, not a product check and not the browser walk.
* Adverse reporting result 2: `ROOT/rpi-440-profile-main-2102.log` lines 264-265, `tail: option used in invalid context -- 4` then `Failed with exit code 1`. It was a shell reporting command printed in log order right after the C1 summary lines, not the browser producer, whose exit 0 stands separate in `07-browser-run.txt`.
* Further wrapper entries in the same native log, so the two results above are not read as exhaustive: line 475 `Failed with exit code 1` after the venv restore reporting command (the restore printed `exit=0` in `ROOT/profile-main-440-observation-1110/04-restore-venv.txt`), and a failed-marker entry at line 150 on a research-phase read-only reading command whose exit code text was not retained. Both are harness or reporting, not product checks.
* Distinction: harness or reporting failures are not product failures and are not evidence that C1 failed.

Root-attributed, not author reruns: fresh canonical witness `ROOT/root-440-profile-prepublication-witness-2112.json` (seven records, final head `2df576f7879ca05d9296013ff07d36fc54ed9cc9`, tree `f3b21ffc2a7ffcce01bd19b41a0fc3f78fab86c3`) and merge preview `ROOT/merge-preview-440-profile-2112.txt` (`a8c361af23fae3dc3b2432e94e88f4a69a12cdb0`). As of the C0 fetch at 2026-11-10T18:07:12Z, origin/main `88a17f8b6d3da6dcfcb8b0db19f481f9e257f61e` changed only the rubric `latest.json` over `b23c08e33`, so no rebase or merge was needed; this is not a claim about main at publication time. The C0 witness chain, review, state and logs are unchanged and keep their original outcome.
