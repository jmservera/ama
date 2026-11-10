# Profile-main correction details (issue 440, 2026-11-10)

Plan: [plan](../plans/2026-11-10-profile-correction-440-1110-plan.md).

## Phase 1 erratum content

Heading `## Erratum 2026-11-10 (correction chain profile-correction-440-1110)` appended to the end of the C0 changes file. Contents:

* Quote of the original line `* No failure, retry or repair occurred. Nothing was waived.` stated INACCURATE HISTORICAL at `2df576f7879ca05d9296013ff07d36fc54ed9cc9`; the original lines stay in place.
* Narrowed account: no product-check failure, no repeat of the browser walk, no repair and no waiver. Exit 0 for A1, A2, B1, B2 and the single C1 producer.
* Adverse harness result 1: `ROOT/profile-main-440-observation-1110/06-admission.txt`, version-only chromium load probe `AttributeError: module 'playwright' has no attribute '__version__'`; the same probe printed the cached chromium path. Not a product check or the walk.
* Adverse harness result 2: `ROOT/rpi-440-profile-main-2102.log` lines 264-265, `tail: option used in invalid context -- 4`, `Failed with exit code 1`; a shell reporting command whose output is printed immediately after the C1 summary lines in log order. State only the log position and that it was a reporting command, not the browser producer; do not assert which file it read.
* Further shell-wrapper adverse entries, disclosed so the two named results are not implied to be exhaustive: log line 475 `Failed with exit code 1` after the venv restore reporting command (the restore itself printed `exit=0`; the trailing filtered `git status` reporting step is the likely source, stated as likely, not proven); and the log's `✗` marker at line 150 on a research-phase read-only ADR/PRD/probe-log reading command whose exit code text is not retained in the lines read. None is a product check or the walk.
* Distinction: C1 producer exit 0 in `07-browser-run.txt`, 714 PASS, 0 FAIL, one walk.
* Root-attributed, not author reruns: canonical witness `root-440-profile-prepublication-witness-2112.json` (seven records, same head and tree) and merge preview `merge-preview-440-profile-2112.txt` (`a8c361af23fae3dc3b2432e94e88f4a69a12cdb0`).
* Main as of the C0 fetch at 2026-11-10T18:07:12Z and the Root merge preview: `88a17f8b6d3da6dcfcb8b0db19f481f9e257f61e` changed only the rubric `latest.json` over `b23c08e33`; no rebase or merge needed. This is not a claim about main at publication time.

## Validation

Read-only documentation and provenance checks only (no test, browser, install or gate run): the witness `verify` is a read-only provenance reader of this chain's records and is the only tool run beyond `git`, `grep` and link existence checks. `git diff --check`, ASCII check on added lines, link targets exist, `git diff --name-only` limited to the changes file plus own-chain files.
