---
title: Changes record for #462 live proof
ms.date: 2026-11-18
---

## Summary

Documentation and evidence only. No `src/`, `infra/` or Azure change; no throwaway resource created. Tier: FOCUSED. `rpi-checks.py --all` was not run. Refs #462.

## Files

* Added `docs/reference/research/resident-showcase-live-proof-2026-11-18.md`.
* Added `.copilot-tracking/evidence/2026-11-18-resident-showcase-live/` (`live-checks.json`, four desktop screenshots; credential fields masked).
* Updated `docs/reference/README.md` (index row) and `docs/reference/log.md` (append-only entry).
* Run artifacts: research, plan, details, critique, this record, review and the session state file.

## Divergences and honest notes

* The login limiter (5 failures per 10 minutes) caused 429 responses on three reruns; evidence comes from the last complete run, earlier incomplete runs were overwritten in the evidence folder.
* A diagnostic command printed the two credential-file values into the session terminal once; nothing was written to the repository (verified by a scan of docs and tracking).
* The sign-out control sits in an account menu; the first script versions looked for a visible button.

## Validation

* Secret scan of `.copilot-tracking` and `docs` for the credential values: no match.
* Link and diff review of the new note, index row and log entry.
* Not applicable: unit tests, mypy, ruff (no code), web UI guards (no web file changed), full gate.

## Per-criterion table

| Criterion | Status |
|-----------|--------|
| 1. Prospective RPI artifacts and threat model | Proven for this run; threat models preserved |
| 2. #444/#455 and rubric | Dependencies proven closed and merged; rubric outcome unproven (needs hosted run on pushed head) |
| 3. Login, denials, canary fields (ticked) | Re-observed live |
| 4. Secrets, HTTPS session, abuse controls (ticked) | Re-observed live |
| 5. SQL parity, Docker, gate, hosted CI (ticked) | Not re-run; rests on earlier evidence |
| 6. Pre-spend record | Proven: resources, USD 440.90 actual since 2026-10-01, about USD 259 left of USD 700, stop plan |
| 7. Live deployed browser verification | Proven on the demo at desktop width; pre-deploy gates not proven here |
| 8. Image identity, URL, limits, owned resources, expiry (ticked) | Refreshed; source commit for the digest unconfirmed |
