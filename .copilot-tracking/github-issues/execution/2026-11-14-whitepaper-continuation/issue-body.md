Track the remaining experiment-recovery and manuscript-finalization steps for the v19 whitepaper (*Everything but the Software: Feature-Driven Decay in an Agentic Coding Loop*) on branch `docs/whitepaper-study-results` (commit `4f39fdb6`, 66-page `main.pdf` SHA-256 `6b00bc227ccd56b89c352d1cea57871a85fd55aa6bf000eb75385b0a64a45977`, 67/67 authoring tests passing) so work can resume on another machine.

## Acceptance Criteria

- [ ] Preserve the stopped 313/315 study baseline (`state.json` SHA-256 `fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f2de1`) in `ama-thought-mve-fallback-recovery` without in-place mutation.
- [ ] Add a 15th disclosed recovery transition in `harness/study.py` and `harness/prepare_estimation_recovery.py` in `jmservera/ama-thought-mve` that copies `.study/pilot-estimation` to a new recovery directory, retains both 300-credit unknown-charge holds in `recovery_hold`, and resets `pilot-estimation-gemini-4-argon-E-15` and `pilot-estimation-gpt-6.1-sol-C-20` from `quarantined` to `partial` at their verified checkpoints.
- [ ] Run `harness/study.py` before the active study deadline (`1795318710.65`, `2026-11-22T03:38:30Z`) to complete the 14 remaining steps (`11` steps in `gemini-4-argon-E-15` from `f06-feature` and `3` steps in `gpt-6.1-sol-C-20` from `f10-feature`).
- [ ] Update `intervention-coverage/v1` to attest all 315 completed trajectories, re-export `results/pilot-estimation/` so `primary_unassisted_frame_complete` and `primary_estimates_available` become `true`, and inspect `runs/pilot-estimation-gpt-6.1-sol-{B-08,C-14}/steps.jsonl` to decide whether their `cr1-change` non-binary hidden-test outcomes remain `null` bounds or are adjudicated.
- [ ] Replay the 4 newly completed endpoint packets ($P_{10}$ and CR1 for `E-15` and `C-20`) via `judging/execute.py` and run 8 `gpt-6-luna` calls (`4 packets x 2 repeats`) in `judging/judge.py` to complete 630/630 packets.
- [ ] Publish the final deposit manifest in `jmservera/ama-thought-mve` binding `osf-v4-2026-10-31.tar.gz`, `osf-v6-2026-11-02.tar.gz` and `osf-v7-2026-11-07.tar.gz` to the 7 November 2026 OSF registration (`osf.io/xcpt4`) and final commits/hashes while excluding `.study/evidence-vault-2026-11-13/`, raw packets and credentials.
- [ ] Refresh `docs/capstone/thought-leadership/everything-but-the-software/main.tex`, `anc/experiment-protocol.tex`, `anc/measurement-provenance.tex` and `anc/supplement-integration.json` with the 315/315 results, resolve the remaining 11 `TODO(author)` markers, rebuild `main.pdf`, and pass all authoring tests.

## Unblocking the Two Quarantined Trajectories

### 1. Exact State of the Quarantined Cells

| Trajectory | Arm / Model | Completed steps | Verified checkpoint (`step` / `head`) | Remaining steps | Current blocker in `state.json` |
| --- | --- | --- | --- | --- | --- |
| `pilot-estimation-gemini-4-argon-E-15` | Arm E / `gemini-4-argon` | 10 / 21 (`f01`–`f05` feature + repair) | `f06-feature` at `763a9a36eb7191d023601c35fcfa049e1c1894b5` | **11 steps** (`f06-feature`..`f10-repair` + `cr1-change`) | `status = "quarantined"`; attempt `...-f06-feature-1` has `status = "infra_failed"`, `supervision.action = "quarantine_cell"`, ledger `status = "quarantine_hold"` (300 reserved credits) |
| `pilot-estimation-gpt-6.1-sol-C-20` | Arm C / `gpt-6.1-sol` | 18 / 21 (`f01`–`f09` feature + review) | `f10-feature` at `81e23369f6125314bab89ac52361b44da8339f60` | **3 steps** (`f10-feature`, `f10-review`, `cr1-change`) | `status = "quarantined"`; attempt `...-f10-feature-1` has `status = "recovery_interrupted"`, ledger `status = "recovery_hold"` (300 reserved credits) under `FALLBACK_RECOVERY_STATE_SHA256` (`kind = "fallback_metadata_quarantine"`) |

### 2. Code Gates in `jmservera/ama-thought-mve`

