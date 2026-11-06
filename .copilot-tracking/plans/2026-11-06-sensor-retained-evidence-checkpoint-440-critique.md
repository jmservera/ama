---
title: Sensor retained-evidence checkpoint 440 plan critique
description: Independent read-only critique of the plan and details for the additive retained-evidence qualification of the Sixteenth sensor checkpoint
ms.date: 2026-11-06
---

## Metadata

* Task ID: 440-sensor-retained-evidence-checkpoint
* Critique date: 2026-11-06
* Plan: .copilot-tracking/plans/2026-11-06-sensor-retained-evidence-checkpoint-440-plan.md
* Phase details: .copilot-tracking/details/2026-11-06-sensor-retained-evidence-checkpoint-440-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context: documentation-only additive qualification of the Sixteenth checkpoint; no source or runtime change, no push.
* Evidence considered: the research, plan and details records above; read-only spot checks of /mnt/ama-gates/g188-r20-1106 (receipt.json, receipt.sha256, 0176-mssql.log, api-all.json), /mnt/ama-gates/e188-r20-1106 (sql-sensor.log, sql-sensor-summary.json, cleanup.json) and the Sixteenth section (lines 4666-4733) of docs/architecture/cutover-evidence-pack.md.
* Assessment boundary: credibility of the plan and the research claims it carries. Not re-read: browser results, the other three image scans, the /tmp native log, git pins and blobs, source line numbers.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Requirement: consume retained evidence | Covered | Receipt sha256 e5751469... equals receipt.sha256; status passed, scope full, jobs 1, failure null, 205 commands, 17 groups, skipped empty, image_cache fresh, resume_eligible false, sealed 2026-11-06T08:47:53Z, head 6887377, tree 30167885..., base and merge base bb3a3b03... all confirmed |
| Requirement: three SQL kinds | Covered | 0176-mssql.log: 285 tests, OK (skipped=1). sql-sensor.log: 68 tests, OK. sql-sensor-summary.json: skipped_mentions 0. cleanup.json: removed-and-absent-confirmed. Package skips (2363/226, 1941/338) not re-read |
| Requirement: image risk 42 / 40 High / 2 Critical / fixable 0 | Partial | api-all.json confirmed 40 HIGH, 2 CRITICAL, 0 with FixedVersion, but those 42 are vulnerability instances across only 17 unique IDs; other three images not re-read (see PC-002) |
| Requirement: hosted-only and unproven items | Covered | receipt hosted_only lists the four items as stated |
| Requirement: CONTINUE, HOLD, gates, lanes | Covered | Matches the Sixteenth recommendation; no contradiction |
| FR1, P1-T1 | Partial | Contents list is good but lacks anchoring of the receipt-versus-parent-head boundary and exit-code derivation (PC-001, PC-004) |
| FR2, P1-T2 | Partial | README placement is stated two ways (PC-005) |
| AC1 | Partial | No method is stated for proving "every numeric claim matches" (PC-006) |
| AC2, AC3, P2-T1 | Covered | Additions-only, name-diff and ignored-inclusive checks are adequate; no heavy command |
| Critique disposition | Missing | Plan says Pending (PC-007) |

## Verdict

* Verdict: Revise
* Rationale: no Critical or High defect. The evidence is real and the core figures reproduce. Medium findings would let the new subsection make an imprecise or unsupported claim (non-retained log, "42 findings" wording, partly read browser results) and are cheap planner corrections.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Exit-code claim relies on a non-retained log and an unverified attribution

* Related IDs: research native log row; P1-T1; AC1
* Evidence: receipt.json commands all carry exit_code; I counted 192 at 0 and 13 at 1, matching the research. The attribution of the 13 to "expected probes" comes from /tmp/rpi-188-r20-postfull-handoff-r59-20261106.log and the child's account; that path is under /tmp and is not retained evidence (a copy exists at /mnt/ama-gates/e188-r20-1106/original188-postfull-handoff-r59.md, not read by the research).
* Concern: the subsection could cite an ephemeral /tmp file as evidence, and could present which 13 commands exited 1 as established when it is not derived from the receipt list.
* Impact: an unreproducible citation in a durable evidence pack; a passed receipt with 13 non-zero exits needs a traceable explanation or an explicit "unexplained here" label.
* Smallest useful change: state 192/13 as receipt-derived; either list the 13 argv or group names from receipt commands, or label the "expected probe" reason as a child account; cite the retained /mnt copy, not /tmp.
* Action owner: planning parent
* Exact resolving evidence: subsection text with the 192/13 counts, the attribution class, and no /tmp path cited as evidence.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: "42 findings" are instances, not unique vulnerabilities

