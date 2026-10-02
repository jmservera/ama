<!-- markdownlint-disable-file -->

# Task Research: rubric-score-gate

| Field              | Value                                                                  |
|--------------------|------------------------------------------------------------------------|
| Date               | 2026-10-02                                                             |
| Researcher / agent | rpi-research (RPI Agent parent, manual mode)                           |
| Status             | Complete                                                               |
| Artifact path      | .copilot-tracking/research/2026-10-02/rubric-score-gate-research.md    |

## Research Brief

* What to research: how to score the AMA capstone project against the FY27 rubric on every PR and push to `main`, approve a PR only when the score is greater than or equal to the previous score, persist the baseline on `main`, and extend later to PRDs, ADRs, code, infrastructure, the final PPTX and the pitch.
* Why it matters: the owner wants a ratchet that prevents rubric regressions as the capstone evolves.
* Audience or intended use: Plan phase for implementation in `jmservera/ama`.
* Scope: GitHub Agentic Workflows (gh-aw) versus a Copilot-enabled classic Actions workflow; baseline storage; approval and gating mechanics; extensibility to future artifact types.
* Non-goals: implementing workflows; changing the BRD; rescoring the BRD by hand.
* Criteria: verified mechanisms in official docs; security (read-only agent, OWASP CI/CD); determinism of the gate; cost; maintainability for a single-owner personal repository.
* Requested outputs: recommendation with design, open decisions and planning readiness.
* Output mode: convergence.

## Research Parameters

| Field                             | Value                                                                                           |
|-----------------------------------|-------------------------------------------------------------------------------------------------|
| Research question(s)              | Which workflow technology and gate design best implement a monotonic rubric-score PR gate?     |
| Codebase scope                    | `.github/`, `docs/brds/`, `docs/reference/method/`, `docs/reference/research/company/`         |
| External scope                    | docs.github.com agentic workflows page, github.github.com/gh-aw reference                       |
| Research posture                  | balanced                                                                                        |
| Posture provenance                | default                                                                                         |
| Explicit limits / deadline        | none                                                                                            |
| Edits allowed during research?    | no, research-only                                                                               |
| Resolved evidence root            | .copilot-tracking/                                                                              |
| Known constraints                 | Personal repo (no org Copilot billing); local terminal unresponsive on this host               |

## Extension Registry and Provenance

| Kind        | Candidate                          | Match and provenance                      | Scoped authority                     | Selected / skipped reason                         |
|-------------|------------------------------------|-------------------------------------------|--------------------------------------|---------------------------------------------------|
| Instruction | .github/copilot-instructions.md    | applyTo `**`                              | Repo conventions, KB log rules       | Selected: governs where scoring docs must live    |
| Instruction | markdown / writing-style           | applyTo `**/*.md`                         | Style of future scorer prompt        | Selected for plan                                 |
| Skill       | owasp-cicd                         | CI/CD security topic                      | Pipeline threat checks               | Selected as lens (inline), not loaded in full     |
| Skill       | context7-mcp                       | Library docs rule                         | Doc lookup                           | Skipped: gh-aw docs fetched directly from source  |
| Specialist  | RPI Researcher                     | Generic lane worker                       | Lane evidence                        | Skipped: lanes small and tightly coupled; inline  |

## User Participation and Research Decisions

| Checkpoint  | Questions or no-interaction rationale                                                       | Answers    | Resulting decision                              |
|-------------|---------------------------------------------------------------------------------------------|------------|-------------------------------------------------|
| Intake      | No questions: request is specific and the owner delegated the technology choice             | n/a        | Research both options, converge on one          |
| Convergence | OD-1..OD-3 deferred to Plan with recommended defaults; none blocks planning                 | unanswered | Recorded in Open Decisions                      |

## Research Questions