1. `StudyController.go()` (`harness/study.py` line 2096) skips cells with `status == "quarantined"`, and `new_attempt()` (line 1819) raises `StudyError("Quarantined cell cannot replay an unresolved request")`.
2. `validate_supervisor_state()` (`harness/study.py` lines 572–575) requires `cell.get("status") == "quarantined"` whenever a ledger entry has `status == "quarantine_hold"`.
3. `validate_recovery_state()` (`harness/study.py` lines 1084–1096) requires `cell.get("status") == "quarantined"` and `cell["attempts"][-1] is selected[-1]` for any attempt in `quarantine_only` (`kind == "fallback_metadata_quarantine"`).

### 3. Step-by-Step Recovery Procedure

1. **Preserve baseline:** Keep `ama-thought-mve-fallback-recovery/.study/pilot-estimation/state.json` (`fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f2de1`) untouched.
2. **Add 15th recovery transition:** In `harness/study.py` and `harness/prepare_estimation_recovery.py`, register `fb39a46fc36f33f62f3286fd517b63bb09787e9c7bcd7d276c4a362f2de1` in `recovery_state_hashes()` / `recovery_incident()` (5,341 completed steps, 5,357 attempts). Copy `.study/pilot-estimation` into a new recovery working directory, convert `gemini-4-argon-E-15-f06-feature-1` from `quarantine_hold` to `recovery_hold` (`status = "recovery_interrupted"`), allow new attempts after `quarantine_only` when an explicit owner quarantine-unblock approval (`accept_fresh_retry_reservation = true`, `accept_fresh_retry_time_allowance = true`) is present, and set both cells' `status` to `"partial"` at their checkpoint HEADs (`763a9a36...` and `81e23369...`).
3. **Execute remaining 14 steps:** Run `study.py` in the new recovery directory (`git reset --hard <checkpoint.head> && git clean -qfd` runs automatically per cell before resuming `f06-feature` and `f10-feature`). Maximum additional reservation is $14 \times 300 = 4,200$ AI credits.
4. **Re-export and finish judging:** Update `intervention-coverage/v1` to 315 trajectories, re-export `results/pilot-estimation/` (flipping `primary_estimates_available` to `true`), and run `judging/execute.py` + `judging/judge.py` on the 4 new endpoint packets (8 `gpt-6-luna` calls).

## Remaining Manuscript and Deposit TODOs

1. **Statistical dependence & amendment chronology** (`docs/capstone/thought-leadership/everything-but-the-software/anc/experiment-protocol.tex` line 519): Record the dated chronology of the 5-arm/$n=21$ amendment and recovery epochs relative to outcome inspection, and either adopt the independent within-model/arm bootstrap by author decision or add a 5-arm $(\mathrm{model}, \mathrm{replicate})$ block-bootstrap sensitivity check in `harness/analyze.py`.
2. **GitHub deposit manifest & archive correspondence** (`docs/capstone/thought-leadership/everything-but-the-software/main.tex` line 1390): Add `DEPOSIT_MANIFEST.json` or release notes in `jmservera/ama-thought-mve` binding `osf-v4-2026-10-31.tar.gz`, `osf-v6-2026-11-02.tar.gz` and `osf-v7-2026-11-07.tar.gz` to `osf.io/xcpt4` and final commits/hashes.
3. **Unlogged historical case CLI/reviewer/build IDs** (`main.tex` line 346): State in Section 3.3 prose that early interactive/CLI case sessions did not log backend build identifiers, and remove the comment.
4. **Scoped original-source verification sign-off** (`main.tex` line 1256): Author-confirm the original-source register in `anc/revision-report.md` (including abstract-only/metadata limits for Besker, Echoes of AI, and the SEC order PDF) and remove the comment.
5. **Provenance-excerpt & participant-anonymity sign-off** (`main.tex` line 1257): Confirm publication approval for the selected provenance excerpts and remove the comment.
6. **Manager / CELA clearance note** (`main.tex` line 294): Move the manager approval and 27 October 2026 CELA submission statement into final prose once process coverage for the current draft is confirmed, and update `test_given_finalization_when_approval_recorded_then_cela_clearance_is_not_invented` in `anc/test_measurement_provenance.py`.
7. **Submission date & reviewer acknowledgements** (`main.tex` lines 60 and 1145): Set final `\date{...}` and reviewer acknowledgements at submission.
8. **Inactive `\else` branch placeholders `PF1`–`PF3`** (`anc/experiment-protocol.tex` lines 1004–1006): If zero `TODO(author)` strings are desired in source, retire the inactive `\else` branch and update `check_manuscript()` in `anc/test_conceptual_figures.py` lines 116–117.

## Related

- Branch: `docs/whitepaper-study-results` (head commit `4f39fdb6`)
- Manuscript: `docs/capstone/thought-leadership/everything-but-the-software/main.tex`
- Protocol slice: `docs/capstone/thought-leadership/everything-but-the-software/anc/experiment-protocol.tex`
- Revision record: `docs/capstone/thought-leadership/everything-but-the-software/anc/revision-report.md`
