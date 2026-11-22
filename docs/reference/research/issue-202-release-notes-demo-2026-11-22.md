---
title: Zava Forward demo release notes (draft, 2026-11-22)
ms.date: 2026-11-22
---
Draft release notes for the synthetic, desktop-only demo, prepared for issue #202. They are not published: no tag, GitHub release or folder deletion has been created. Whether a GitHub release accompanies the tag is still an open owner decision in the issue.

## Baseline

* Archive tag `v0.21.0` (annotated, object `0096b113`, commit `65a514ed`, 2026-10-27) holds the last commit containing `mvp/` (one tracked file, `mvp/README.md`). Both `mvp/` and `prototype/` are absent from the current tree.
* The notes cover first-parent commits on `main` from `v0.21.0` to `6fd6e3f8` (2026-11-22): 1388 commits, of which 516 `docs`, 327 `feat`, 186 `chore`, 172 `test`, 164 `fix`, 7 `ci` and the rest other prefixes. Pull request numbers are in the commit subjects. A GitHub search for merged pull requests is capped at 1000 results, so the commit log is the complete source.

## Deployed revisions (read 2026-11-22 20:55 UTC, resource group `ama`)

| App | Active revision | Health | Traffic | Image digest |
| --- | --- | --- | --- | --- |
| `ca-cutover-test-demo-api` | `ca-cutover-test-demo-api--0000053` | Healthy | 100 percent | `zava-forward-api@sha256:065628c9...467eed` |
| `ca-resident-demo` | `ca-resident-demo--0000025` | Healthy | 100 percent | `zava-resident-demo@sha256:e6b50684...906618` |

Both apps answer `/healthz` with HTTP 200 and `/` with 200.

## Highlights since the archive tag

* Demo bundles and fixes: reviewed demo fix bundles (#2105, #2106, #2107, #2155, #2159), a one-minute five-home simulator cadence (#1518), readings covering at least half of all homes (#2198), a dual-axis sensor chart and map gauges (#2196), and a resident sensor monitoring consent checkbox (#2197).
* Chat: five bounded agents as employee chat skills (#541), grounded resident answers with an AI label (#564, #593), answer origin labels and rule-grounded case-unblock answers (#1641), routing of questions to the right agent (#2199), per-role and per-thread limits (#1547), and receipts for refused turns (#661, #840, #1003, #1085).
* AI governance: fail-closed call authorisation (#1545), held-out freeze and leak gate (#1084), named-human approval for live RAI thresholds (#1631), a break-glass disclaimer recorded in response and audit (#879), and chat memory refused as controlled-decision evidence (#1552).
* Resident experience: resident page redesign (#1069), sensor gauges, history and plain-language chart summaries (#586, #603, #763), and a queue-level resident choice screen (#652, #715, #838).
* Sensors and IoT: a live reading simulator container for every home (#1088), a bounded Azure IoT Registry backend (#1393), the live versus backfill handover demo (#698, #847), and sensor status in the employee map and resident view (#1826).
* Infrastructure: a single-environment demo profile with internal identity (#2160), an optional DTU SQL tier and demo deployment fixes (#2167), a scripted Azure rebuild and teardown with dry run (#672), an offline deployment plan preview (#1662), and what-if results on the run summary (#996, #1012).
* Tooling: a read-only demo preflight script (#2209), an executable design traceability gate (#665), and an offline monitoring declaration check for task releases (#1140).

## Known limits

* Demo only: synthetic data, desktop only, no production claim.
* Generative AI answers are unprovable while an open suspension covers AI work; replies use rules only (see [issue-2202-finalproof-2026-11-22.md](./issue-2202-finalproof-2026-11-22.md)).
* The `mvp-ci` and `mvp-validation` workflow files remain, as dispatch-only replacements (see [issue-202-release-prep-2026-11-22.md](./issue-202-release-prep-2026-11-22.md)).
