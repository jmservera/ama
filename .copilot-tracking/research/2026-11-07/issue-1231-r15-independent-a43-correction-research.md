# Research: issue 1231 independent correction cycle 1 on a43d74cb

Date: 2026-11-07. Disposition: executed from the actual independent findings (session f751a4dc, files/review-1231-a43/functional-findings.json) and the code.

* Finding 1 (High): publish stages with os.open(..., 0o666); the hard link keeps that mode, so a 0022 or 0002 umask yields a 0644 or 0664 archive record where the parent's mkstemp gave 0600. Confirmed in ranking_publication.py. Fix: create the stage with 0o600 (the umask can only narrow it).
* Finding 2 (Medium): when link or write fails and the owned stage unlink also fails, the retained name exists only in an exception note; the runner serializes str(e) and the Store logs only the error, so the stage is undiscoverable. Fix: the helper sets an attribute stage_retained on the primary exception (note kept); the runner message and next action name the file, the Store logs a WARNING naming it and adds a path-free sentence to the 503 text.
* Not broadened: crash-orphan and fsync contract unchanged; no cross-UID observation is claimed.

## Chronology deviation (recorded, not hidden)

The source edits were made in the working tree before this research and plan were written to disk; nothing was committed before them. These records are committed before the source commit, but they are not strictly prospective. No critique was run.

## Limits

r14 receipt (50858c21...) and all earlier receipts stay preserved but do not cover any new head. Only light unit and static checks; no FULL, SQL, browser, images or scanners; #86 owns the heavy lane.
