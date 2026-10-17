<!-- markdownlint-disable-file -->
# RPI Phase Details: climate-source-evidence-178

## Metadata

Task 178; date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md
Research: .copilot-tracking/research/2026-10-17/climate-source-evidence-178-research.md

## Phase Index

| Phase | Name | Status | Detail |
| --- | --- | --- | --- |
| P01 | Bounded temperature evidence | Complete | P01-T01 |
| P02 | Canonical integration | Complete | P02-T01 |
| P03 | Validation/reconciliation | Complete | P03-T01 |
| P04 | Rebase-only continuation | Complete | P04-T01 |

<!-- rpi:phase id=P04 -->
## P04: Rebase-only continuation

<!-- rpi:task id=P04-T01 -->
### P04-T01: Preserve and validate combined evidence

Caller-authorized continuation from f4ea7542874baf6045db2e33764b1348a976c238
onto main 4e4a389f53870137a0f0582861766be5983a8f96. Remote topic lease is
the original full feature head. Initial worktree clean, PR #371 open/main.
Only docs/reference/README.md, docs/reference/log.md and src/core/README.md
overlap; combine clear additive intentions. Preserve main's entire source
tree except the original narrow climate documentation delta; preserve feature
helper/tests/JSON/synthesis byte-for-byte. Every main/feature log entry must
survive, in its original stream order. Stop on ambiguous intent.
No removals or new production targets. No downloads, private data, Azure,
role/network changes, spending or approval. Replay only existing public input
using P01-T01's exact command and cmp against the unchanged JSON.
Focused unittest/compileall and exact existing available lint/type checks;
report unavailable tooling honestly, never fabricate a pass.
Check upstream blob retention, feature-only blob retention, original main
log entry sequence, original feature log entry sequence, shared-file additions
and git diff --check. One bounded resolution Review, not a second assessment
of original full #178 acceptance. Update existing artifacts then one
force-with-lease push to only the named topic and PR #371 update; STOP.

Completion: rebase finished at implementation head e2c0a19. Only index and log
needed manual additive resolution; core README auto-combined cleanly.
All 2,129 upstream non-feature files byte-identical, all four feature-only
production files byte-identical; all upstream shared-file added lines retained.
Main's 267 and feature's 266 log entries each occur once in original stream
order; main's complete log remains a byte-prefix. Eight climate tests,
compileall, exact retained-input cmp, four changed local link references and
git diff --check passed. Existing core CI Ruff/format/mypy all passed using
already installed Ruff 0.17.1/mypy 2.4.0 in the recorded #370 rebase environment.
No install/download. Exact commands/results are in the changes record.
Resolution Review completed once: execution Complete, outcome Conformant for
P04 only. Parent delivery remains next, not owner/full-feature acceptance.

<!-- rpi:phase id=P01 -->
## P01: Bounded temperature evidence

<!-- rpi:task id=P01-T01 -->
### P01-T01: Offline parser, synthetic tests and derived JSON

Context: W5 supplies monthly averages, no RH, exact Durham coordinates/elevation.
Intent: reproducible statistics for 1991-01 through 2020-12, not replay extremes.
Targets: tools/climate_station_bounds.py, tools/test_climate_station_bounds.py,
docs/reference/research/climate-source-evidence-178.json.
Dependencies: local W5 bytes, no package installs/network.
Input locator:
/home/azureuser/.copilot/session-state/836a4f13-ad62-4778-8bea-453cc42fe79f/files/climate-178/durhamdata.txt.
Preflight verified 92,268 bytes and W5 hash on 2026-10-17.
Offline invocation:

```bash
python3 tools/climate_station_bounds.py \
  /home/azureuser/.copilot/session-state/836a4f13-ad62-4778-8bea-453cc42fe79f/files/climate-178/durhamdata.txt \
  --source-url https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/durhamdata.txt \
  --retrieved-on 2026-10-17 --start-year 1991 --end-year 2020 \
  --expected-sha256 d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9
```

