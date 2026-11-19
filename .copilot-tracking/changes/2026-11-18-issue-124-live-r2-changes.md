# Changes: issue #124 live audit, second pass

Status: complete. Tier FOCUSED. No source edit, no Azure resource created or changed, `rpi-checks.py` not run.

## Files

* `docs/reference/research/issue-124-live-r2-phase0-discovery-audit-2026-11-18.md` (new): method, retained evidence, per-criterion table, owner-only list.
* `docs/reference/README.md`: one index sentence after the existing #124 entry.
* `docs/reference/log.md`: appended entry; earlier entries untouched.
* `.copilot-tracking/evidence/2026-11-18/issue-124-live-r2/`: `unittest.txt`, `probe.json`, `consumers.txt`, `azure_cli_outputs.txt`, `live_discovery_probe.py` and `.json`. The browser screenshot was deleted because it only showed the signed-in workbench and could carry account details.
* Tracking artifacts `*-issue-124-live-r2-*` for research, plan, details, critique, changes, review; state file updated in place for this pass (the earlier pass's artifacts are untouched).

## Validation

| Check | Result |
| --- | --- |
| `PYTHONPATH=src:tests python3 -m unittest test_discovery_contract test_discovery_flow test_discovery_register` (from `src/core`) | 59 tests OK (before and after the edits) |
| Probe re-run, compared to first pass | Identical apart from worktree path |
| Relative links in the new note | All resolve |
| `git diff --check` | Clean |
| Secret scan of evidence | Only the driver contains the words for runtime file reads; no credential values, no e-mail addresses, no GUIDs in outputs |
| mypy, ruff | Not applicable (no `src` or `infra` Python changed) |
| Hosted CI | Not observed; nothing was pushed |
| sloptrim detector | Not found on this machine; prose rules applied manually |

## Per-criterion table

| Criterion (issue state) | Proven for the demo | Unproven | Class of the gap |
| --- | --- | --- | --- |
| Discovery owner nominated and endpoint agreed (unticked) | Rule: human-only, distinct from sponsor, endpoint fixed to accepted handover | The nomination and agreement themselves | Owner/person-only (executive sponsor) |
| Lifecycle and event dictionary validated (unticked) | Schema and counts 15/15/8/7/4; 49 gaps block sign-off | Operational-owner validation | Owner/person-only (workshops) |
| Constraint register supporting and contradicting evidence (unticked) | Two-sided rule; seed register 0/0 with two gaps per hypothesis | Real evidence from the twelve-month extract and owner validation | Owner/person-only plus approved company data |
| Findings are not company findings until owners validate (ticked) | Re-confirmed, fail-closed | None | None |

## Deviations

* The first `implement-start` witness call was refused because the state file lacked the changes pointer. The pointer was added and the call repeated (`ok`), with the witness's qualification that documentation edits predated it (the README and log edits ran in parallel with the first call). A first `implement-done` call was also refused because I had removed this file to rewrite it; it is repeated below.
* A first run of the live probe crashed in its final print after writing output; the driver was fixed and re-run.
