---
title: Research, #74 evidence packaging and parent handoff
description: Bounded evidence-packaging research; no source change
ms.date: 2026-11-13
---

Scope: package already-committed independent review and focused-validation records for #74 into this topic branch `docs/demo-home-scope-handoff-74-0526` (base and source `f50c5c7fdd179e4d3c187130afbdf1e369983992`, tree `65e39a2821c95f13a9a5375ab5bea633688273ef`, parent base `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`). Refs #74 only. This research executed no tests, resources, AppSource or semantic searches. Planning Readiness: Ready. Research disposition: executed (git object inspection only).

## Frozen source

* The initial source RPI (research, plan, details, changes, critique, review, state) is already in `f50c5c7fd`. It is not copied again.
* Classification stays: one INITIAL additive read-only building-scope display, source spend UNKNOWN, no correction cycle renewed.

## Source records and provenance

| Record | Origin commit | Blob | SHA-256 | Packaged copy (byte-identical) |
| --- | --- | --- | --- | --- |
| Independent static assessment | `c3aecd94625313b75d710f4c50bec7f82c7cabcb` (retained worktree `issue-74-applicability-review-0506`, branch `review/demo-home-scope-74-0506`) | `9b7b040f603f8c7676d9bddb79d568f0861927bf` | `8def4a7d598cfe4dc168cd8dbacf1e141b6edd27be7a5b17e4edbd7d78771b83` | `c3aecd946-independent-assessment.md` |
| Execution-boundary addendum | `4b8689031dff1760e66971c9e9894d59b924b1f0` (same branch, tip) | `8c1ffdaa5b389711408d79ec98fee57aee759e88` | `58e48cc3dcd7fe9a992a6a639de36a99cb05c72f85a8ffb5804a6bd945e5b5c8` | `4b8689031-independent-assessment-addendum.md` |
| Retained validation, initial attempt | `8b98f72a3efe6aa96c92c40e7a9c5b66d89dc7a8` (retained worktree `issue-74-retained-validation-0518`, branch `test/demo-home-scope-74-0518`) | `3c2fa0c9fa844ce360a29fed4c7b02bb741b45b5` | `c8637dd249e5d2b11211ede04b8730529aa93438fd204bdaeaaa7a61db3bbc81` | `8b98f72a3-retained-validation-evidence-initial.md` |
| Retained validation with browser addendum | `84478e5c9958ac2adca0959b23550896ced0d1a0` (same branch, tip) | `2733a5aa6f33b77c57ead5dd0a25818ff58f078a` | `700114b45db34e4ac5e221afc8a7eb3cb963f1e61d3c41798250b04682596e28` | `84478e5c9-retained-validation-evidence-with-browser-addendum.md` |

Packaged under `.copilot-tracking/reviews/2026-11-13-74-evidence-handoff-0526-source-records/`. Original paths: the two assessment records were `.copilot-tracking/reviews/2026-11-13-74-home-building-applicability-display-independent-assessment.md` and `...-assessment-addendum.md`; both validation commits used `.copilot-tracking/reviews/2026-11-13-74-retained-validation-0518-evidence.md`, so both versions are kept under distinct commit-prefixed names (bytes unchanged, names added only for packaging). The later file is a superset of the earlier file. Each origin commit descends from `f50c5c7fd` and changes only a tracking Markdown file.

## What the records support

* Static review `c3aecd946`: source Pass (FOCUSED tier) after reading all nine files and the full current 8055-character web-design-guidelines source. Its test statements are author-reported; no command was run by the reviewer. Nonblocking observations preserved: `translate="no"` on identifiers, 320 px long-ID wrapping, "Homes:" versus "Affected homes:" label, sibling ID display on a staff-only screen, README line width. Its remark that author native commands are not outputs is confirmed by the addendum.
* Addendum `4b8689031`: the author transcript retains commands but not outputs, so executed results were not independently evidenced at that time. The invalid wrong-source red (stale editable install, one unrelated 404, assertion wording mismatch) is an adverse fact, not a valid base-red. The plan's API-regression checkbox was an attribution limit.
* Retained validation `8b98f72a3`: actual exit 0 for node check, Ruff check, Ruff format check, mypy and six existing `tests.test_home_case_api` tests. Browser run was first blocked on memory headroom, preserved as historical.
* Browser addendum `84478e5c9`: one actual browser run, 24 PASS markers, 0 FAIL, inner and outer exit 0, non-queued heavy lock, exact source `f50c5c7fd` unchanged, enforced 2 GiB cgroup memory with no swap, 4.79 GiB headroom against a 3 GiB scoped budget. Independent Review read the raw files and found it conformant with three limits: paraphrased argv in `cmd.txt`, the exit file reflects the inner script, no during-run memory snapshot.

## Qualifications that must travel with the records

* 24 PASS markers are output markers from one run, not 24 independent tests or runs, and not proof that every assertion was counted.
* Axe was SKIPPED (`ZF_AXE_JS` unset). No automated accessibility, assistive-technology or WCAG result exists.
* The old base-red claim remains author-reported and unverified. The wrong-source 404 and wording error are not a valid base-red.
* Raw bundles live outside the repository (`/tmp/ama-74-retained-0518/`) and are not packaged. The local VM is not durable delivery.
* No hosted CI was observed. No human, owner, AT or WCAG confirmation exists. G5 remains optional, owner-unconfirmed and unproven by literal criterion 2.

## Parent relationship

Intended consumer: a coherent future demo parent that integrates this ready #74 evidence with #184. `e904` is a separate minute-integration candidate under independent review and separate recorded validation. Its live worktrees were not inspected, merged or admitted here.
