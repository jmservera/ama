<!-- markdownlint-disable-file -->
# Details: Blob plus Quality parent-topic checkpoint (2026-11-09)

Plan: [plan](../plans/2026-11-09-blob-quality-2055-440-plan.md).

## P1 reuse table (to appear in the pack)

| Dependency | Evidence | Status at HEAD |
| --- | --- | --- |
| Blob adapter, publication, runner, wiring (Core 26+57+53, API 36), Bicep policy 59 | `logs-1288-main-integration` at tree of `2aa038043` | Historical reuse; src/infra identical except `dispatch.py` and score data |
| Quality sensor/consumer/lane/assistants (API c7 45, e2 62, lane 30, assistants 120, release 54, transport 7, inventories 29, consumption 17+42, bounds 6, consumer 47) | same logs | Historical reuse; 100 skips (58 SQL, 31, 7, 4) |
| Agents 303 | `logs-1288-e8` | Fresh for the E8 wrap only, not a published or hosted result |
| Quality retained-sensor browser journey | none retained at an integrated head | O1 selected |
| Live Blob, immutability, remote atomicity, from-empty deployment, actual model, final SQL audit, AT | none | Unknown or deferred, owners listed |

## P2 O1 steps

1. `mktemp -d /tmp/i440-bq-2055-XXXXXX` as `D`; subdirs `home`, `tmp`, `data`, `logs`.
2. `python3 -m venv D/venv`; `D/venv/bin/pip install -e` the three worktree projects. If Playwright is not resolved, install into this venv only.
3. Import-origin proof (all modules resolve inside this worktree).
4. Admit the check through `flock -n`; capture stdout/stderr, exit, start and end time and tool versions to `D/logs`.
5. Verify no owned process remains; `git status` clean of the fixture.

## P3 documentation

Append "Parent-topic Blob and Quality checkpoint (2026-11-09, Refs #440 #1288 #1258 #1259 #136)" to the pack, with merged-main Blob observations and parent-topic observations in separate subsections, the document-qualified trace, the reuse table, the 761/861 discrepancy, unmet matrix and the final merged-main resume requirement. One index paragraph in `docs/reference/README.md`; one appended `log.md` entry.

## P4

Changes record, one independent `rubber-duck` Review of the delta, state JSON, handoff, one Conventional Commit with the noreply identity and Copilot trailer.
