---
title: Changes, issue 153 content-audit live run 2
ms.date: 2026-11-18
---

Refs #153. Docs and evidence only; no `src/` change. Tier: FOCUSED (no source, SQL, security, infrastructure or
deployment change). Not run: `rpi-checks.py --all`, mypy and ruff (no Python under `src/` or `infra/` changed; the
audit scripts live under `docs/reference/research/`).

## Files

* `docs/reference/research/content-audit-live-153-2026-11-18.md` (new): findings N1 to N6, holds P1 to P5, per-criterion result.
* `docs/reference/research/content-audit-live-153-2026-11-18/` (new): `scripts/login.py`, `scripts/audit.py`, `screen-hit-summary.json`, 43 redacted screenshots in `screens/`.
* `docs/reference/README.md` and `docs/reference/log.md`: index row and appended entry.
* `.copilot-tracking/` research, plan, details, critique, changes, review and `issue-153-live2-state.json`.

## Per-criterion result

| Criterion | Result | Evidence |
| --- | --- | --- |
| Content standard and glossary exist | Proven | `docs/reference/research/ux/content-standard.md`, used as the audit reference |
| Copy audit removes gate, hold, provenance, trace from core flow | Partly proven | No gate, provenance, trace or snapshot on 43 screenshots; "Held", "envelope" and a verb "holds" remain (N3, N4) |
| Error and blocked messages state reason, owner, next action | Partly proven | P3 holds; N1, N2, N5 show gaps |
| AI suggestion text says "AI suggestion, not approved" | Proven | P2, P5 on the staff AI tab (case ZF-2025-0031) and the resident page |
| Resident-facing wording reviewed by a named human before any use | Unproven | Needs a named person's dated review record of exact text; an automated run cannot supply it; the demo waivers cover DPO and Legal approval, not this step |

## Deviations and incidents

* The state file `issue-153-live-state.json` (from an earlier run) was overwritten in the worktree before its prior existence was seen; restored with `git checkout`, diff clean, and the new state is `issue-153-live2-state.json`. The witness `research-open` call was made before this and recorded the old path; later calls use the new path.
* `/tmp/state-*.json` session files vanished mid-run (another process); the scripts now use `~/.cache/ama153` (mode 700, not committed).
* No Azure resource was created; nothing to delete. No credential value was printed.
