# Review: issue 360 live re-run (2026-11-18)

Executed once. Outcome: conformant for a docs-only demo evidence candidate. No src change; tier FOCUSED.

## Checks

* Evidence and secrets: literal scan of all re-run evidence, artifacts and the note for the three credential files' values: 0 hits (the one PNG with a blank page and the staff screenshot with emails masked were scanned as bytes).
* `git diff --check`: clean. Links in the appended section are relative to existing files.
* Claims against evidence: every row traces to a file in the re-run evidence folder. One weak spot, recorded honestly: the forged-role-header row in the re-run returned 200 without recording the role, so the note cites the 08:36 run for the unchanged role.
* mypy, ruff, unit tests and `rpi-checks.py`: not applicable (no source change); `--all` not run by owner instruction.
* Hosted CI: not observed; nothing pushed.

## Findings

None open. Routed later work: browser-mode 401 versus 302; owner records of c and e; a second Entra staff role; restart drill if ever authorised.

## Boundary

Unmet #360 criteria: c, d (partly), e. No issue box was ticked.
