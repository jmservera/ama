---
title: Issue 1845 withdrawn-sensor canary false positive research
description: Research for a test-only repair of short decimal canary searches that collide with numeric timestamp metadata
ms.date: 2026-11-17
ms.topic: reference
---

## Status

* Research disposition: executed.
* Planning Readiness: Ready.
* Base: `main` f1df574bba2b94cd83bb2a783079ec94cd584c90, branch
  `test/withdrawn-sensor-canary-1845`.
* Validation tier: FULL, chosen conservatively because the test guards a
  privacy control. Any focused downgrade is a proposal for coordinator
  assessment after the actual diff and evidence, not a publication exemption.
* HVE behaviour testing: not applicable (no agent, prompt, instruction or skill change).
* Web UI: no web change is scoped.

## Scope from the task brief

Issue #1845 reports that `test_quality_sensors.Http.test_withdrawal_withholds_uncited_derived_text_and_edited_output`
(lines 859-879) searches serialized detail/list/export/sensors JSON for `23.7`
and `24.9` after consent withdrawal. The retained failure matched `23.7` only
inside numeric timestamps `1794924123.7340033` and `1794924123.7119958`. The
brief treats this as a confirmed test false positive, not a leak. The separate
#1641 consent-regrant defect is not cleared. The immutable nomination receipt
is not mounted and is not read, overwritten or claimed.

## Heavy-resource boundary

No heavy admission. No browser, SQL, Docker, scanner, image or full gate runs
in this launch, and `/tmp/ama-rpi-heavy.lock` is not queued, polled or bypassed.

## Witness disclosure

The persisted opening state and this artifact existed before `research-open`
was recorded (seq 2, ok); source orientation on the test file came after it.

## Findings

### Test under repair (`src/api/tests/test_quality_sensors.py`, class `Http`)

* `_after_withdrawal(tid)` returns four projections: `detail`, `list`,
  `export` and `sensors`. The test at lines 863-882 serializes each with
  `json.dumps` and asserts `assertNotIn("23.7" | "24.9", text, name)` after
  `set_consent("declined")`.
* The mock provider (`CapturingProvider`, lines 39-80) writes the leak into
  `summary` ("Indoor 23.7 degC was recorded."), `unknowns` ("Whether 23.7 degC
  is typical.") and `findings[0].text` ("Reading of 23.7 degC."). The edited
  output is "Edited: indoor 24.9 degC was recorded." Every canary therefore
  appears as a standalone decimal token in text, never inside a longer number.
* The test already carries positive controls before withdrawal
  (`assertIn("23.7", json.dumps(p["output"]))` and the `24.9` detail check),
  and post-withdrawal checks that findings are empty and `edited_output`
  provenance is stripped. Those stay.

### Source of the incidental numbers

A probe (scratch test subclass in the run-local work folder, not committed)
ran the same flow and listed float-valued metadata in the projections:
`created_at`, `as_of`, `not_before` and `at` are epoch seconds with a
fractional part (for example `1794926317.129992`) in `detail`, `list` and
`export`; `sensors` had none. Any epoch whose seconds end in `23` with a
fraction starting `.7` (or `24` and `.9`) contains `23.7` (or `24.9`) as a
substring, which is exactly the retained failure (`1794924123.7340033`,
`1794924123.7119958`). The probability is small per run but not zero, and it
rises with the number of timestamps serialized.

### Deterministic reproduction (no clock dependence)

`work/scratch/repro_1845.py` serializes constructed metadata
`{"created_at": 1794924123.7340033, "as_of": 1794924123.7119958, "at": 1794924124.9123}`:
the old substring check returns True for both `23.7` and `24.9`. A
digit-bounded decimal match, `(?<![\d.])VALUE(?!\d)`, returns False on that
metadata and True for "Indoor 23.7 degC was recorded.", "Edited: indoor 24.9
degC was recorded.", a bare numeric reading `"temperature_c": 23.7` and
"(23.7)". The baseline target test passed on this head (1 test, 0.9 s), which
confirms the defect is a rare collision, not a constant failure.

### Options considered

| Option | Verdict |
| --- | --- |
| Digit-bounded decimal match applied to the same four projections | Chosen. Keeps whole-body coverage, still catches bare numeric values, no field-specific knowledge. |
| Search only the exact leaked phrases | Rejected: narrower than the current check; a bare numeric leak would pass. |
| Strip `created_at`, `as_of`, `not_before`, `at` before searching | Rejected: blanket metadata stripping is out of scope and could hide a leak in those fields. |
| Patch `time.time` to a fixed value | Rejected: disturbs sealing buckets and consent timing; adds coupling without proving the matcher. |
| Retry, skip or xfail | Rejected by the brief. |

### Chosen shape (proposal for Plan)

* One small module-level helper in the existing test file that matches a
  decimal canary only when it is not part of a longer number.
* Use it for the post-withdrawal loop and for the pre-withdrawal positive
  controls, so the detector is shown live on the real projections.
* A small standalone `unittest.TestCase` in the same file with constructed
  metadata: clean timestamps accepted, actual original and edited text
  detected (including text sitting beside the colliding timestamps).
* No production, auth, provider or gate file changes.

## Validation tier

FULL, by the brief's conservative choice, because the change touches a
privacy-regression guard. Basis for a possible focused downgrade (coordinator
assessment only): the change keeps the same four projections and the same
canaries, narrows only the substring semantics to digit-bounded decimals, and
adds positive controls. This launch runs only targeted preflight; the
coordinator runs the final full gate on the frozen candidate.

## Adverse and open evidence

* The retained failed receipt is not mounted; the failure facts come from the
  issue body and brief and are not independently re-observed.
* The collision itself was not reproduced through the live service (that
  would need clock luck); only constructed metadata reproduces it, as the
  brief directs.
* #1641 (consent regrant) is not cleared or touched. Browser and SQL groups
  for nomination #1837 are not covered by anything here.
* Environment: venv installed editable from a `git archive` of HEAD under the
  run work folder; production code is identical to the worktree because the
  change is test-only. Tests run from the worktree test directory.
