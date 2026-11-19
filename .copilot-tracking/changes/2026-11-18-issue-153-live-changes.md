# Changes: issue 153 live plain-language audit (2026-11-18)

Tier: FOCUSED (docs and evidence only; no src, infra, SQL or deployment change; Azure access read-only).
Refs #153.

## Files

* docs/reference/research/plain-language-live-153-2026-11-18.md (new research note)
* docs/reference/research/plain-language-live-153-2026-11-18/ (scripts, JSON, text, 20 screenshots)
* docs/reference/research/ux/content-standard.md (dated section, ms.date)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/ research, critique, plan, details, changes, review, state

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Standard and glossary exist (ticked) | Proven earlier; unchanged |
| Copy audit removes gate, hold, provenance, trace (ticked) | Proven for 13 staff views and resident page; caveat F1, F2 (internal identifiers in dynamic text) |
| Errors state reason, owner, next action (ticked) | Not proven universally: 404/403 bodies give reason only (F3, F4) |
| AI suggestion label (ticked) | Proven live on Assistant proposals |
| Resident wording reviewed by a named human (UNTICKED) | Unproven: needs a person's review record; reviewer appointed 2026-10-15; exact text captured for review |

## Validation

* Link check and git diff review (below, review record). mypy, ruff, unit tests, rpi-checks: not applicable (no code).
* Azure: no resource created, nothing to delete. Playwright used for browser proofs.
* Incident: credential file contents were printed once to the session log by a shape-check command; not in repo.
