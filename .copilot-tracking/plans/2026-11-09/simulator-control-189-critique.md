<!-- markdownlint-disable-file -->
# Issue 189 critique (one pass, 2026-11-09)

Execution: executed once, independent `rubber-duck` agent, on the final candidate plan and details. Verdict: Revise. Dispositions below are applied directly; no finding conflicts with a confirmed user decision and no significant or divergent issue needs a user decision. Critique is not repeated for this task.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | High | Process lock plus revision check is not cross-process; another replica or the CLI could overwrite between check and replace. | Accepted. Add an exclusive non-blocking `flock` on a sidecar lock file beside the control file (`live_control.locked`), held across read, check, write and read-back, used by the API surface AND the existing CLI start/stop (small backward-compatible edit to `live_control.py`). Lock failure fails closed with `CONTROL_BUSY` 409. Tests: concurrent writer holds the lock (API refuses), CLI refuses while locked, two racing API starts produce one success. Advisory-lock behaviour on an Azure Files SMB mount is UNPROVEN and recorded as such; the expected-revision check remains the second guard. |
| 2 | Medium | "Sending" implies a live run. | Accepted. State label is "Permitted" with the text that sending is permitted until expiry and this screen cannot see whether a simulator job runs; API `state` keeps the `decide()` value but adds `activity: "unverified"`. Test with no simulator running asserts the wording and field. |
| 3 | Medium | Authorization tests lack a concrete boundary matrix. | Accepted. HTTP matrix for GET, start and stop: no principal, malformed principal, wrong tenant, no OID, non-admin staff role, admin plus staff role (allowed), contractor, password provider (no admin possible), missing CSRF header, lookalike paths (`/api/admin/simulator-control/`, `/api/admin/simulator-controls`, `/api/admin/simulator-control/start/x`), each asserting 401/403/404, no file change and no disclosure; case, finance and audit GETs remain refused for the administrator. |

Plan and details were revised for these dispositions in the same pass (see plan risks and details contract; `CONTROL_BUSY` added).
