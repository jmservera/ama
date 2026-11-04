<!-- markdownlint-disable-file -->
# Plan: resident sensors live seed (#1072, Refs #462)

Task slug `resident-sensors-live-seed-1072`; branch `ops/sensors-live-seed-1072`; target `main`. Details: [phase details](../../details/2026-11-04/resident-sensors-live-seed-1072-details.md). Critique: [critique](./resident-sensors-live-seed-1072-critique.md).

## Phases

* [x] Phase 1: read-only root-cause check (live walk, SQL network posture, repository evidence).
* [x] Phase 2: assess the documented apply and seed route; stop when it needs access not held (owner decision recorded).
* [ ] Phase 3: live view apply and synthetic seed. Blocked on the owner decision in the issue comment and the UX doc section; not performed.
* [x] Phase 4: record evidence in the UX doc, `docs/reference/README.md` and `docs/reference/log.md`; commit, push, open PR with `Refs #1072` and `Refs #462`.

## Acceptance mapping (issue #1072)

| Criterion | Status |
| --- | --- |
| Synthetic sensor readings seeded or mapped for at least one demo resident | Not met |
| Re-walk records temperature, humidity and 24-hour forecast live | Not met (walk done; fail-closed message observed) |
| Synthetic only, no private data | Preserved: nothing loaded |

The PR therefore uses `Refs`, never `Closes`.
