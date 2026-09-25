---
title: Idea Register
description: Working register of research ideas for Case Study 48 that are not yet validated requirements
ms.date: 2026-09-24
ms.topic: reference
---

## Purpose

This register records ideas raised during the Case Study 48 research so they
are not lost. An entry is a proposal to investigate, not an approved
requirement, design decision or observed outcome. Move an idea into the
[Case Study 48 Addendum](../case_study_48_addendum.md) or the
[Business Requirements Document](../brds/agentic-retrofit-programme-brd.md)
only after its evidence and owners are recorded.

## Status Values

| Status | Meaning |
| --- | --- |
| Captured | Recorded, with no research yet |
| Researching | Evidence is being collected |
| Proposed | Research is written up and ready for review |
| Validated | Accepted by the named owners and reflected in the addendum or BRD |
| Parked | Deferred, with the reason recorded |
| Rejected | Not pursued, with the reason recorded |

## Ideas

| ID | Date raised | Source | Idea | Status | Research |
| --- | --- | --- | --- | --- | --- |
| IDEA-001 | 2026-09-24 | Project lead | Build parts of some requested agents from small typed decision models (classifiers), such as the open-weight [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b), through the TypeSafe System One contract instead of a general generative model | Proposed | [System One Decision Models for Retrofit Agents](./typesafe-system-one-agent-fit.md) |

## Follow-Up Candidates From IDEA-001

These candidates came from the IDEA-001 research. They are research
suggestions, not ideas raised by the project lead. Each one needs an owner
before work starts.

| ID | Candidate | Why it may matter | Status |
| --- | --- | --- | --- |
| IDEA-001a | Classify historical free-text delay notes by delay cause to build the Phase 0 baseline | The addendum requires a twelve-month baseline by delay cause, and the notes are likely unstructured | Captured |
| IDEA-001b | Screen drafted resident communications with typed guardrail questions before a human sends them | The addendum forbids implied consent, universal bill-saving promises and use of the working programme line in hazard, complaint or consent messages | Captured |
| IDEA-001c | Compare hosted Jev with self-hosted Kev-4B and Kev-9B on synthetic Proper North Homes test sets during shadow mode | Accuracy, calibration, data residency and cost differ between the options | Captured |
| IDEA-001d | Use typed change classification to support the regulatory source update workflow | Step 3 of the reference update path requires each difference to be classified and linked to affected requirements | Captured |
