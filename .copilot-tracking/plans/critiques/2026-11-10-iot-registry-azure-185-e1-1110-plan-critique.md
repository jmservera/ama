<!-- markdownlint-disable-file -->
# Critique: #185 Registry adapter E1 plan (single pass)

Executed once, 2026-11-10 by the implementing agent as an adversarial read of the [plan](../2026-11-10-iot-registry-azure-185-e1-1110-plan.md) and [details](../../details/2026-11-10-iot-registry-azure-185-e1-1110-details.md) against the [research](../../research/2026-11-10-iot-registry-azure-185-e1-1110-research.md) and the Root brief. No nested agent (brief). Verdict: proceed with amendments; all compatible and applied directly; no user decision needed; not repeated.

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | A real hub lists every unmarked foreign device without `statusReason`; with more than 100 of them `list_run` refuses `LIST_INCOMPLETE` on every call, so the adapter is unusable on a large shared hub. | Medium | Accepted, not weakened. Refusal is the truthful result under the bounded contract; skipping would reopen F1. Documented in the README as a limit (use a hub or scope where unmarked devices stay within the budget). No new policy invented. |
| 2 | Confirmation reads of non-enrolled IDs touch metadata of foreign devices. | Low | Accepted: `get_devices` already returns it; the read is metadata-only, nothing is stored, logged or returned except the ID. |
| 3 | A suppressed `__context__` remains reachable by code that walks it. | Low | Accepted and documented; clearing it is impossible inside a caller handler. Tests assert the formatted traceback, repr and `__suppress_context__`, not an absent `__context__` for ambient cases. |
| 4 | A shared 100-read budget could be consumed by unmarked entries that are listed before a marked one, refusing instead of listing it. | Low | Accepted: refusal is the explicit, safe result; order cannot cause a silent omission. |
| 5 | Including a non-enrolled ID could make `provision` active-run checks refuse spuriously. | Low | Intended: a marked hidden run identity is an active run; refusal is truthful. |
| 6 | The suppress flag set in `__init__` could be lost if a caller re-raises with `from`. | Low | No such site exists; the traceback test covers every refusal path so a future regression is caught. |
| 7 | A concurrently deleted device returns 404 on confirmation. | Low | Treated as absent (not owned); covered. |

## Checks that passed

* Complete-or-refuse holds: every list entry is either decided by an exact string marker or a bounded read, or the call refuses.
* No wildcard or unconditioned destructive path, no new SDK method, no change outside the owned files and README.
* Authority and scope: E1 only; no live operation; historical records untouched.