* Related IDs: research image scans row; requirement image risk; AC1
* Evidence: api-all.json has 42 instances (40 HIGH, 2 CRITICAL), 0 fixed versions, but 17 unique VulnerabilityIDs. The research says each of the four images has 42 but I verified only the api image.
* Concern: unqualified "42 findings" can be read as 42 distinct CVEs and also hides that the count counts package instances. Per-image equality for agents, orchestrator and importer is unverified by me.
* Impact: misleading risk magnitude in a pack that must not overstate or understate.
* Smallest useful change: word it as "42 vulnerability instances (N unique IDs) per image, scanner output, fixable 0, not security-clean"; compute unique IDs per image at write time and say they were read from the four *-all.json files.
* Action owner: planning parent
* Exact resolving evidence: subsection table with instance and unique-ID counts for all four images and a note that the 39-to-42 cause is unverified.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Partly read browser results must not become evidence

* Related IDs: research browser row; plan follow-up; AC1
* Evidence: research states only the first eight scans of case-journey-results.json were read; the file exists in g188-r20-1106 and is read-only cheap to read in full.
* Concern: the plan lists browser results as deferred to a coordinator, but the subsection scope (FR1) does not say whether browser data is included. A partial reading cited as "zero violations, one incomplete" would be an unsupported generalisation.
* Impact: false assurance on accessibility; the repository forbids claiming conformance without evidence.
* Smallest useful change: either read the whole file (and regulatory-ux-results.json if mentioned) and state the totals, or exclude browser results from the subsection and list them as unread. State that axe results are not WCAG conformance acceptance.
* Action owner: planning parent
* Exact resolving evidence: subsection either has full-file counts with the read method, or an explicit "not assessed" row.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Receipt-versus-parent-head boundary and diff scope need explicit text and acceptance

* Related IDs: research contrarian wave and fresh pins; FR1; AC1
* Evidence: receipt identity head 6887377, tree 30167885... equals the parent tree 30167885... in the Sixteenth; the parent commit is 9476dc96. The research reports 99 files +1967/-81 against the Sixteenth's 19 files +1169/-81; these were not re-derived by me.
* Concern: the plan has no acceptance criterion requiring the subsection to say that the receipt is a gate for the child head and not a new gate at the parent commit, even though tree equality holds; and the 99-file versus 19-file difference could be read as a contradiction with the Sixteenth if not labelled as a different scope (source and tests versus all files including tracking records).
* Impact: relabelled receipt, or a flagged contradiction with an immutable earlier section.
* Smallest useful change: add an AC that the subsection states head versus parent identity, tree equality and the scope of each diff figure, and records the difference as a flagged scope difference rather than a correction of the Sixteenth.
* Action owner: planning parent
* Exact resolving evidence: AC text plus subsection sentences; P2-T1 pin recheck output.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: README insertion point and branch context are ambiguous

* Related IDs: plan FR2; details P1-T2; details Context
* Evidence: plan says "after the Sixteenth or provenance paragraph"; details says "after the R10 paragraph". The worktree branch is docs/queue-dispatch-protocol-checkpoint-440 (git branch confirmed), a queue name for a sensor task, while the plan says the target is feat/discovery-assurance-integration-123.
* Concern: two placements, and no stated rationale for committing sensor work on a queue-named branch.
* Impact: inconsistent execution and possible append-only check confusion; branch lineage is unclear for a reviewer.
* Smallest useful change: choose the details wording, and record in Changes why this branch is used and that it is the local handoff branch for the same #1222 workstream.
* Action owner: planning parent
* Exact resolving evidence: plan and details use one placement; the Changes record states branch rationale.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: AC1 has no verification method; supplement context incomplete

