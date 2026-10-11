---
description: "Repository guidance for evolving AMA research documentation"
applyTo: "**"
---

# AMA Repository Instructions

## Repository Purpose and Structure

This repository contains Markdown documentation for an evolving research
project rather than executable software.

* `docs/` is the canonical location for project documentation.
  `docs/case_study_48_original.md` preserves the initial problem specification,
  while `docs/case_study_48_addendum.md` evolves as research adds, validates,
  refines, or invalidates assumptions. Always read both documents to start
  working on the project.
* `docs/reference/` is the project knowledge base, the second brain for
  agents and people. Read its index, `docs/reference/README.md`, at the start
  of every task to find the relevant files, and read
  `docs/reference/memory.md` for the owner's context and preferences.
  * `docs/reference/regulatory/` holds dated local copies of legislation,
    regulatory standards, government policy, guidance, funding material and
    standards-body information, grouped by topic. Read
    `docs/reference/regulatory/README.md` before using these sources.
  * `docs/reference/research/` holds cited research syntheses.
    `research/sector/housing-association-primer.md` explains what a UK
    housing association is. Read it to understand the customer.
  * `docs/reference/method/` holds AMA training material and reusable
    prompts.
  * `docs/reference/resources/` holds curated pointers to internal and
    external resources, such as the Microsoft Industry Hub, with retrieved
    findings. Internal Microsoft content can be retrieved with WorkIQ.
  * `docs/reference/log.md` is the append-only change log for the knowledge
    base.
* `docs/presentations/` holds the final, validated presentation decks. Deck
  working files (content YAML, research, validation images and change logs)
  stay under `.copilot-tracking/ppt/{YYYY-MM-DD}/{deck-name}/`. After a deck
  passes validation, copy the generated PPTX from its `slide-deck/` folder to
  `docs/presentations/{deck-name}.pptx` as the delivery copy, replacing the
  previous version of the same deck, and list it in the index. Use the
  `ama-mentor-deck` skill in `.github/skills/ama-mentor-deck/` to create,
  update, review or republish the mentor progress review deck.
* `support/` is the owner's private working area and is not part of the
  knowledge base. `support/cohort.md` identifies colleagues who may be able
  to help with particular technical areas.
* `.github/agents/company-*` are the role agents for interrogating the
  problem from different Zava North Homes perspectives.
  Their shared evidence base is
  `docs/reference/research/company/company-profile-research.md`.
* `.github/agents/ama-*` are AMA helper agents with knowledge extracted from the AMA trainings.

There is no build, test, lint, or single-test command configured in the
repository. Validate changes by reviewing the rendered Markdown and the Git
diff.

## Branch and Pull Request Workflow

Make all new work on a topic branch and bring it into `main` through a pull
request. Do not commit or push directly to `main`.

* Before changing files, check `git status --short` and
  `git branch --show-current`, then identify any known upstream branch or PR
  lifecycle and the proposed work's relationship and dependency. Honour an
  explicit owner branch/base direction within the safeguards below; otherwise
  select by coherent workstream, not by a new message, document type or phase:

  | Situation | Branch decision |
  | --- | --- |
  | No file change, such as a question or explanation | Do not create a branch. |
  | Known active branch or open PR matches the continuing research, design, PRD, implementation or review workstream | Reuse it by default. Do not routinely ask before continuing a coherent iteration. |
  | Related work needs independently reviewable isolation or carries material risk or breaking change | Create a child branch from the current topic to preserve unmerged ancestry; use a separate worktree when parallel or isolated working copies are needed. |
  | On `main` with no matching active topic, unrelated work, work whose prior branch has merged, or an explicit request for a fresh main-based branch | Fetch and create a branch from the latest `origin/main` named `{type}/{short-description}`, where `{type}` is the Conventional Commit type, for example `docs/retrofit-funding-update` or `feat/rubric-gate-context`. |

  For a closed-but-unmerged branch or PR, a detached or unknown branch, or an
  ambiguous relationship or dependency, pause and ask the owner for the
  smallest clarification needed. Branch selection uses read-only inspection;
  it does not authorize discarding, stashing, committing or moving existing
  work, rewriting history, reopening or merging a PR, deleting a branch, or
  writing to a remote. Create/switch the selected branch only after this
  decision and the dirty-worktree safeguard below.
* When uncommitted changes already exist, do not discard, stash, commit or
  move them without the owner's confirmation. Ask whether to carry them onto
  the new branch or to isolate the new work in a separate `git worktree`.
