# Changes: issue 435 live pass 3 (2026-11-18)

Docs only, tier FOCUSED (documentation and diff review; no src, SQL, security, infrastructure or deck change). No Azure resource created; credential files not read. Witness note: `implement-start` reported the tree already dirty because the evidence folder and tracking files were created first; no source file was edited.

## Files

* `docs/reference/research/capstone-pitch-435-live-r3-2026-11-18.md` (new)
* `docs/reference/research/evaluation/pitch-435-live-r3-2026-11-18/deck-inspection.txt`, `azure-readonly.txt` (new, command output, no secrets)
* `docs/reference/README.md` index row; `docs/reference/log.md` entry
* `.copilot-tracking/` research, critique, plan, details, changes, review and state for this pass (`-r3`; earlier passes preserved)

## Per-criterion proven or unproven

| # | Criterion | Issue tick | Result |
| --- | --- | --- | --- |
| 1 | Placement decided; deck rebuilt if changed | unticked | Proven (decision, deck inspected, unchanged, no rebuild owed) |
| 2 | Mentor confirms meaning of Tokenomics | unticked | Unproven: needs the mentor; owner-only |
| 3 | Segment rehearsed in the timed route | ticked | Unproven: rehearsal notes record no performed timing; tick conflicts with the repository |
| 4 | Finite batch decision, spend authority recorded | unticked | Proven for the demo (#432 batch: 12 calls, 2,522 tokens, USD 0.000744, authority recorded) |
| 5 | Deck challenged against the full guide | ticked | Not re-proven; existing offline challenge cited |
| 6 | Statements sourced and labelled, no price, saving or payback | ticked | Consistent with retained slide text; not re-proven |

## Validation

* python-pptx inspection of the deck and read-only `az containerapp show` and `az eventhubs namespace show`: outputs retained.
* Relative-link check on the new note: no broken links.
* `git diff --stat` reviewed. mypy, ruff, unit tests and `rpi-checks.py --all` not applicable or not run (no src change).