No redownload if bytes absent/mismatched. CLI output is the generated report.
Boundaries: parse only documented monthly schema; reject incompatible headers,
units, malformed/nonfinite numbers and duplicate dates; count estimated,
provisional, missing and absent months; independent field quality decisions.
Midpoint needs both valid fields; retain minima/maxima source lines and all ties.
Count contract: expected 360 calendar months; present + absent = expected.
Per field present = valid + provisional + missing + estimated, using provisional
row first, then missing token, then estimated token. Diagnostics do not overlap.
Pair counts valid + excluded = present; no cross-month pairing.
Empty field/pair returns status unavailable, null extrema and zero valid count;
zero rows in window errors. No interpolation/filling. Test exact counts,
absent dates, ties, all-invalid series, invalid months and unknown markers.
Metadata includes source URL, actual retrieval date, station header, input hash,
period, counts, statistic definitions and humidity unavailable reason.
Validation: tiny wholly synthetic fixture strings and real public input;
CLI bad input exits nonzero; deterministic JSON; independent output cross-check.
Unresolved: station representativeness and reuse approval, not parser defaults.
Completion evidence: command outputs/counts and hash in changes record.
Observed: 360/360 calendar months, 351 accepted pairs, nine estimated exclusions
per temperature field. Eight unittest methods pass. Report hash
f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615.

<!-- rpi:phase id=P02 -->
## P02: Canonical integration

<!-- rpi:task id=P02-T01 -->
### P02-T01: Metadata, terms, recommendation and results

Context: C1 offline table is historical; W1-W14 enable real progress.
Targets: existing synthesis/register, reference README and append-only log;
directly coupled src/core/README.md climate-status paragraph.
Intent: new dated current section with official comparison, sources, exact
HadUK release OGL/citation, CEDA login test, Met Office automation restriction,
Durham evidence and no-RH limitation. Link derived JSON/helper, no tracking
links in canonical docs.
Primary product: administrative regions v1.3.2.ceda, UUID
386b3c1ee2054ef5ae0d73060963a9f1, matching W3/W4. 1km UUID
789b3065d74a4c948ab05d33556c86d0 remains a distinct grid alternative, not the
same citation or tested download. No adopted paired replay source exists.
Dependencies: P01 output for precise numbers.
Boundaries: original/snapshots/memory immutable; no unrelated stock/infra changes.
Historic sections labelled as prior dates, not rewritten as fresh evidence.
Validation: every current external property maps to dated official URL; licence
versus access versus approval distinctions, no claim of all EA products lacking
climate data. CIBSE exact redistribution terms remain unavailable, not OGL.
Completion evidence: full diff and per-criterion audit.
Unresolved: owner approval and paired historical record bounds.

<!-- rpi:phase id=P03 -->
## P03: Validation and reconciliation

<!-- rpi:task id=P03-T01 -->
### P03-T01: Tests, links, artifacts and handoff

Context: local evidence delivery does not complete #178.
Intent: reconcile task markers/details/changes, tests and issue audit before Review.
Targets: P01-P02 outputs, tracking only.
Dependencies: P01/P02.
Validation: focused unit discovery; actual-file invocation and second independent
arithmetic calculation; report deterministic hash; Markdown local links/anchors
and git diff --check; ensure no raw public or private dataset committed.
Completion evidence: exact commands, results, planned deviations, immutable-path
checks and session phase completion.
Unresolved: same human/access gates; not silently waived.

Completion: eight unittest methods pass, Python compileall passes, actual report
reproduces byte-for-byte, independent Decimal calculation confirms every extremum
and occurrence, all six added local link targets/anchors resolve, append-only
log prefix and immutable/excluded paths verified. git diff --check passes.
Initial full historic-log link scan found a pre-existing retired mvp anchor;
changed-link validation excludes that unrelated historical issue.