* Before committing, resolve the authenticated GitHub account with
  `gh api user` and construct its privacy-safe email as
  `{id}+{login}@users.noreply.github.com` using the returned `id` and `login`.
  Configure that address with repository-local `git config --local user.email`
  and use it for both author and committer. Do not hardcode a user's email in
  these instructions, use a private email or change global Git configuration.
  If GitHub rejects a push for email privacy, do not disable privacy protection;
  obtain the owner's permission before amending an existing commit.
* Commit following the commit message conventions, push the branch and open
  a pull request with `gh pr create`. Target `main` for an independent branch;
  target the parent topic for deliberate stacked work, declaring the dependency
  in the pull request. After the parent merges, re-evaluate and retarget the
  child as needed; never silently rebase, force-push, rewrite or merge work
  merely to manage branch lineage. Describe the change, the evidence or
  sources used and the validation performed.
* Let the pull request checks, including the rubric scoring workflow, run
  before merge. Address review feedback with further commits on the same
  branch.
* Leave the merge decision to the owner. Do not merge, force-push or rewrite
  `main` history unless the owner asks.

## Knowledge Base Conventions

Keep `docs/reference/` current so knowledge compounds across sessions instead
of being rediscovered.

* Start from the index and open only the files the task needs. Search large
  regulatory snapshots for the relevant provision instead of reading them end
  to end.
* Treat regulatory snapshots as immutable. Record a newer retrieval as a
  reviewed update in the regulatory register.
* Integrate new findings into the existing synthesis or project document.
  Create a new page only when no existing page can hold the topic, and follow
  the placement rules in the index.
* File durable answers, comparisons and findings back into the knowledge base
  with their evidence rather than leaving them in chat history.
* When a knowledge base file is added, moved, retired or materially changed,
  update the index and append an entry to `docs/reference/log.md`. Never
  rewrite earlier log entries.
* Update `docs/reference/memory.md` only when the owner asks. Memory is
  context, not evidence.
* Flag contradictions between sources and syntheses rather than silently
  resolving them.
* Use relative links between knowledge base files and fix every link a move
  breaks.

## Problem Specification Conventions

Preserve `docs/case_study_48_original.md` unchanged. Extend
`docs/case_study_48_addendum.md` in place as research progresses. Do not create
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

## Legal and Regulatory Evidence Conventions

Treat local regulatory documents as evidence snapshots, not a self-updating
source of legal truth.

* Classify each claim as legislation, regulatory standard, official guidance,
  final policy, consultation material, funding condition, technical standard
  or internal interpretation.
* Use the authority hierarchy and current-use status in
  `docs/reference/regulatory/README.md`. Do not use historical or superseded
  material as an operational rule.
* Cite the local source, relevant provision or section, source date and
  retrieval date for every material regulatory claim.
* Check the linked official source for amendments, commencement, replacement
  or withdrawal before a consequential design, approval, release or external
  submission. Record the check rather than claiming a local copy is current.
* Keep legal interpretation and activation of operational rules under named
  human legal, compliance or professional approval. Agents may retrieve,
  compare, summarise and flag changes, but must not decide that a duty is
  satisfied or silently update a live control.
* Record detected changes as review items with affected requirements,
  decisions, user journeys, rules, tests and evidence. Preserve prior versions
  and the effective dates of approved changes.
* Assess change likelihood as `High`, `Medium` or `Low`, and apply the review
  cadence in the reference register. Increase review frequency around announced
  commencement dates, consultations, scheme changes and standards revisions.
* Design every control to reduce avoidable effort and delay for employees,
  residents, contractors and public officials without weakening safety,
  accessibility, privacy, redress, professional judgement or resident choice.
* Prefer official legislation data, publication metadata and alerts for change
  detection. Web scraping may support discovery, but scraped content remains
  unverified until provenance, completeness and differences are reviewed.

## Cohort Reference Conventions

Use `support/cohort.md` only when the owner asks who could answer questions or
contribute expertise. It is private owner material outside the knowledge base:

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

## Company Profile Agent Conventions

Treat the company-role agents as research instruments, not simulated employees
with privileged knowledge.

* Keep every response anchored to `docs/case_study_48_original.md`,
  `docs/case_study_48_addendum.md` and
  `docs/reference/research/company/company-profile-research.md`.
* Label information as a case-study fact, sector-informed hypothesis, or
  unknown company detail. Never turn a comparator's practice into a fact about
  Zava North Homes.
* Ask one focused question at a time when eliciting missing information.
* Stay within the role's decision rights and identify handoffs when another
  profile owns the answer.
* Preserve resident consent, legal review, professional judgement, and formal
  approval boundaries. A role profile must not imply authority to override
  them.
* Propose wording for the problem specification only after separating evidence
  from assumptions.

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
