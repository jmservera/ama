<!-- markdownlint-disable-file -->
# Phase details: iot-trace-docs-156-1112

## Phase 1: register section (draft text)

Insert before `[bc-prd]: ../../../prds/zava-forward-retrofit-programme-demonstrator.md`:

```markdown
### Demo IoT-to-UI source trace update (2026-11-12, Refs #156, #184, #187, #189, #134)

This dated update is additive. It reads current source at `main` `e4854bd7e` and
does not change the 2026-10-18 snapshot rows above (#187 and #189 there still
read "interface unspecified", which was true at that date) or the executable
register (still 74 screen issues, 0 supplied designs, blocked). It is
documentation of what static source shows, not a design, a test result, an
observation or an approval. Issue states were read on 2026-11-12.

| Item | Source-read finding (evidence class: static source, not observed) | Design artefact and gap |
| --- | --- | --- |
...five rows...
```

Rows (final wording lives in the changes record):

1. #189 (O, criterion 3 unticked): administrator screen `#/simulator` (`web/app.js`, `web/simulator-control.js`), API `simulator_admin.py` (PR 1313), local browser check `checks/simulator_control_browser_check.py` on a synthetic store. Budget alert always "not recorded, not verified live"; no deployed job started. Design Not supplied; no accessibility, human or live evidence.
2. #187 (C, criteria ticked per public issue state): partial control. Start/stop, 100-home cap, 14-day window in `live_control.py` and the screen; replay and speed exist as library code (`sensor_stream.py`, `iot_stream.py`); no pause control or operator surface for replay, speed or faults found in the bounded trace. Closed state and source not reconciled. Design Not supplied.
3. Employee Quality sensor panel: `sensorPanel` in the "Quality and handover" tab (`web/app.js`), local check `checks/quality_sensors_browser_check.py` on a mock provider. `employee-case-workspace-redesign.md` names `qualityPanel` and `handoffPanel` only. Design Not supplied; no IoT-to-UI flow specification.
4. Cadence: source 5 minutes (`SLOT_SECONDS = 300`, simulator docstring, Bicep `*/5 * * * *`); owner target 1 minute (runbook 2026-11-12) is a target, unverified. Gap only; no campaign reopened.
5. Five-home AI scope: not verified by a bounded, nonexhaustive trace (`assistants.py`, `sensor_view.py`, `infra/main.bicep`); no reference to the simulator cohort found in those files; five-home limit is the simulator control cohort per runbook; `enableApiAi` default false. No global-absence claim; orchestrator and agents paths not traced.

Closing paragraph: no new design approval; C1 unticked; Fluent 2, WCAG baseline, content standard, manual paths unchanged; D1/source-correction UNKNOWN unaffected; no model/deployment/live run.

## Phase 2: index and log

* Index row after line 1057 of `docs/reference/README.md`: link to the new section anchor, one-sentence summary, date 2026-11-12, "Not run" tool statement.
* Log: `## [2026-11-12] update | Demo IoT-to-UI source trace rows (Refs #156 #184)` appended at end, three bullets, evidence pointer.

## Phase 3: verification commands (read-only)

* `git diff --numstat` and `git diff -U0 | grep '^-[^-]'` must show no removed lines.
* Anchor/link check by reading; `grep -nP '[^\x00-\x7F]'` on added lines; `grep -n ' — '` none.
* Re-read each cited path with `grep -n` at the end.
