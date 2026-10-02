---
title: Program Manager Document Workspace Journey
description: Stakeholder-informed UX hypothesis and design handoff for a repository-backed program documentation canvas
ms.date: 2026-10-02
ms.topic: concept
---

## Research Status

This artifact is based on stakeholder input and repository analysis, not direct
research with program managers. Every behavioural claim below is therefore
reported or assumed and must be validated through interviews, contextual
inquiry and usability testing before it is treated as a proven requirement.

## Jobs-to-be-Done Analysis

### Job Statement

When working between engineering sprints, a program manager wants to find,
understand, connect and update the solution's business and product documents
without using a coding tool or Git, so that the repository remains the shared
source of truth while programme decisions stay coherent and current.

Evidence basis: reported by the project owner on 2026-10-02.

### Context and Current Solution

| Element | Finding | Evidence basis |
| --- | --- | --- |
| User | Program managers who understand Markdown but are not comfortable with coding tools or Git | Reported |
| Environment | Desktop work with frequent switching to other applications to gather information | Reported |
| Current approach | Engineering stores documentation in the repository; program managers would otherwise need VS Code or an equivalent coding workflow | Reported |
| Functional job | Browse BRDs, PRDs, ADRs, project documentation and presentations; search across them; understand relationships; edit Markdown | Reported |
| Emotional job | Feel in control of the programme story without fear of damaging code or Git history | Assumed |
| Social job | Collaborate with engineering through one source of truth while using programme-management language and interaction patterns | Assumed |
| Switching cost | Learning repository navigation, Git state and coding-editor conventions | Reported and assumed |
| Failure consequence | Requirements, decisions and evidence can diverge between sprints or important context can be missed | Assumed; severity requires validation |

### Success Measures

These measures are hypotheses until baseline user research is completed:

* Time to locate a known requirement, decision or evidence source.
* Successful completion of a Markdown update without opening a coding tool.
* Percentage of document switches completed without losing unsaved work.
* User ability to identify whether material is a case fact, proposal,
  hypothesis, synthesis or source snapshot.
* Reduction in documentation copies outside the repository.
* Search success and abandonment rate.

## User Journey Map

Persona: a desktop-based program manager working between engineering sprints.

Scenario: review the current programme position, reconcile information from
other applications and update a shared Markdown requirement or project page.

| Phase | User actions | Thoughts and emotions | Pain points | Design opportunity | Evidence basis |
| --- | --- | --- | --- | --- | --- |
| Orient | Opens the workspace and scans programme status and document groups | "Where should I start, and what changed?" Potential uncertainty | A repository tree exposes implementation structure rather than programme meaning | Provide a curated programme spine, category counts and latest-update signals | Assumed |
| Find | Searches for a requirement, decision, topic or evidence source | Wants fast recall while switching from another application | File names and folder paths may not match the phrase the user remembers | Search titles, descriptions, paths and Markdown content; group by BRD, PRD, ADR, research, evidence and presentation | Reported need; interaction assumed |
| Understand | Reads a document and follows its references | Needs to distinguish fact, proposal and hypothesis | Markdown links can hide the wider traceability context | Show evidence classification, outgoing links and backlinks beside the rendered document | Assumed |
| Update | Switches to edit mode, changes Markdown and saves | Wants confidence that only the intended document changes | Coding-editor chrome, Git concepts and unsafe source material create anxiety | Use a focused editor, explicit save state, protected immutable records and clear errors | Reported need; emotional response assumed |
| Reconcile | Moves to another application and returns with additional information | Wants to resume without losing place or text | Context switching can cause lost edits and stale views | Preserve the open document, warn before discarding edits and provide manual index refresh | Reported context; behaviour assumed |
| Complete | Confirms the change and continues programme work | Wants the shared record to be current | A success-shaped message could hide a failed write | Show success only after the repository write completes; surface save failures explicitly | Assumed |

## Accessibility Requirements

Accessibility is integrated into every stage rather than treated as a later
check:

* All navigation, document selection, read/edit switching, search and save
  controls must be keyboard reachable in a logical order.
* Visible focus must meet WCAG 2.2 AA expectations and must not be clipped by
  sticky headers or panels.
* Search and save status changes must be announced through live regions.
* Inputs need persistent accessible labels; placeholders cannot be the only
  label.
* Heading hierarchy must remain logical in both workspace chrome and rendered
  Markdown.
* Text and interactive-control contrast must meet WCAG AA. Evidence classes
  and save state cannot rely on colour alone.
* Controls must be at least 24 by 24 CSS pixels, with larger primary targets
  where space permits.
* The workspace must remain usable at 200 percent text zoom. Narrow layouts
  may move document context below the content rather than clipping it.
* Motion must respect `prefers-reduced-motion`.
* Read-only reasons and save failures must be available as text and announced,
  not communicated only by a disabled control.

Standard accessibility was requested for version one. Direct testing with
keyboard-only and screen-reader users remains required.

## Design Handoff

### Information Architecture

The workspace uses two complementary structures:

* A curated programme spine for the original case, addendum, BRD and knowledge
  base index.
* A complete library grouped into project documents, BRDs, PRDs, ADRs, ideas,
  research, regulatory evidence, methods, resources, presentations and
  visuals. Empty groups become visible automatically when documents are added.

### User Flow

1. Entry: the overview shows connected-record counts, the programme spine,
   recent files and a research-status notice.
2. Find: the user chooses a library record or searches across content with
   `Ctrl+K`.
3. Read: Markdown renders in a focused reading view with evidence class,
   repository path, outgoing links and backlinks.
4. Edit: an editable Markdown record can switch to a plain-text Markdown
   editor. Immutable case evidence, regulatory snapshots and owner-controlled
   memory remain read-only with a reason.
5. Save: the primary action writes the Markdown file directly to the shared
   workspace. `Ctrl+S` is supported. Success is shown only after the write
   completes.
6. Exit: switching records with unsaved work requires confirmation. A save
   failure leaves the document dirty and provides a recovery message.

Presentations and visual artifacts are discoverable but read-only in version
one. Rich presentation preview, relationship visualisation and future MCP
connectivity are version-two opportunities.

### Design Principles

* Progressive disclosure: begin with the programme spine, then reveal the full
  library, relationship context and editing controls as needed.
* Progress visibility: keep save state and current document identity visible.
* Contextual guidance: explain read-only policy at the document, not in a
  separate manual.
* Programme language first: expose requirements, decisions and evidence rather
  than branches, commits or editor mechanics.
* Truthful status: never imply that a file was saved, refreshed or classified
  when the underlying operation failed.

## Validation Plan

Before expanding the canvas, conduct five to eight program-manager interviews
and observe at least three real between-sprint documentation tasks. Test the
prototype with keyboard-only navigation and at least one screen reader. Focus
validation on category language, search terms, confidence while saving,
traceability usefulness, context-switch recovery and whether the immutable-file
boundaries match users' mental model.
