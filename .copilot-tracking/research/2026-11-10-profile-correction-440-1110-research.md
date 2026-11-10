# Profile-main correction research (issue 440, 2026-11-10)

Task `profile-correction-440-1110`, parent `profile-main-440-1110` (C0, head `2df576f7879ca05d9296013ff07d36fc54ed9cc9`, tree `f3b21ffc2a7ffcce01bd19b41a0fc3f78fab86c3`, witness chain 7, verify exit 0). Research disposition: executed, reading existing raw outputs only.

## Trigger

Independent Readiness `aa570f67` (`ROOT/independent-440-profile-main-2111/readiness/readiness-findings.json`): approve_with_comments, one Medium. The C0 changes file lines 26-30 states "No failure, retry or repair occurred. Nothing was waived." That blanket claim omits two retained adverse harness results.

## Evidence read (existing files only; ROOT is `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files`)

| Item | Locator | Finding |
| --- | --- | --- |
| Admission version probe | `ROOT/profile-main-440-observation-1110/06-admission.txt`, section "chromium load check (version only)" | `AttributeError: module 'playwright' has no attribute '__version__'`; the same probe then printed the cached chromium path. Harness probe error, not a product check; the probe was not the browser walk |
| Reporting tail | `ROOT/rpi-440-profile-main-2102.log` lines 264-265 (native session 2102 log) | `tail: option used in invalid context -- 4` then `Failed with exit code 1`, in log order right after the C1 summary lines. Shell reporting command only, not the producer; the file it read is not asserted. The log also shows `Failed with exit code 1` at line 475 (venv restore reporting; restore printed exit=0) and a `✗` marker at line 150 (research-phase read-only reading command); both are harness/reporting, disclosed in the details |
| C1 producer | `ROOT/profile-main-440-observation-1110/07-browser-run.txt` | Producer `exit=0`, 714 PASS, 0 FAIL, one walk. Distinct from both adverse results; no repeat of the browser walk |
| Wrong-checkout A1/A2 | C0 changes divergences and pack section | Already recorded honestly as not current-main proof; unchanged |
| Root fresh canonical witness | `ROOT/root-440-profile-prepublication-witness-2112.json` | Seven records, exact final head and tree as C0, same artifact-change notes. Root-attributed, not an author rerun |
| Root merge preview | `ROOT/merge-preview-440-profile-2112.txt` | Single line `a8c361af23fae3dc3b2432e94e88f4a69a12cdb0`. Root-attributed; its construction method is not in the file |
| Current main | origin/main `88a17f8b6d3da6dcfcb8b0db19f481f9e257f61e` | Changed only `.github/rubric/scores/latest.json` over `b23c08e33`; no rebase or merge needed |

## Findings

* The C0 claim is inaccurate as a blanket statement. It is accurate only for product checks (A selectors, B1, B2, C1 all exited 0) and for the browser walk (single run, no repeat).
* Neither adverse result is a product failure or evidence C1 failed. Neither was rerun, repaired or waived by a test change.
* Smallest correction: a dated erratum in the C0 changes file that quotes the original claim as inaccurate historical at `2df576f`, narrowed account and locators. The pack section does not make the blanket claim (to be confirmed by a read of its Process record before deciding on an amendment).

## Planning Readiness

Ready. Constraints: no source, test, tool or metadata run; no edit to the C0 review, state, event log or raw logs; erratum added without rewriting the quoted original text.