* Related IDs: AC1; P2-T1; research SQL supplement row
* Evidence: P2-T1 lists pins, diffs, anchors, ASCII and frontmatter but no numeric re-extraction. sql-sensor-summary.json lists the five selectors; the supplement ran outside the receipt command list in a separate container with its own cleanup record.
* Concern: AC1 cannot be demonstrated from P2 as written. The subsection should also state that the 68-test supplement is not a receipt command and has no link to the receipt hash, and record its selectors.
* Impact: the central acceptance criterion would rest on assertion.
* Smallest useful change: add to P2-T1 a read-only recomputation (sha256 of receipt, counts from receipt.json, tail of the two SQL logs, image counts from JSON, sql-sensor-summary.json) and record the outputs in Changes; add selectors and "outside receipt" to FR1.
* Action owner: planning parent
* Exact resolving evidence: Changes record with the recomputed values equal to the subsection figures.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Plan critique disposition still Pending

* Related IDs: plan Critique Disposition
* Evidence: plan states "Pending: critique not yet run".
* Concern: the plan must record this critique's outcome and how each finding was applied or rejected before P1.
* Impact: critique-to-implementation traceability.
* Smallest useful change: after revising, record Revise outcome and per-finding disposition PC-001 to PC-006 without another critique pass.
* Action owner: planning parent
* Exact resolving evidence: plan Critique Disposition lists each PC with applied or rejected.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Additive append at the end of an append-only pack, following the existing "provenance qualification" precedent; no new checkpoint number, no heavy execution, no new issues.
* Core figures reproduced from retained files: receipt hash and identity, 285 with one skip, 68 with zero skips, cleanup confirmed, hosted-only items, 40 High and 2 Critical in the API image with none fixable.
* Residual risk accepted by design: the cause of the 39-to-42 increase and the receipt at the intended parent head stay with the #188 lane.

## Questions or Blocking Evidence Gaps

* None. No user decision is required.

## Limitations

* Spot checks only; git pins, blob ids, document status, source line numbers, browser files, other image scans and package skip counts were not re-read.
* Commands run were read-only; no tests, SQL, containers, scanners or installs.

## Skill files read and commands run

* Skill files read: /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/rpi/rpi-plan-critique/SKILL.md and /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/rpi/rpi-plan-critique/templates/plan-critique.md.
* Records read with view: the research, plan and details records; the Sixteenth section of docs/architecture/cutover-evidence-pack.md (lines 4666-4735).
* Commands run (all read-only): sha256sum of receipt.json with cat of receipt.sha256; tail of 0176-mssql.log and sql-sensor.log; head of cleanup.json; a python3 one-off that loaded receipt.json and printed top-level keys; ls of the gate folders and the /tmp log path; grep -n of "^## " and "Sixteenth" in the pack with git status --short and git branch --show-current; python3 reads of receipt.json (identity, sql, hosted_only, exit-code counter, images keys) and of api-all.json (severity, fixed-version and unique-ID counts), plus sql-sensor-summary.json and git log -1. One python3 call failed with a wrong path (e188 api-all.json) and was rerun against g188.

## Recommended Next Action

* Highest-impact finding: PC-002 (instance versus unique-ID wording; shared Medium with PC-001, PC-003, PC-004)
* Action owner: planning parent
* Smallest next action: revise the plan and details to cover PC-001 to PC-007 directly, then proceed to P1 without another critique
* User response required: no

## Relevant artifacts

| Path | Description |
|------|-------------|
| [.copilot-tracking/research/2026-11-06-sensor-retained-evidence-checkpoint-440-research.md](.copilot-tracking/research/2026-11-06-sensor-retained-evidence-checkpoint-440-research.md) | Research record |
| [.copilot-tracking/plans/2026-11-06-sensor-retained-evidence-checkpoint-440-plan.md](.copilot-tracking/plans/2026-11-06-sensor-retained-evidence-checkpoint-440-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-11-06-sensor-retained-evidence-checkpoint-440-details.md](.copilot-tracking/details/2026-11-06-sensor-retained-evidence-checkpoint-440-details.md) | Phase details under critique |
| [docs/architecture/cutover-evidence-pack.md](docs/architecture/cutover-evidence-pack.md) | Pack containing the Sixteenth section |

## Next Steps

* Return to the planning parent: apply PC-001 to PC-007 as direct corrections, then proceed. No user command is needed.
