---
title: Project Memory
description: Owner-curated working notes, preferences and standing context for the AMA Case Study 48 project
ms.date: 2026-11-25
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

## GitHub API Rate Limits, 2026-11-23

* The GraphQL API gives each user 5,000 points per hour, shared by every
  session that uses the same token. Many parallel delivery sessions plus
  `gh project` and `gh pr` calls exhaust it (owner shared the
  [GitHub documentation](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api),
  2026-11-23).
* Prefer REST (`gh api`) for pull requests, merges and check runs, which has a
  separate limit. Check the GraphQL budget with `gh api rate_limit`, read the
  project board once per delivery check (otherwise use the cache), batch
  Status edits into that single pass and avoid parallel GraphQL bursts.

## GitHub API Rate Limits, 2026-11-25

Owner-supplied working notes from the GitHub documentation
([GraphQL](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api),
[REST](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2026-03-10),
retrieved 2026-11-25). GitHub states that the figures can change without notice.
These notes explain the delivery coordinator's "GraphQL: API rate limit already
exceeded" and `gh project` failures.

* The REST and GraphQL primary limits are separate buckets. A user (including a
  personal access token and any app acting for that user) gets 5,000 REST
  requests or 5,000 GraphQL points per hour. REST costs one request each.
  GraphQL costs roughly the number of connection requests divided by 100, with a
  minimum of 1. Exhausting GraphQL leaves REST available.
* Prefer `gh api` REST calls (issues, comments, pulls, merges, check runs) over
  `gh issue`, `gh pr` and `gh project` commands, which use GraphQL. Project
  board Status writes have only GraphQL, so batch them in one call or use the
  cached board snapshot while limited.
* Read the response headers `x-ratelimit-remaining`, `x-ratelimit-reset` (UTC
  epoch seconds) and `x-ratelimit-resource` instead of spending points on a
  `rateLimit` query. An exceeded primary limit can still return HTTP 200 with
  an error body and `x-ratelimit-remaining` of 0. Do not retry before the reset
  time.
* Secondary limits apply across both APIs: at most 100 concurrent requests,
  900 points a minute for REST and 2,000 for GraphQL per endpoint, and about 80
  content-creating requests a minute or 500 an hour. Mutations and REST writes
  count 5 points, reads 1.
* On a secondary-limit response (HTTP 403 or 200) wait for `retry-after`
  seconds when present, otherwise at least one minute, then back off
  exponentially and stop after a fixed number of retries. Continued requests
  while limited can get an integration banned.
* Pause at least one second between write requests, avoid concurrent writes
  and prefer webhooks or one batched read over polling. GraphQL calls need
  `first` or `last` of 1 to 100 on every connection and at most 500,000 nodes.
* The `GITHUB_TOKEN` inside Actions has its own lower limit of 1,000 requests
  an hour per repository.
