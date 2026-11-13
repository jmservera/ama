---
title: Local handoff, ready #74 evidence for a future demo parent
description: Concise handoff; evidence and metadata only, not a publication
ms.date: 2026-11-13
---

Refs #74, not closing. For a coherent future demo parent integrating ready #74 with #184. This is not a second speculative main PR and the local VM is not durable delivery.

## What is ready

* Source candidate `f50c5c7fdd179e4d3c187130afbdf1e369983992`, tree `65e39a2821c95f13a9a5375ab5bea633688273ef`, base `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`: initial additive read-only existing-building scope display, source spend UNKNOWN, no correction cycle. Unchanged here; `git diff f50c5c7fd..HEAD -- src` is empty.
* Evidence at this branch: records under `.copilot-tracking/reviews/2026-11-13-74-evidence-handoff-0526-source-records/`, identities in the [research table](../research/2026-11-13-74-evidence-handoff-0526-research.md), the [plan clarification](../plans/2026-11-13-74-evidence-handoff-0526-clarification.md), and the [changes](2026-11-13-74-evidence-handoff-0526-changes.md) and [review](../reviews/2026-11-13-74-evidence-handoff-0526-review.md) of this packaging.

## For the parent

* Carry this evidence folder and the `f50c5c7fd` RPI records together. Publish through the parent PR with `Refs #74`, not a closing keyword.
* The raw bundles under `/tmp/ama-74-retained-0518/` are not durable and are not packaged. The results apply only to `f50c5c7fd`; re-run the focused checks on the exact parent head when it differs in `app.js`, the check, its fixtures or the home-case/building API code.
* `e904` is a separate minute-integration candidate under its own independent review and recorded validation. It was not inspected, merged or admitted here; the parent owns that decision.

## State to state exactly

* Recorded execution results (`8b98f72a3` first section; no independent Review of that section is recorded): node check, Ruff check and format, mypy and six existing API tests exit 0. Browser addendum (`84478e5c9`, independent Review read the raw files): one browser run with 24 PASS markers, 0 FAIL, exit 0 under enforced 2 GiB cgroup and non-queued lock.
* Not: 24 independent tests or runs, a count of every assertion, a valid base-red, axe, AT or WCAG evidence, hosted CI, owner confirmation of the G5 display or label.
* Open outside engineering: owner, AT, WCAG and outcome confirmation. Compound criterion 2 is unproved. Nonblocking label, `translate`, 320 px and checkbox qualifications stand.
