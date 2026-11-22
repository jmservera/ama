---
title: Project Memory
description: Owner-curated working notes, preferences and standing context for the AMA Case Study 48 project
ms.date: 2026-09-30
ms.topic: reference
---

## How to Use This File

This file holds the project owner's working notes and standing context. It is
part of the [Project Knowledge Base](./README.md), but it is not an evidence
source.

* Read it at the start of a task for context on the programme, deliverables
  and preferences.
* Update it only when the project owner asks. Record the change in the
  [Knowledge Base Log](./log.md).
* Do not treat an entry as a validated finding, a company fact or a
  regulatory claim. Move evidence-backed material into the relevant research
  or project document instead.

## AMA Programme Process

The programme progresses through five stages:

1. Rubric: what good looks like
2. Masterclasses: build the capability
3. Mentoring: challenge and coach
4. Capstone: apply the learning
5. Panel: demonstrate mastery

## Presentation Guidance

Prepare a 15-minute presentation pitch, and be prepared to go back and forth
between the business and technology.

The final presentation, architecture and pitch must each be checked and
challenged against the complete
[Capstone Assessment Guide](./method/ama-capstone-assessment-guide.md).
The challenge must use the published criteria and descriptors, record the
evidence for each judgement, identify gaps and assumptions, and apply the
section and individual-criterion floors before treating a deliverable as
ready.

Additional tips:

* Prepare the meetings for explaining it to the CEO, CIO and CFO, tailoring your message to each executive's priorities and concerns.
* Keep your slides concise and focused on key points.
* Anticipate potential questions and prepare answers.
* Practice your pitch multiple times to ensure smooth delivery.
* Engage your audience with clear visuals and examples.
* Time yourself to make sure you stay within the 15-minute limit.

Cohort 1 shared the following guidance, recorded here as peer advice rather
than validated evidence:

* Start with the customer and the reason the work matters.
* Make the business problem and value unmistakable.
* Tell one clear end-to-end story, not a series of disconnected slides.
* Show how the solution changes the customer outcome.
* Use the demo as the proof point that brings the story to life.

## Standing Preferences

* `support/` is the owner's private working area. `support/cohort.md` is for
  internal use and is not part of the knowledge base. Consult it only when
  the owner asks who could help with a question.
* AI is the most important part of the demo, so AI usage is generally
  approved for the demo (owner statement, 2026-11-22). The owner holds the
  OQ-017 model-call authority and has approved model calls for the demo. All
  demo data is synthetic and the model is planned to move to the UK, so DH-006
  is accepted for demo scope only. Real resident data, production use, Legal
  and DPO approval stay out of this approval. Agents must not mark AI-related
  demo work human-blocked on OQ-017 or DH-006.

## Delivery Decision, 2026-11-22

* Owner decision (2026-11-22): the multi-hour full local gate is not the
  per-change gate. Per change, use targeted local tests (including the tests
  of every touched area and ruff, mypy and format checks), hosted CI on the
  exact head, independent review, and a post-merge smoke test against the
  deployed demo (health, chat ask, map, resident chart) with a rollback to the
  last good revision. Run the full gate only for major changes (infrastructure,
  deployment, SQL, security, release) and once after a large group of merged
  changes, on the integrated main tip. Human, legal and resident gates are
  unchanged.
