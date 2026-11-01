<!-- markdownlint-disable-file -->
# Task Research: Issue 441 resident portal documentation closure verification

* Date: 2026-11-01
* Task slug: issue-441-closure-verification
* Branch/worktree: docs/resident-portal-integration at origin/main 36a1d0da25cf
* Research disposition: executed
* Planning Readiness: Ready (evidence-only slice; criterion 5 remains a human gate)

## Scope

Issue #441 integration was delivered by #442 (merged 2026-10-24, head cc5caf76) and #454 (merged 2026-10-27, head 3000b398). The 2026-10-31 closure audit left criteria 5 and 9 unticked. This slice re-verifies the delivered integration on current main with focused checks and records what remains human-gated. No product document is edited.

## Evidence

| Check | Result |
| --- | --- |
| Overlap PRs/issues #426, #424, #439 | All MERGED (2026-10-28, 2026-10-28, 2026-10-27); no open dependency or ordering constraint remains |
| Custody packages (session b9cc4727, resident-portal-requirements-20261023) | 28 files located in adr/, brd/, prd/; sha256 prefixes recorded in the changes artifact |
| Diagram custody | Excalidraw, SVG and PNG in the draft package are byte-identical to the copies under `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/` |
| BRD IDs | FR-053 to FR-062 present as requirement rows; AC-104 to AC-126 all present as inline `AC-nnn:` criteria |
| PRD IDs | FR-062 to FR-071 and AC-111 to AC-140 all present as table rows; FR/AC tables show no duplicate definition rows beyond the traceability matrices |
| Formula | 90 cases/week x 8 weeks = 720 WIP; 84 baseline h; 50% x 65% -> 27.3 gross; 27.3 - 3.6 - 0.96 - 2 - 6 = 14.74 net; 48 h one-off separate; -1.594/94.333 labelled combined sensitivities, author judgement (PRD lines 2780-2792; addendum line 73) |
| FR-044/AC-084 | Per-message named review is the stated default (PRD lines 960-975, 1045-1053; BRD RULE-018, OD-53); routine exception is proposed, OFF, subject to OD-53 and separate RULE-020 release |
| Protected files | `docs/case_study_48_original.md` and `docs/reference/memory.md` unchanged since base 140d8f49 |
| ADR registry | Proposal remains id-null UNREGISTERED (`resident-service-unregistered-proposal.md`); `docs/adrs/` holds 0001-0006 only; no guessed ID |
| Link check (BRD, PRD, addendum, architecture and reference READMEs, discovery text equivalent) | 5 inherited broken relative links, none introduced by #441: addendum to `capstone/deck/agents-in-retrofit-process.svg` and `capstone/pitch/tokenomics-pitch-brief.md`; architecture README to `capstone/deck/zava-forward-executive-draft.pptx`; reference README (2) to `presentations/ama-mentor-progress-review.pptx`. Introduced by commits 0f657342, a75bbdff, acafc6ee. Left unchanged per scope |

## Unmet and human-gated items

* Criterion 5: the requirements owner must explicitly disposition FR-044/AC-084. This cannot be authored or inferred; the wording already makes per-message review normative and the exception inactive.
* Criterion 9: exact integrated-byte independent review and passing publication gates for this head are CI/human evidence, not produced locally. Local checks are focused only.
* Quality FAIL, Define BLOCKED, Govern/Finalize NOT_EVALUATED, OD-52 to OD-55 and product criteria Not run stay visible. No live acceptance, screen-reader conformance, deployment, spending or approval is claimed.

## Selected approach

Evidence-only PR: record the verification, request the owner disposition, use `Refs #441` naming criteria 5 and 9.