|  # | Sub-question                                                                                       | Type            | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | gh-aw or Copilot-enabled classic workflow?                                                         | depth           | H        | answered |
| Q2 | How can the workflow approve or block a PR, and who decides (agent or deterministic code)?         | depth           | H        | answered |
| Q3 | Where and how is the baseline stored on `main` without letting the PR author tamper with it?      | depth           | H        | answered |
| Q4 | How to control LLM scoring variance so a `>=` gate is not flaky?                                  | depth           | H        | answered |
| Q5 | How to extend to PRDs, ADRs, code, infra, PPTX and pitch?                                          | breadth         | M        | answered |
| Q6 | Authentication and cost for a personal repository                                                  | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/reference/research/company/capstone-brd-rubric-review.md` (manual readiness score 61/100, per-criterion table), `docs/reference/method/ama-capstone-assessment-guide.md`, `.copilot-tracking/brd-sessions/agentic-retrofit-programme.quality-report.yml`.
* Reused (verified) findings: the manual review already scores all 20 criteria with evidence and treats B and C as readiness estimates. It is a ready-made seed baseline (C3).
* Superseded / stale: none.

## Research Cycle Log

### Cycle 1

* Active direction controls: none
* Posture: balanced; completion when Q1 to Q6 are evidence-backed

#### Wave 1: Wider

* Candidates: (a) gh-aw markdown workflow with Copilot engine; (b) classic Actions YAML calling Copilot CLI with a PAT; (c) classic Actions YAML calling GitHub Models (`actions/ai-inference`); (d) Copilot code review with custom instructions.
* Reflection: (d) cannot emit a numeric gate; (b) and (c) need hand-built safety; (a) has built-in read-only agent, safe outputs and threat detection (W1, W2).

#### Wave 2: Deeper

* gh-aw safe outputs relevant to the gate: `submit-pull-request-review` with `APPROVE`, `REQUEST_CHANGES`, `COMMENT` and `allowed-events` enforcement; `create-check-run` with `success`/`failure`; `push-to-pull-request-branch`; `add-comment` with `hide-older-comments`; custom safe-output `jobs` that read `$GH_AW_AGENT_OUTPUT` and run deterministic steps with their own permissions (W2, W5).
* Persistence options: `repo-memory` (dedicated `memory/*` branch, unlimited retention), `cache-memory` (7 days), or a file on `main` (W3).
* Frontmatter supports `pre-steps`/`steps` for deterministic preparation, `max-ai-credits`, `timeout-minutes`, `engine.model`, `network` allowlist (W4).
* Auth: personal repos must use `COPILOT_GITHUB_TOKEN` (fine-grained PAT, Account permission Copilot Requests: Read); `copilot-requests: write` is org-billing only (W6).
* Rubric facts: 20 criteria x 5 points; floors per section and no criterion at 1; B and C scored live (C1).
* BRD: about 1,700 lines across 65 H2/H3 sections; within agent context when read by file tools (C2).

#### Wave 3: Contrarian

* X-1 Scorer variance: an LLM rescoring an unchanged document can move individual criteria by +/-1, so a strict `>=` on total would fail spuriously. Mitigations: (i) content fingerprint per artifact; unchanged artifacts carry their previous scores forward without rescoring; (ii) agent receives previous per-criterion scores and rationale and may change a criterion only with diff-cited evidence; (iii) pin `engine.model`; (iv) optional tolerance. Accepted as design requirement.
* X-2 Agent as judge of its own gate: letting the agent choose `APPROVE` couples the pass/fail decision to model output. Mitigation: agent emits structured scores only; a deterministic custom safe-output job computes totals, floors, comparison and posts the decision. Accepted.
* X-3 Baseline tampering: if the gate read the baseline from the PR head, a PR could lower `baseline.json`. Mitigation: gate reads the baseline from the base branch ref (`origin/main`) only; a PR that edits the baseline file outside the bot commit fails. Accepted.
* X-4 Required check on bot commit: commits pushed with `GITHUB_TOKEN` do not trigger new workflow runs, so a bot commit that writes the new score file to the PR branch would leave the new head SHA without the required check. Mitigation: the gate job sets the commit status on the new SHA it pushed (statuses API works on any SHA), then submits the review. Alternative: do not commit from PR at all and persist on `main` after merge. Accepted with OD-2.
* X-5 GITHUB_TOKEN approvals: GitHub blocks Actions from approving PRs unless the repository setting "Allow GitHub Actions to create and approve pull requests" is enabled (known GitHub behaviour, not re-fetched this session). A required status check is the more robust merge gate; the approving review is optional sugar. Accepted as OD-2.
* X-6 Direct pushes to `main` cannot be blocked after the fact. The push run can only score, update the baseline, and open an issue on regression. Branch protection requiring PRs is the real control. Accepted.
* X-7 gh-aw is public preview and requires `gh aw compile` to produce the `.lock.yml`; the local terminal is unreliable on this host. Mitigation: owner compiles locally, or a bootstrap step is documented. Recorded as blocker B-1 (non-blocking for planning).
* X-8 Live criteria (B1 to B5, C2) cannot be evidenced by documents. Scorer must cap them as readiness estimates, consistent with C3, until a deck, demo recording or pitch transcript exists.

#### Parent Synthesis and Disposition

| Material / claim                                   | Evidence           | Disposition | Rationale                                                        |
|----------------------------------------------------|--------------------|-------------|------------------------------------------------------------------|
| Use gh-aw with Copilot engine                      | W1, W2, W4, W5     | accepted    | Built-in sandbox, safe outputs, threat detection, less glue code |
| Classic YAML + Copilot CLI PAT                     | W6, X-2            | rejected    | Agent and write token share a job; must hand-build guardrails    |
| Classic YAML + GitHub Models                       | none verified      | rejected    | No repo exploration tools; context limits unverified, risky      |
| Copilot code review instructions                   | none               | rejected    | No numeric output, cannot gate                                   |
| Deterministic gate in custom safe-output job       | W5, X-2            | accepted    | Separates judgement from enforcement                             |
| Baseline file on `main`, read from base ref        | X-3, C3            | accepted    | Meets "store in main"; tamper-resistant                          |
| `repo-memory` branch as baseline store             | W3                 | deferred    | Simpler writes but owner asked for `main`                        |
| Fingerprint carry-forward and evidence-cited delta | X-1                | accepted    | Removes most variance                                            |

## Evidence Log

| ID | Location                                                                                       | Retrieved   | Finding                                                                                                   |
|----|------------------------------------------------------------------------------------------------|-------------|-----------------------------------------------------------------------------------------------------------|
| C1 | docs/reference/method/ama-capstone-assessment-guide.md:12-20                                   | 2026-10-02  | 20 criteria, 4 sections, 5 points each; floors and outcome bands in "How the outcome is determined"       |
| C2 | docs/brds/agentic-retrofit-programme-brd.md:29-1715                                            | 2026-10-02  | BRD has 65 H2/H3 sections spanning about 1,700 lines                                                      |
| C3 | docs/reference/research/company/capstone-brd-rubric-review.md:18-58                            | 2026-10-02  | Manual readiness scores per criterion, total 61/100; usable seed baseline                                 |
| C4 | .git/config:9-10                                                                               | 2026-10-02  | Remote `https://github.com/jmservera/ama` is a personal-account repository                                |
| C5 | .github/ (file search)                                                                         | 2026-10-02  | No `.github/workflows/` exists yet; skills, agents and copilot-instructions only                          |
| W1 | https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows              | 2026-10-02  | Markdown + frontmatter, compiled to `.lock.yml`; read-only by default; safe outputs; Copilot default engine; public preview; AIC billing, `max-ai-credits` default 1,000 |
| W2 | https://github.github.com/gh-aw/reference/safe-outputs/                                        | 2026-10-02  | `submit-pull-request-review` (APPROVE/REQUEST_CHANGES/COMMENT, `allowed-events`), `create-check-run`, `push-to-pull-request-branch`, `add-comment`, `noop` required when no action |
| W3 | https://github.github.com/gh-aw/reference/repo-memory/                                         | 2026-10-02  | Repo memory persists files on a `memory/*` git branch with size and glob limits                           |
| W4 | https://github.github.com/gh-aw/reference/frontmatter/                                         | 2026-10-02  | `on:` standard triggers, `pre-steps`/`steps`/`jobs`, `engine`, `network`, `timeout-minutes`, `max-ai-credits`, strict mode default |
| W5 | https://github.github.com/gh-aw/reference/custom-safe-outputs/                                 | 2026-10-02  | Custom safe-output jobs: typed inputs become an agent tool; job reads `$GH_AW_AGENT_OUTPUT`; own permissions; `needs: safe_outputs` ordering |
| W6 | https://github.github.com/gh-aw/reference/auth/                                                | 2026-10-02  | Personal repos use `COPILOT_GITHUB_TOKEN` fine-grained PAT with Copilot Requests: Read; `copilot-requests: write` requires org billing |

## Recommended Design

Use a GitHub Agentic Workflow with the Copilot engine for judgement and a deterministic custom safe-output job for enforcement.

```text
PR opened/synchronized  ─┐
push to main            ─┤
workflow_dispatch       ─┘
        │
 pre-steps (deterministic)
   • read .github/rubric/artifacts.yml (artifact registry)
   • resolve present artifacts, compute SHA-256 fingerprints
   • extract non-text artifacts (pptx -> markdown, pitch transcript)
   • git show origin/main:.github/rubric/scores/latest.json -> /tmp/baseline.json
        │
 agent (read-only, Copilot, pinned model)
   • rescore only artifacts whose fingerprint changed
   • per criterion: score 1-5, evidence path:line, delta justification
   • calls custom tool `record_rubric_score` with JSON
        │
 custom safe-output job `record-rubric-score` (deterministic)
   • validate JSON schema, compute section totals, floors, outcome band
   • compare total with baseline from main (rule = OD-1)
   • PR: write latest.json + history.jsonl to PR branch, set commit status
     `rubric/score` on new head, post sticky comment, submit review (OD-2)
   • push to main: update baseline if changed; open issue on regression
```

* Registry `.github/rubric/artifacts.yml` lists artifact types with globs, extractor and criteria they inform: `brd` (now), `prd`, `adr`, `code`, `infra`, `deck` (`docs/presentations/*.pptx`), `pitch` (transcript `.vtt`/`.md`), `thought-leadership` (Section D). Adding a future artifact is a registry edit, not a workflow edit.
* Rubric criteria and floors live in `.github/rubric/rubric.yml`, derived from C1, so the gate code and the prompt share one source.
* Seed `.github/rubric/scores/latest.json` from C3 (61/100) so the first PR has a baseline.
* Score file is a portfolio scorecard: 20 criteria, each with evidence drawn from any artifact, plus per-artifact fingerprints and model id.
* Path filters limit runs to registry globs plus `.github/rubric/**`, controlling AIC cost; `max-ai-credits` caps a run.

## Open Decisions

| ID   | Decision                                            | Options                                                                                                       | Recommended default                                                             |
|------|-----------------------------------------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| OD-1 | Gate rule                                           | (a) total >= baseline; (b) (a) plus no criterion decrease; (c) (a) with tolerance                              | (a), report per-criterion drops as warnings                                     |
| OD-2 | Merge enforcement                                   | (a) required status check `rubric/score`; (b) bot APPROVE review (needs repo setting); (c) both              | (c): status check as the enforced gate, APPROVE/REQUEST_CHANGES as visible verdict |
| OD-3 | Copilot auth                                        | `COPILOT_GITHUB_TOKEN` PAT (personal repo) vs move repo to an org with `copilot-requests: write`              | `COPILOT_GITHUB_TOKEN`                                                          |

## Risks

* gh-aw is public preview; syntax may change. Pin the gh-aw version in the compiled lock file and recompile deliberately.
* Each run consumes AI credits; path filters and fingerprint carry-forward limit reruns.
* Scores are readiness estimates, not panel predictions; label them so in every comment.
* Single-owner repo: the owner can bypass branch protection; the gate is a discipline aid, not an external control.

## Research Disposition and Planning Readiness

* Research disposition: executed (Cycle 1, inline waves; no re-entry needed: Q1 to Q6 answered, remaining items are owner decisions with defaults).
* Planning Readiness: Ready.
* Blocker B-1 (non-blocking): gh CLI / gh-aw availability unverified locally because the terminal returned no output.

## Self-check

* Every question answered with evidence IDs: yes.
* Alternatives compared and one recommendation selected in convergence mode: yes.
* No source files edited: yes.
