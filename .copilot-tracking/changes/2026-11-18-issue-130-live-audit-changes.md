# Changes: issue 130 live audit (Refs #130)

Tier: FOCUSED, docs and evidence only. No `src/`, workflow, infra or dependency file changed; `rpi-checks.py --all` not run.

## Files

* `docs/reference/research/issue-130-live-r3-nomination-route-audit-2026-11-18.md` (new)
* `docs/reference/README.md` (index line), `docs/reference/log.md` (append)
* `.copilot-tracking/evidence/2026-11-18/issue-130-live-r3/` (probe scripts, raw output, digest, offline test summaries, screenshot)
* `.copilot-tracking/{research,plans,details,critiques,changes,reviews,rpi-sessions}` artifacts

## Per-criterion table (demo)

| Criterion | Issue | Result |
| --- | --- | --- |
| Representative participation and comprehension need authorized human evidence | Unticked | UNPROVEN, cannot be proven for the demo: needs real representatives; `representative_authorities` empty; person-run testing excluded |
| Original account, source, channel kept | Ticked | Offline proven; live write unproven (403) |
| Acknowledged route and named owner before review | Ticked | Offline proven; live read of owner list only |
| Challenge or correction with evidence, reviewer, outcome | Ticked | Offline proven; live write unproven |
| Correction re-reviews dependents only | Ticked | Offline proven; live unproven |
| Hazard routes to #85 | Ticked | Route text proven live; live hazard referral unproven |
| Non-response, support needs never lower priority; unknown not none | Ticked | Offline proven; null hazard_concern refused live |
| Tests: wrong identity, limited authority, manual route | Ticked | Proven offline (91 core, 14 api OK) |
| Nothing sent, booked, approved automatically | Ticked | Proven live (no write succeeded) |

Production-only or person-dependent: OD-41/OD-42 representative authority, staffed-acknowledgement delivery evidence, policy owner appointment, Azure SQL nomination coverage and whole-graph acceptance.

## Findings

* Blocking defect persists on revision 0000031 (digest `sha256:5368f4e4...c17e5fb`): every staff write returns 403. Fix would change a `src/core` security control (FULL tier); not done, reported.
* Azure: read-only; nothing created, nothing to delete. Credentials: runtime read, literal scan of evidence found none.
