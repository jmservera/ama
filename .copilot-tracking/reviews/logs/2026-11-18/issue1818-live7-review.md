<!-- markdownlint-disable-file -->
# Issue 1818 round 7: review (executed once)

Outcome: conformant for the stated scope (documentation and live evidence only); no material finding open. Routed follow-ups below.

## Scope assessed

Research note, index and log entries, changes record with per-criterion table, three Playwright scripts, retained raw output outside the repository. No `src/`, SQL, workflow or infra change; focused tier; `rpi-checks.py --all` not run.

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| R7-1 | Medium | The demo relies on image `demo-1818live6` containing the unmerged receiver fix (`7bde5f149`); main lacks it. | Separate full-tier task: land the fix with SQL tests. |
| R7-2 | Low | Resident chart y-axis labels oversized and overlapping "Latest stored" (R6-3 persists). | Separate UI follow-up. |
| R7-3 | Low | Device deletion is reported by the job, not read back (registry listing is unauthorised for this identity). | Accept for the demo; disclosed. |
| R7-4 | Info | A leftover hub-scope role assignment for the demo identity was removed during cleanup. | Disclosed in the note. |
| R7-5 | Info | Criterion 4 not re-run; ticked by #1826. | Disclosed. |

## Evidence handling

Credentials were read in-process only. Notes carry synthetic case ids only. Cleanup verified: no job and no role assignment for IoT Hub or Event Hubs remain for the demo identity; the Event Hubs namespace and route stay (owner-named, not throwaway).
