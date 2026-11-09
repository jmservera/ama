<!-- markdownlint-disable-file -->
# Research: PR 1295 C4 current-main source freshness (2026-11-09)

* Task: `pr-1295-c4-current-main-freshness` (parent `pr-1295-c3-navigation-corrections`). Qualified `hve-core-all:rpi-agent`, Claude Sonnet 5.5, worktree `docs/demo-recovery-pr1295-1109`.
* Research disposition: executed (read C3 handoff, both C3 independent findings, anchor and hash contract of both diagram generators, dry-run overlap of main).
* Planning Readiness: Ready.
* Correction budget: cycle 4 of 5 total. C1 to C3 and every adverse record are retained, nothing is reset or renewed; one cycle remains after C4. No extension is inferred.

## Identities (read at start)

| Item | SHA |
| --- | --- |
| Frozen clean start HEAD | `5c13be8029216613a5652f48e9d9fb7a69ed65ff` (tree `5fc6952ae67cbc323bd2c7345e6b9678d6710db1`) |
| Coordinator-pinned merge target | `23e944c1fccf0c4578e7beb0740ddd55c3f935b2` |
| `origin/main` after fresh fetch | `df8e858b2150198e5e22c73d224a0d3592c73daa`, a descendant of the pinned target |
| Merge base with HEAD | `f3532b02c01d7d21dadfe0d18f4f18b9f7502e07` |
| Owner remote head | `0bcf55da1d516c82567e6eb44357343054c69b76` (ancestry preserved, not touched) |

`df8e858b2` differs from the pinned target only in `.github/rubric/scores/latest.json` (score record, 5 lines). The coordinator pinned the reviewer base, so the pinned `23e944c1` is merged and the rubric-only descendant is reported, not silently substituted.

## Inputs read

* Common rules, C3 handoff, `independent-pr1295-c3/readiness-findings.json` (approve with comments, one Medium carried hosted conflict at the old owner head) and `functional-findings.json` (approve, zero findings; scoped to `5c13be80`, no certification of current main).
* Both C3 defects are closed. The hosted conflict at `0bcf55da1` is a separate post-publication gate, not a local defect and not an old-head CI prerequisite.
* Readiness recommended actions: reconcile ordinarily with the target, inspect the concrete IoT 1304 overlap, run bounded generator `--check` and locator/hash checks, refresh only proven stale derivatives, preserve both append-only histories, keep frozen items.

## Concrete overlap (diff of `HEAD...origin/main`, 170 files, 4697 insertions)

Main adds PR 1304 and earlier live-simulator/device-provision work. The paths the diagram generators bind (whole-file SHA-256 plus a line anchor) that differ on main:

| Generator input | Anchor | Current line | Target line | Evidence |
| --- | --- | --- | --- | --- |
| `src/core/src/zava_forward/core/sensor_consumer.py` | `class SensorConsumer:` | 196 | 219 | `git show` of both revisions |
| `src/core/src/zava_forward/core/sensor_analysis_store.py` | `def analyse_retained(` | 19 | 21 | same |
| `infra/live-simulator-job.bicep` | `sourceAt(..., 18, ...)` | description at 18 | description at 18 | file changed on main, line text unchanged, hash changes |
| `src/api/README.md`, `src/core/README.md` | heading anchors | to be located | to be located | both changed on main |

Other main-changed paths (`docs/reference/README.md`, `docs/reference/log.md`, `docs/reference/research/iot-sensor-analytics-research-plan.md`, `infra/README.md`, API live files) are either append-only histories (preserve both sides), or bound by `sensors` research-plan hash in `build-architecture.mjs`. The architecture generator binds whole-file hashes, so a hash can go stale even where the anchor text is unchanged; the readiness review therefore required an actual check, not an inference from the anchor line.

## Authorization boundary

* Existing authority covers metadata, derivatives, catalog and receipt refresh only where the actual check proves them stale. A references-only correction must be shown to keep structure, text, geometry and PNG bytes unchanged. If any visual or package input changes, that change is reported and not rebuilt automatically.
* The C3 contracts stay: 13 mapping cases, 55 slides, 55 non-empty reciprocal notes, 108 fixed actions, protected cost bytes. They are re-asserted only if a deck input changes.
* Frozen and unchanged: protected QX manifest sentence "All 54 page numbers" (`slides.json:3029`), runbook page numbers (`docs/capstone/demo/runbook.md:109`). Current-versus-baseline wording may be documented outside the protected material and never presents baseline numbers as current.
* The owner's "go ahead on safe demo assumptions" does not approve live Azure, model, native, assistive technology, notch, rehearsal, human, professional or financial changes.

## Not in scope

Full gate, private `ZF_DATA`, global installs, price research, cloud, model calls, push, PR, issue, board, merge, rebase, force.

## Planning inputs

Ordinary no-fast-forward merge of the pinned target; conflicts (if any) resolved preserving both histories; run bounded architecture `build`/`update` and resident journey generators in `--check` mode, locator/source-hash checks and architecture node tests; refresh only what is proven stale; compare invariance; targeted deck contract checks only if a deck input changes; docs, KB index and log, tracking records.
