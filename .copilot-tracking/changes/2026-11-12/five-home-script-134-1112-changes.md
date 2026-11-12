<!-- markdownlint-disable-file -->
# Changes: five synthetic demo homes (2026-11-12, Refs #134 #184)

Task `five-home-script-134-1112`. Base `d288b2a893a5a934f4357bbc7be79fa94ab59580`. Documentation only.

## Changed

* [docs/capstone/demo/runbook.md](../../../docs/capstone/demo/runbook.md): `ms.date` and description; new section with the target-mode table, five homes with ids and direct links, provenance and limits, preflight.
* [docs/reference/README.md](../../../docs/reference/README.md): `ms.date` and one pointer sentence.
* [docs/reference/log.md](../../../docs/reference/log.md): one appended entry.
* Tracking: research, plan, details, critique, this file, review, state record.
* Outside the repository: `files/134-five-home-script-1112/` in the coordinator session folder (`selected-five.json`, `replay_probe.py`, `replay_output.json`); not committed.

## Actions actually run

* Read-only local replay of the committed generator simulation (not the register), twice before the critique, byte identical; 980 cases, 443 open. No further replay after critique PC-002.
* Link existence/anchor check script (read-only), route regex check, `git diff --check`, dash scan, status checks. No runtime, gate, CI, cloud, model, SQL or live action; no push.
* Disclosure: the log and index edits were applied with a short Python text-replace script rather than the edit tool.

## Validation record (docs tier)

| Check | Result |
| --- | --- |
| Relative links in runbook and index resolve, new anchors exist | Pass |
| Same check on log: 17 pre-existing missing targets in older entries (outside this diff) | Pre-existing, not changed |
| Route regex accepts all five `#/case/<id>?tab=quality` | Pass (source regex copied) |
| `git diff --check` | Pass |
| No en or em dashes in added lines | Pass |
| Hosted CI, full gate, runtime, deployed-origin availability, sensor existence | Not run |

## Divergences

Section placed before "Choose The Route Beforehand" (details said after) so the route table can be read with the target mode in mind; route E is referenced as "below".
