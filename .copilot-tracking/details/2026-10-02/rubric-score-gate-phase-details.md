<!-- markdownlint-disable-file -->

# Phase Details: rubric-score-gate

Task ID: 2026-10-02-rubric-score-gate. Evidence IDs refer to the research artifact.

## P01 Rubric configuration and seed baseline

* P01-T01: Encode the 20 criteria from docs/reference/method/ama-capstone-assessment-guide.md (C1) with id, section, title, descriptor summary, and `live` flag for B1 to B5 and C2 (scored live; readiness estimate only, X-8). Sections A 35, B 35, C 15, D 15; floors 21, 21, 9, 9; criterion floor 1 fails; bands Distinction 90, Merit 78, Pass 66.
* P01-T02: Registry entries: id, title, globs, extractor (`text` or `pptx`), status (`active` or `planned`), criteria informed. Only `brd` is active today, glob `docs/brds/**/*.md`. Planned globs: `docs/prds/**/*.md`, `docs/adrs/**/*.md` and `docs/planning/adrs/**/*.md`, `src/**`, `infra/**`, `docs/presentations/*.pptx`, `docs/pitch/**/*.{md,vtt,txt}`, `docs/thought-leadership/**/*.md`. Planned entries with no matching files are ignored, so activation is automatic when files appear; the `status` field documents intent only.
* P01-T03: Seed from docs/reference/research/company/capstone-brd-rubric-review.md:44-66 (C3). Fields: schema_version, source `manual-seed`, total 61, sections, criteria (score, rationale), fingerprints `{}`, instrument_fingerprint null.
* P01-T04: `.gitattributes` line `.github/rubric/scores/history.jsonl merge=union`.

Done when JSON parses and seed total equals 61.

## P02 Deterministic scripts

* P02-T01 prepare.py:
  * `decide`: compute per-artifact SHA-256 over sorted matched files and an instrument fingerprint over rubric.json, artifacts.json and the workflow `.md`; load baseline from `git show <base-ref>:.github/rubric/scores/latest.json`; `should_score` true when baseline is missing, seeded, or any fingerprint differs. Write `should_score`, `baseline_total`, `changed` to `$GITHUB_OUTPUT`.
  * `context`: write `/tmp/gh-aw/agent/rubric/context.json` (baseline scorecard, fingerprints, changed artifacts, file lists) and extract PPTX slide and notes text with zipfile + ElementTree to `/tmp/gh-aw/agent/rubric/extracted/`.
* P02-T02 gate.py: read `$GH_AW_AGENT_OUTPUT`, select last `record_rubric_score` item, parse `scorecard` JSON, validate ids and score range, compute sections, floors, band, compare with baseline (OD-1), list per-criterion drops, write new latest.json and append history.jsonl, write markdown report and a decision JSON for the workflow steps.

Done when both scripts compile and handle missing inputs with exit code 2 and invalid scorecards with a failing decision.

## P03 Agentic workflow

* Frontmatter: triggers FR-1, `permissions: contents read, pull-requests read`, `engine: copilot` with pinned model, `checkout.fetch: ["main"]`, `fetch-depth: 0`, `timeout-minutes: 20`, `max-ai-credits`, `network: defaults`, `tools.github` read toolsets, `jobs.rubric_prepare` (statuses write) with outputs, `jobs.agent.needs/if`, `steps:` running prepare.py context, `safe-outputs.jobs.record-rubric-score` with input `scorecard` (string), permissions contents/pull-requests/statuses/issues write.
* Gate job steps: checkout PR head or main (fetch-depth 0); run gate.py; set statuses; upsert sticky comment; submit review with fallback; commit and push scores; on push events, push to main or open issue. Use actions/github-script for API calls.
* Prompt: rubric path, context path, scoring rules (evidence citations, carry-forward, live caps, no inflation), injection guard, output schema, single tool call.

## P04 Setup documentation and validation

* README: purpose, flow diagram, owner setup (secret, Actions approval setting, gh aw install and compile, branch protection with required status `rubric/score`), first-run bootstrap, adding an artifact type, cost and limitations.
* Validation: `get_errors` on all new files; optional local run `python .github/rubric/scripts/prepare.py decide` when the terminal works; otherwise record as pending live execution.
