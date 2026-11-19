<!-- markdownlint-disable-file -->
# Issue 1818 live round 7: changes log (Refs #1818)

Chronological, UTC, 2026-11-18. No secrets, tokens, object ids or credential values. No `src/` change.

| Time | Action | Result |
| --- | --- | --- |
| 12:58 | Research, plan, single critique (C1 to C4 applied) | witness `research-open` and `plan-done` ok; implement-start ok 12:59 |
| 13:00 | Temporary role assignments (IoT Hub Registry Contributor, Event Hubs Data Receiver) and job `job-demo-live7` created | first start used a wrong command form and idled; fixed with `--args=-m...`; second execution `job-demo-live7-ddi13td` |
| 13:04 | Send window | `sent=9 failed=0 stored=9`, 25.6 s, exit 0; cumulative 54 of 200 messages |
| 13:07 | Employee browser (fresh) | 3 demo cards recent, list lines, filter 0 of 443; first selector attempts opened the wrong marker (mouse click on overlapping markers) and were corrected to keyboard activation; adverse attempts not kept as evidence |
| 13:08 | Resident browser (fresh) | first attempt timed out at `networkidle` (cold start); retried with `domcontentloaded`; recent, 11.55 C, 36 readings |
| 13:10 | Cleanup | job deleted, both temporary assignments removed, plus one leftover Event Hubs Data Receiver at the hub scope for the same identity; no live7 job remains |
| 13:17 | Resident browser (stale) | "older than 15 minutes" |
| 13:19 | Employee browser (stale) | 3 cards "Reading out of date", filter "3 of 443"; sign-in needed a 120 s timeout after an earlier cold-start timeout |
| 13:25 | Documentation | research note, index and log entries added |

Evidence (outside the repository): `job-live7-output.txt`, `shots/` (card text, card and page screenshots, list and filter screenshots, result JSON) under `/home/azureuser/.local/share/ama/phase-witness/1818-live-20261118T1257Z`.

## Per-criterion table (issue 1818, Refs only)

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 `/api/map` sensor summary | Proven (demo) | fresh 3, restricted 97, not-loaded 343 in one response |
| 2 Employee map, card, list, filter | Proven (demo) | cards, list lines, filter 0 then 3 of 443 |
| 3 Resident `#sec-sensors` | Proven (demo) | fresh and stale text; no other home id |
| 4 Tests and browser checks on exact HEAD | Unproven here | ticked by #1826; not re-run, no source change |
| 5 Live Hub to SQL to UI walkthrough | Proven (demo) | [research note](../../../docs/reference/research/issue-1818-live-iot-map-walkthrough-evidence-2026-11-18.md) |

## Validation (focused)

No source, test, workflow or infra file changed, so unit tests, mypy and ruff do not apply. Documentation link and diff review only. Scripts added: `walkthrough_probe7.py`, `walkthrough_employee7.py`, `walkthrough_resident7.py` (explorer `explore7.py`).
