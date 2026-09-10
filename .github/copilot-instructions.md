---
description: "Repository guidance for evolving AMA research documentation"
applyTo: "**"
---

# AMA Repository Instructions

## Repository Purpose and Structure

This repository contains Markdown documentation for an evolving research
project rather than executable software.

* `docs/` is the canonical location for project documentation.
  `docs/case_study_48.md` is the initial problem specification and should evolve
  as research adds, validates, refines, or invalidates assumptions.
* `support/` contains reference material that helps the research effort.
  `support/cohort.md` identifies colleagues who may be able to help with
  particular technical areas.

There is no build, test, lint, or single-test command configured in the
repository. Validate changes by reviewing the rendered Markdown and the Git
diff.

## Problem Specification Conventions

Extend `docs/case_study_48.md` in place as the research progresses. Do not create
additional case studies unless the project scope explicitly expands.

* Preserve the current problem framing: business challenge, transformation
  objective, agentic architecture, governance constraints, expected outcomes,
  timing, and business case.
* Integrate research findings into the relevant section instead of appending an
  unrelated running log. Add a focused section only when the existing structure
  cannot represent the new material clearly.
* Keep assumptions, proposals, validated findings, and observed outcomes
  distinguishable. Do not convert a forecast or research hypothesis into a
  statement of fact.
* Describe each agent's end-to-end responsibility and autonomy level. Make human
  approval, resident consent, regulatory controls, and safety constraints
  explicit wherever an agent drafts, recommends, acts, or flags.
* Attach concrete dates to regulatory claims and distinguish requirements
  already in force from consultations and future phases.
* Update the frontmatter `ms.date` using ISO `YYYY-MM-DD` whenever the
  specification changes materially.
* Keep business value and success measures quantitative when evidence supports
  them. Preserve uncertainty when figures remain estimates.

## Cohort Reference Conventions

Use `support/cohort.md` to identify colleagues who may be able to answer
questions or contribute expertise:

* Separate suggested subject-matter areas from the evidence used to infer them.
* Use `High`, `Medium`, or `Limited` confidence only as a measure of evidence
  strength, never as a rating of a person's proficiency or performance.
* Prefer self-declared expertise and explicit delivery ownership over indirect
  profile or activity signals.
* Mark narrow or indirect inferences as provisional and request confirmation
  from the person concerned.
* Frame the map as a help-routing reference, not an assessment of colleagues.
* Preserve the human-validation request when changing suggested expertise.
* Use the smallest relevant set of contacts for a research question. Do not
  infer that an entry grants availability, ownership, or endorsement.

## Markdown Style

* Preserve the heading hierarchy and table style already used by the target
  file.
* Use YAML frontmatter for new Markdown files. Do not add an H1 when the
  frontmatter contains `title`.
* Use `*` for unordered lists in new content.
* Use fenced code blocks with a language identifier when code examples are
  necessary.
* Use plain ASCII punctuation unless names or source material require Unicode.
* Avoid em dashes and bolded-prefix list items.
* Keep claims concise, specific, and traceable to the evidence available in the
  repository or supplied with the task. Do not invent customer facts,
  regulations, metrics, dates, or evidence.
