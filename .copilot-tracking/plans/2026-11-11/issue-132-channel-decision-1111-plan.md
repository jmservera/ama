---
title: Issue 132 delivery-channel and identity decision record plan
ms.date: 2026-11-11
task_id: issue-132-channel-decision-1111
---

## Scope and authority

* Docs-only candidate for a later, separately admitted Implement. This admission is Research and Plan only; nothing below is executed here.
* Research: `.copilot-tracking/research/2026-11-11/issue-132-channel-decision-1111-research.md` (disposition `executed`, Planning Readiness `Ready`). Details: `.copilot-tracking/details/2026-11-11/issue-132-channel-decision-1111-details.md`. Critique: `.copilot-tracking/plans/2026-11-11/issue-132-channel-decision-1111-critique.md`.
* Branch `docs/demo-intake-channel-decision-132-1111`, base `74e63363bdcb6f9d420ff9c71b8332a9baf0044b`, target `main`.
* Ledger: C1 to C5 and E1 to E4 spent, E5 unadmitted and one remains. This plan consumes no correction, grants no new five or reset, transfers no 134 authority and is not the E5 admission. Whether a later docs-only Implement is an E5 or ordinary documentation work under the owner's delegated technical decisions is Root's classification.
* No change or tick of either criterion is authorized. The named variation and escalation criterion is out of scope.

## Objective

Make the repository's decision record match the owner's existing, dated, synthetic-demonstrator decision, so the criterion "Decision recorded on whether delivery is a staff-mediated intake or a provider portal, with identity approach" can be read against a recorded decision, without turning a deferred production decision into whole acceptance.

## Decision (proposed technical selection, transcribing the owner direction)

* Demonstrator interaction route: option A, staff-mediated intake. Only existing authenticated staff act; the worker is a named person in the record (`confirmed_by`), never a signed-in actor.
* Identity approach: the existing staff identity decision, ADR 0002 "Entra-authoritative staff access" (accepted by the owner 2026-10-24, bounded, release gates open), and the existing auth modes `password` (development fixture) and `trusted-proxy`. No new identity architecture.
* Option B (provider portal, B2B guest, #116) stays deferred. Production worker identity, onboarding, lawful basis, DPIA and Legal, Compliance, DPO and identity-owner approval stay unresolved.
* Authority source: owner comment [6753054374](https://github.com/jmservera/ama/issues/132#issuecomment-6753054374), 2026-11-09, quoted exactly. Named as the exercise owner, Juan Manuel Servera (ADR 0005 names the same exercise owner), as owner-directed, not as formal acceptance of ADR 0007's option A text, which the comment does not adopt verbatim. The ADR 0002 section is the precedent for a bounded owner-decision section inside a Proposed ADR.

## Target paths and exact edits

| Path | Section | Change |
| --- | --- | --- |
| `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md` | Frontmatter | Update `description` to say "Proposed for production; owner-directed for the synthetic demonstrator only"; set `ms.date` to the edit date. Keep the filename and title so existing references stay valid |
| same | `## Status` | Replace the stale "the owner has not decided" sentence with a dated delta: overall status stays Proposed (not an acceptance of provider portal, #116, production or any Legal, Compliance, DPO or identity approval); add one sentence pointing to the new section. Keep the 2026-11-04 proposal date |
| same | `## Context` | Keep the 2026-11-04 bullets as history; mark the last bullet ("That answer has not been given") as answered on 2026-11-09 with a link to the new section. Do not delete original text |
| same | new `## Owner Direction for the Synthetic Demonstrator (2026-11-09, Refs #132)` after `## Proposed decision` | Quote the owner comment exactly with id, URL and timestamp, and state "relayed on the issue from the owner's account; the original owner message is not held in the repository". Record: option A for the synthetic demonstrator; identity approach per ADR 0002 owner decision and current auth modes; contractor not a signed-in actor; no new account, permission, portal, public access, provider send, contract instruction, resident consent or production acceptance. State the status label "Owner-directed for the synthetic demonstrator only". Link requirement-qualified: ADR 0002 section (staff identity, bounded, gates open), PRD Profile Journey Contract (no portal, `in-review`), core README staff intake section (implemented behavior, not approval) |
| same | `## Owner decisions needed` | Split into "Owner-directed for the synthetic demonstrator" (the staff-mediated route and the staff-only slice, citing the comment; not stated as formal acceptance of option A)  and "Still open" (confirm option B deferred for production and name the #116 identity decision owner; real worker identity, lawful basis and any Legal, Compliance, DPO or identity-owner approval; named variation and escalation owner, with the escalation criterion cross-reference) |
| same | `## Next stacked slices once accepted` and `## Context` "Not delivered" bullet | Mark both as the 2026-11-04 snapshot (dated history, text kept). Add one dated clause: the staff intake (capture, correction, acknowledgement, screen) is delivered by PR 1425, with PR 1432 and PR 1438 as bounded test and keyboard-probe follow-ups; accessibility and live acceptance are unproven and the escalation write path and named escalation owner are still undelivered. Verify each PR number and scope with `git log` before writing |
| `docs/reference/README.md` | Task table near the "Understand or provision staff sign-in" row | Add one row: task "Understand the staff-mediated contractor intake decision (Refs #132)", link to the new ADR 0007 section, status text "Owner-directed for the synthetic demonstrator only (2026-11-09); ADR stays Proposed; provider portal, #116 and production identity unresolved; no criterion ticked" |
| `docs/reference/log.md` | Append at end | New dated entry in the existing style: what changed, evidence class (documentation only), explicit non-claims, tracking pointer. Never edit earlier entries |

No other file changes. Explicitly not touched: PRD, BRD, case study, ADR 0002 and 0005 text, source, tests, config, workflows, the cut-over evidence pack (its ADR blob pins are dated history and stay as recorded), the issue, board and any PR.

## Acceptance boundary

* Merging records the decision only. It does not tick either criterion, close issue 132, accept ADR 0007 as a whole, accept a provider portal, resolve #116, claim that fixture logins authenticate actual workers or staff, or supply Legal, Compliance, DPO, identity or production approval.
* The tick of the decision criterion is a later Root and owner action: the owner or Root must judge that the demonstrator-scoped recorded decision satisfies the unscoped wording. This plan does not decide that and does not relax the wording.
* If the owner or Root judges that the criterion needs a production-scope decision or a named #116 owner, the plan stops at the recorded section and returns the focused owner question below.

## Validation (docs-only tier)

* Markdown and link review of the three changed files, relative-link and anchor check by reading, `git diff` review, plain ASCII, no em dashes, `*` lists, no bolded-prefix items.
* No runtime, test, browser, install, SQL, provider, cloud or deployment run; no `rpi-checks` full gate.
* Future publication still needs independent exact-head review, actual applicable hosted checks read for the exact head, and preserved original and adverse history. A skipped or path-filtered check is not a success.
* Original research, plan, critique and Review stay as written; a later Implement adds its own dated changes and review artifacts and does not edit these.

## Risks

* Over-claim: a reader could take "owner-directed" as acceptance of the ADR. Mitigation: the status label, the headline Status text and the acceptance boundary all repeat the limits.
* Provenance: the owner words are relayed. Mitigation: say so in the record and keep the issue comment URL as the authority pointer.
* Stale claims: the "Next stacked slices" clause must be checked against repository history before writing.

## Focused question returned for the owner (if the tick is sought)

"Does the owner accept the synthetic-demonstrator-scoped record in ADR 0007 (staff-mediated intake, existing staff identity, portal and #116 deferred) as satisfying the criterion 'Decision recorded ... with identity approach', and who owns the production #116 provider-identity decision?"
