---
description: "Primary research artifact for Issue #185 PR #1801 c2 src-api credential-hygiene failure remediation"
---
<!-- markdownlint-disable-file -->

# Task Research: simulated-device-identity-provisioning-185-c2

| Field              | Value                                                                                         |
|--------------------|-----------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                    |
| Researcher / agent | rpi-research (coordinated by RPI Agent automatic session)                                     |
| Status             | Complete                                                                                      |
| Artifact path      | .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md |

## Research Brief

* What to research: Exact root cause, regex line-bridging behavior, and surgical remediation for the `src-api` hosted CI failure (`test_iot_credential_hygiene.SourceScanTests.test_no_device_key_or_connection_string_in_repository_text`) on `PR #1801` (`headRefOid` `ffce28c98fa284a3445a93d4c2250966099c250f`, branch `feat/iot-185-device-provisioning` targeting `feat/demo-164-chat-grounding-provenance-0900` / `PR #1641`).
* Why it matters: Commit `ffce28c98` passed `9/10` CI checks (`src-core`, `mssql`, `src-namespace`, `src-agents`, `src-importer`, `src-orchestrator`, `image-paths`, `src-changes`, `src-no-working-data`) and failed solely in `src-api` because negative secret-redaction unit tests in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` contain literal contiguous synthetic secret fixtures in Python source text that match `test_iot_credential_hygiene.PATTERNS`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, `rpi-review`, and coordinator verification of the frozen local commit on `feat/iot-185-device-provisioning`.
* Scope: `src/api/tests/test_iot_credential_hygiene.py`, `src/core/tests/test_live_provisioning.py`, `src/core/tests/test_device_provision.py`, `src/core/tests/test_device_identity.py`, `src/core/pyproject.toml`, and `.github/workflows/src-ci.yml`.
* Non-goals: Modifying `src/api/tests/test_iot_credential_hygiene.py` scanner patterns or weakening secret scanning, changing runtime behavior of `zava_forward.core.synthetic` production modules, pushing to remote, or running `gh pr create`.
* Criteria: Reproduce the exact 3-item `AssertionError` locally, verify every `PATTERNS` regex (including greedy `[^\n]*` single-line bridging under `ruff format` at `line-length = 100`), ensure runtime strings passed to functions under test remain character-for-character identical, and confirm Focused validation tier requirements under owner decision D4 / Issue #1294.
* Requested outputs: Primary `c2` research artifact with `C#` codebase evidence, contrarian regex-bridging analysis, converged remediation approach, and Planning Readiness.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                        |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q4 covering CI failure reproduction, `PATTERNS` regex mechanics under Ruff formatting, runtime fixture invariance, and validation tier |
| Codebase scope                       | `src/api/tests/test_iot_credential_hygiene.py`, `src/core/tests/`, `src/core/pyproject.toml`, `.github/workflows/src-ci.yml` |
| External scope                       | none (bounded internal repository and PR #1801 check-run metadata)                                                           |
| Initial internal candidate areas     | `src/api/tests/test_iot_credential_hygiene.py`, `src/core/tests/test_live_provisioning.py`, `src/core/tests/test_device_provision.py` |
| Initial external candidate areas     | none                                                                                                                         |
| Research posture                     | focused                                                                                                                      |
| Posture provenance                   | caller-specified (bounded internal `c2` CI test-fixture remediation with named files and Focused validation tier)            |
| Explicit limits / deadline           | Focused validation tier; commit locally on `feat/iot-185-device-provisioning`; do not push or run `gh pr create`             |
| Posture-specific completion basis    | focused scope and materiality                                                                                                |
| Edits allowed during research?       | no, research-only                                                                                                            |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                         |
| Known constraints / excluded sources | Keep literal matches of `PATTERNS` out of source, tests, and tracking artifacts; no `.copilot-tracking/` refs in code/commits |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                     | Match and provenance                                         | Scoped authority or output contract                                       | Selected / skipped reason                                                                 |
|---------------------|-----------------------------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA rules) | `applyTo: "**"` matches repository inputs and evidence paths | Enforces D4/#1294 validation tiers, `src-ci.yml` parity, and commit rules | Selected: binding repository guidance for validation tier and local git commit metadata   |
| Skill               | `python-foundational`                         | Semantic match to Python unit tests, Ruff, and mypy          | General Python quality conventions                                        | Skipped: exact commands and `pyproject.toml` rules are already defined in repository code |
| Skill               | `web-design-guidelines`                       | Applies only to `src/api/src/zava_forward/api/web/` edits    | Web UI review rules                                                       | Skipped: zero web UI files are touched in `c2`                                            |
| Research specialist | `hve-core-all:rpi-researcher`                 | Registered host subagent for independent research lanes      | Delegated lane artifact under `subagents/`                                | Skipped (inline): tightly coupled 3-file regex/test trace completes directly in 1 wave set |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered              | Resulting decision or selected further research                                                       |
|------------------|---------------------------------------------------------------------------------------------------------------------------|-----------------------------------|-------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller root cause, target test files, Focused validation commands, and no-push rule | Unanswered (non-interactive)      | Proceed in `focused` posture on `feat/iot-185-device-provisioning`                                    |
| Direction change | Wave 3 contrarian regex trace found that `PATTERNS["device connection string"]` and `PATTERNS["shared access signature"]` use `[^\n]*`, which can bridge `" + "` on a single 100-char Ruff-formatted line unless the token keywords themselves are split | Not needed (resolved within scope) | Split token keywords (`"Host" + "Name="`, `"SharedAccess" + "Key="`, `"SharedAccess" + "Signature "`, `"-----BEGIN " + "PRIVATE KEY-----"`) in addition to key payload fragments |
| Convergence      | Single Cycle 1 resolved Q1-Q4 with deterministic local reproduction and high-confidence codebase evidence                 | Not needed (automatic RPI mode)   | Mark Planning Readiness `Ready` and hand off to `rpi-plan`                                            |

## Scope and Success Criteria

* Scope: Inspect `PR #1801` CI status, `src/api/tests/test_iot_credential_hygiene.py`, `src/core/tests/test_live_provisioning.py`, `src/core/tests/test_device_provision.py`, `src/core/pyproject.toml`, and `.github/workflows/src-ci.yml`.
* Assumptions:
  * Only `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` fail `test_no_device_key_or_connection_string_in_repository_text` across the repository (`src/`, `infra/`, `docs/`, `.github/`). (Verified in Cycle 1.)
  * Naive concatenation on a single line could still trigger `[^\n]*` lookahead/bridging patterns if `ruff format` joins adjacent string literals or `+` expressions onto one line. (Verified in Cycle 1 Wave 3.)
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Remediate the 3 `test_iot_credential_hygiene` findings in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` by assembling synthetic secret test inputs at runtime via string concatenation/multiplication while keeping runtime inputs identical and source matches at 0.
  * Validate with `src/core` provisioning unit tests, `src/api/tests/test_iot_credential_hygiene.py`, `ruff check`, `ruff format --check`, and `mypy` in `src/core`.
  * Write dated `c2` RPI artifacts under `.copilot-tracking/` and create one frozen clean local commit without pushing.
* Inferred research questions:
  * Why did `c1` (`src-core`) pass while `src-api` failed, and can `src/core/tests/test_live_provisioning.py` also guard `src/core` test sources directly so `src-core` catches any future literal fixture regression immediately?
  * How do `ruff` (`select = ["E", "F", "I", "B", "UP"]`, `line-length = 100`) and `mypy` (`strict = true`) interact with runtime string assembly in `src/core/tests/`?
* Caller constraints and non-goals: Research phase is strictly read-only; Focused validation tier; do not modify `src/api/tests/test_iot_credential_hygiene.py`; do not push or open a PR.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Restrict code edits to `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` under Focused tier | Caller intake | Preserves `src/core` production modules and `src/api` credential-hygiene scanner unchanged |
| exclude                                                  | Do not push or run `gh pr create`; leave clean local commit for coordinator review                      | Caller intake       | Bounds Implement closeout to local git commit verification                         |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | What exact CI checks ran on `PR #1801` (`ffce28c98`), and does `test_iot_credential_hygiene.py` reproduce the identical 3 findings locally?       | straightforward                          | H        | answered |
| Q2 | Which exact lines in `src/core/tests/` match or nearly match `test_iot_credential_hygiene.PATTERNS`, and how do those regexes behave across `+` concatenation and `ruff format`? | depth | H | answered |
| Q3 | How can synthetic test fixtures be assembled at runtime so the strings passed into functions under test remain 100% byte-for-byte identical while preventing regressions in `src-core`? | depth | H | answered |
| Q4 | Does Focused validation tier apply under owner decision D4 / Issue #1294, and what exact commands mirror `.github/workflows/src-ci.yml`?          | straightforward                          | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/simulated-device-identity-provisioning-185-state.json`, `.copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-research.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`.
* Reused (verified) findings: Commit `ffce28c98` implemented `zava_forward.core.synthetic.live_provisioning`, aligned `device_identity.py` and `device_provision.py`, and passed all 24 tests in `test_device_provision.py` + `test_live_provisioning.py` as well as hosted `src-core` CI (`C1`, `C2`, `C7`).
* Superseded / stale: `c1` `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` (`src/core/tests/test_live_provisioning.py:132-145`) only AST-scanned production modules (`live_provisioning.py`, `device_identity.py`, `device_provision.py`) and did not scan `src/core/tests/` or execute `src/api/tests/test_iot_credential_hygiene.py` during Focused `src/core`-only validation (`C4`).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (test fixture assembly in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` under Focused tier); exclude (no push or `gh pr create`).
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: Read-only execution during Research; Focused validation tier and frozen local commit bound downstream phases.

#### Wave 1: Wider

* Plan and independent lanes: Inline inspection of `git show --stat ffce28c98`, `gh pr view 1801 --json ... statusCheckRollup`, `src/api/tests/test_iot_credential_hygiene.py`, `.github/workflows/src-ci.yml`, and repository-wide `grep` across `src/` and `tools/` for `SharedAccessKey`, `PATTERNS`, and credential-hygiene scanners.
* Worker evidence relationships or inline fallback: Inline execution mapped Q1 -> `PR #1801` passed `9/10` checks and failed only `src-api` (`job/132858346342`), reproduced identically locally with `test_iot_credential_hygiene.py` returning the exact 3 findings (`C1`, `C2`, `C3`).
* Reflection: `test_iot_credential_hygiene.py` is the sole repository-wide text scanner (`SCANNED = ("src", "infra", "docs", ".github")`, `C3`). Wave 2 needs line-level inspection of every secret-shaped constant and string literal in `src/core/tests/`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact regex definitions in `src/api/tests/test_iot_credential_hygiene.py:42-53`, all occurrences of `SharedAccess*`, `azure-devices`, `HostName`, `PRIVATE KEY`, and base64 fixtures across `src/core/tests/`, and `src/core/pyproject.toml` Ruff/mypy rules.
* Plan and independent lanes: Inline `view` and `grep -n` across `src/core/tests/test_live_provisioning.py`, `src/core/tests/test_device_provision.py`, `src/core/tests/test_device_identity.py`, and `src/core/tests/test_device_registry_azure.py`, plus `src/core/pyproject.toml`.
* Worker evidence relationships or inline fallback:
  * `src/core/tests/test_live_provisioning.py:15-28` defines module constants `RAW_KEY_B64`, `RAW_CONN_STR` (single-line f-string triggering `"device connection string"`), `RAW_SAS_TOKEN` (implicit multi-line literal), and `RAW_PEM` (implicit multi-line literal whose opening header triggers `"private key block"`) (`C4`).
  * `src/core/tests/test_device_provision.py:132-136` passes a contiguous `"Owner SharedAccess" + "Key=..."` literal inside `test_report_refuses_secret_bearing_credential_owner`, triggering `"shared access key value"` (`C5`).
  * `src/core/pyproject.toml:26-39` enforces `ruff` `line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`, and `mypy` `strict = true` across `files = ["src", "tests"]` (`C6`).
* Reflection: Identified all 3 failing literals plus adjacent multi-line `RAW_SAS_TOKEN` and `RAW_KEY_B64` constants. Wave 3 must challenge whether simple `+` concatenation between segments (`"HostName=...;" + "DeviceId=...;" + "SharedAccessKey="`) could still match `PATTERNS` on a single source line.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge (1) whether `PATTERNS` regexes in `test_iot_credential_hygiene.py` can match across `" + "` Python syntax on the same line, (2) whether `ruff` (`UP`/`B`/`ruff format`) rewrites string `+` concatenation back into contiguous literals, (3) whether `.copilot-tracking/` or `docs/` files added in `ffce28c98` match `PATTERNS`, and (4) whether D4/#1294 permits Focused tier here.
* Plan and independent lanes: Character-by-character trace of `PATTERNS` (`src/api/tests/test_iot_credential_hygiene.py:42-53`), inspection of `test_iot_credential_hygiene.py:184-194` (`test_scanner_detects_each_pattern`), audit of `SCANNED` roots, and D4/#1294 rules in `.github/copilot-instructions.md`.
* Worker evidence relationships or inline fallback:
  * **Critical regex-bridging discovery (`C3`)**: `PATTERNS["device connection string"]` uses `[^\n]*` between the `.azure-devices.net;` host prefix and `(?:SharedAccessKey|x509)\s*=`, and `PATTERNS["shared access signature"]` uses lookaheads `(?=[^\n]*\bsr=\S)(?=[^\n]*\bsig=\S)` after `SharedAccessSignature\s+`. Because `[^\n]*` matches quotes, spaces, and `+` operators on the same line, writing `"HostName=hub.azure-devices.net;" + "DeviceId=d;" + "SharedAccessKey="` on a single `<100`-character line STILL matches `"device connection string"`! (`test_iot_credential_hygiene.py` only escaped flagging its own line 99 because line 176 passes `this = Path(__file__).resolve()` as `skip` to `scan_directory`, `C3`.)
  * **Mitigation (`C3`, `C4`, `C5`)**: Splitting the pattern keywords and domain tokens themselves via runtime `+` / `"".join(...)` (for example `"Host" + "Name="`, `"azure-" + "devices.net"`, `"SharedAccess" + "Key="`, `"SharedAccess" + "Signature "`, `"-----BEGIN " + "PRIVATE KEY-----"`, `"-----END " + "PRIVATE KEY-----"`, and splitting the 44-char synthetic base64 key into two 22-char halves) guarantees 0 regex matches regardless of line wrapping, while `ruff` (`E,F,I,B,UP`) and `ruff format` preserve explicit `+` / `"".join(...)` expressions without constant-folding them (`C6`).
  * **Repository scope check (`C2`, `C3`)**: `SCANNED = ("src", "infra", "docs", ".github")` reported 0 findings in `src/core/README.md` or any other file in `ffce28c98`; `.copilot-tracking/` is outside `SCANNED`, and we also avoid writing literal secret-shaped strings in `.copilot-tracking/` artifacts per `rpi-research` secret-hygiene constraints.
  * **Self-guard in `src-core` (`C4`)**: Extending `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` (or adding a companion test in `test_live_provisioning.py`) to verify that `src/core` synthetic modules and their unit tests contain zero matches for credential-hygiene patterns ensures `src-core` catches any regression even when run standalone.
  * **Validation tier (`C8`, `C9`)**: Test-only remediation in `src/core/tests/` modifies no production code, SQL, infra/Bicep, Dockerfiles, workflows, `src/api/checks/` browser scripts, or `src/api/src/zava_forward/api/web/` files, confirming Focused validation tier under D4 / Issue #1294.
* Reflection: Contrarian analysis caught a subtle `[^\n]*` single-line regex bridging trap before planning and confirmed that splitting keywords + payload halves keeps runtime values 100% identical while guaranteeing 0 source-scan matches under any formatter layout.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Assemble synthetic secret fixtures in `test_live_provisioning.py` and `test_device_provision.py` at runtime by splitting both marker keywords (`Host`+`Name`, `azure-`+`devices.net`, `SharedAccess`+`Key`, `SharedAccess`+`Signature`, `-----BEGIN `+`PRIVATE KEY-----`) and base64 key halves | `C2`, `C3`, `C4`, `C5`, `C6` | accepted | Preserves byte-for-byte identical runtime strings passed to functions under test while eliminating both contiguous matches and `[^\n]*` single-line bridging matches under `ruff format` | Selected convergence recommendation |
| Add a focused source-hygiene assertion in `test_live_provisioning.py` covering `src/core` synthetic production and test files alongside running `src/api/tests/test_iot_credential_hygiene.py` | `C3`, `C4`, `C7` | accepted | Directly prevents `src/core`-only test runs from missing test-file credential-hygiene regressions in future cycles while adding negligible runtime (<5 ms) | Included in convergence plan |
| Exclude `src/core/tests/` inside `src/api/tests/test_iot_credential_hygiene.py` | `C3` | rejected | Violates caller scope and weakens repository-wide Issue #184 criterion 3 credential hygiene scanning | Recorded as rejected alternative |
| Replace synthetic fixtures with non-matching dummy strings (e.g., `"not-a-secret"`) | `C4`, `C5`, `C7` | rejected | Would stop exercising the negative regex redaction and secret-rejection branches in `live_provisioning.py` and `device_provision.py` | Recorded as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Q1-Q4 are completely answered with verified local reproduction and exact `path:line` codebase evidence; zero open conjectures remain.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`-`C9`)

## Evidence Log

* Delegation: inline: bounded 2-file unit-test remediation where direct regex inspection and local test reproduction completed in under 8 tool calls.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | Commit `ffce28c98` on `feat/iot-185-device-provisioning` (`PR #1801` -> `feat/demo-164-chat-grounding-provenance-0900`) passed `9/10` CI checks (`src-core`, `mssql`, `src-namespace`, `src-agents`, `src-importer`, `src-orchestrator`, `image-paths`, `src-changes`, `src-no-working-data`) and failed solely on `src-api` (`job/132858346342`) | `.copilot-tracking/rpi-sessions/2026-11-15/simulated-device-identity-provisioning-185-state.json:1-45` | bash (`git show`, `gh pr view 1801`) | high | Verified exact head `ffce28c98fa284a3445a93d4c2250966099c250f` |
| C2 | Running `src/api/tests/test_iot_credential_hygiene.py` locally fails `test_no_device_key_or_connection_string_in_repository_text` with the exact 3 findings (`test_live_provisioning.py: device connection string`, `test_live_provisioning.py: private key block`, `test_device_provision.py: shared access key value`) | `src/api/tests/test_iot_credential_hygiene.py:175-182` | bash (`unittest`) | high | 11/12 tests pass; 1 fails with identical list diff |
| C3 | `PATTERNS` scans `SCANNED = ("src", "infra", "docs", ".github")` (skipping only `test_iot_credential_hygiene.py` itself via `skip=this`) and uses greedy `[^\n]*` in `"device connection string"` and `"shared access signature"`, plus contiguous keyword checks in `"shared access key value"` and `"private key block"` | `src/api/tests/test_iot_credential_hygiene.py:24-53` | view | high | Explains why single-line `" + "` without keyword splitting can still match `[^\n]*` |
| C4 | `test_live_provisioning.py` defines contiguous literal fixtures `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, and `RAW_PEM` at module top and scans only production modules (`live_provisioning.py`, `device_identity.py`, `device_provision.py`) in `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` | `src/core/tests/test_live_provisioning.py:15-28` | view / grep | high | Lines 17 and 25 trigger the 2 `test_live_provisioning.py` findings; line 220 also holds a 36-char fragment |
| C5 | `test_device_provision.py` passes a single contiguous string literal containing a synthetic `SharedAccess` key assignment inside `test_report_refuses_secret_bearing_credential_owner` | `src/core/tests/test_device_provision.py:132-138` | view / grep | high | Line 134 triggers the `test_device_provision.py` finding |
| C6 | `src/core/pyproject.toml` sets `line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`, and `mypy` `strict = true` across `files = ["src", "tests"]`, with neither `test_live_provisioning.py` nor `test_device_provision.py` excluded | `src/core/pyproject.toml:26-52` | view | high | Explicit `"".join((...))` or `+` across tuple/string parts satisfies Ruff `E,F,I,B,UP` and strict mypy |
| C7 | Existing `src/core` provisioning tests (`test_device_provision.py` and `test_live_provisioning.py`, 24 tests) pass in `0.102s` and rely on the runtime string values of `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and the secret-bearing owner input to test redaction and rejection | `src/core/tests/test_live_provisioning.py:118-315` | bash (`unittest`) | high | Runtime fixture strings must remain byte-for-byte identical |
| C8 | `Source projects CI` runs `python -m unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` inside `src/${{ matrix.project }}` | `.github/workflows/src-ci.yml:81-95` | view | high | Confirms exact hosted CI commands for `src-core` and `src-api` |
| C9 | Focused validation tier applies under owner decision D4 / Issue #1294 when a small test-only fix touches no SQL, Bicep/infra, Dockerfiles, workflows, `src/api/checks/` scripts, or `src/api/src/zava_forward/api/web/` assets | `.github/copilot-instructions.md:72-108` | view | high | Basis for Focused validation tier classification |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* `none`

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `PR #1801` (`ffce28c98`) passed `9/10` CI checks and failed only `src-api` on `test_no_device_key_or_connection_string_in_repository_text` with 3 exact matches across `test_live_provisioning.py` and `test_device_provision.py`, reproduced 1-for-1 locally. | `C1`, `C2` | high | Confirms exact bounded remediation scope with no hidden repository-wide matches. |
| Q2 | `PATTERNS` matches contiguous `SharedAccess` key assignments and `-----BEGIN ... PRIVATE KEY-----` headers, and uses greedy `[^\n]*` on single lines for connection strings and SAS signatures, meaning naive single-line `" + "` concatenation without splitting keywords can still match after `ruff format`. | `C3`, `C4`, `C5`, `C6` | high | Split both marker keywords/domains and base64 payload halves via `"".join(...)` / `+` so no line can match regardless of formatting. |
| Q3 | Assembling `RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and the `test_device_provision.py` owner string from split parts yields byte-for-byte identical runtime values while keeping literal source text 100% clean; adding a `src/core` test-source hygiene check prevents future standalone `src-core` blind spots. | `C4`, `C5`, `C7` | high | Preserves all 24 negative secret-rejection/redaction assertions and adds local `src-core` regression protection. |
| Q4 | Focused validation tier applies under D4 / Issue #1294: run targeted `src/core` tests, `src/api/tests/test_iot_credential_hygiene.py`, full `src/core` unit tests, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core`. | `C6`, `C8`, `C9` | high | Ready for `rpi-plan` with deterministic verification commands. |

## Key Discoveries

* `test_iot_credential_hygiene.py` skips scanning itself (`skip=this` at line 176), which is why single-line `"HostName=...;SharedAccessKey=" + "A" * 24` inside `test_iot_credential_hygiene.py` passes while the same pattern in any other file would still trigger `PATTERNS["device connection string"]` due to greedy `[^\n]*` (`C3`).
* Splitting both the credential keywords (`"Host" + "Name="`, `"azure-" + "devices.net"`, `"SharedAccess" + "Key="`, `"SharedAccess" + "Signature "`, `"-----BEGIN " + "PRIVATE KEY-----"`) and base64 payload halves via `"".join((...))` / `+` guarantees 0 source matches under any `ruff format` line-wrapping while producing identical runtime strings (`C3`, `C4`, `C5`, `C6`).
* Expanding `test_source_modules_contain_no_embedded_keys_connection_strings_or_sas_tokens` in `src/core/tests/test_live_provisioning.py` to also scan `src/core` synthetic test files closes the cross-package feedback gap between `src-core` and `src-api` (`C4`, `C8`).

### Complete Examples

```python
RAW_KEY_B64 = "".join(("K9mP2vX8qL4nR7tY1wZ5bC", "3dF6gH0jM8pQ2sV4xN6zA="))
RAW_CONN_STR = "".join(
    (
        "Host",
        "Name=zava-sim-hub.",
        "azure-devices.net;DeviceId=SIM-TEST01;",
        "SharedAccess",
        "Key=",
        RAW_KEY_B64,
    )
)
RAW_SAS_TOKEN = "".join(
    (
        "SharedAccess",
        "Signature ",
        "sr=zava-sim-hub.",
        "azure-devices.net%2Fdevices%2FSIM-TEST01",
        "&sig=",
        "AbCdEfGhIjKlMnOpQrStUv",
        "WxYz0123456789%2B%2F%3D%3D&se=1999999999",
    )
)
RAW_PEM = "".join(
    (
        "-----BEGIN ",
        "PRIVATE KEY-----\n",
        "MIIEvgIBADANBgkqhkiG9w0BAQEF",
        "AASCBKgwggSkAgEAAoIBAQC7\n",
        "-----END ",
        "PRIVATE KEY-----",
    )
)
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Reconstruct the synthetic secret test inputs in `src/core/tests/test_live_provisioning.py` (`RAW_KEY_B64`, `RAW_CONN_STR`, `RAW_SAS_TOKEN`, `RAW_PEM`, and the 36-char assertion fragment) and `src/core/tests/test_device_provision.py` (`test_report_refuses_secret_bearing_credential_owner`) at runtime using tuple `"".join((...))` / string concatenation across split keyword, domain, and base64 segments so runtime values remain byte-for-byte identical while source literals contain 0 matches for `test_iot_credential_hygiene.PATTERNS`; extend `test_live_provisioning.py` source-hygiene coverage to scan the synthetic test files as well.
* Rationale: Directly eliminates all 3 CI failure findings and prevents `[^\n]*` single-line regex bridging under `ruff format` (`line-length = 100`), keeps every negative redaction and refusal unit test exercising identical runtime inputs, and satisfies strict `mypy` and `ruff` (`E,F,I,B,UP`) without touching `src/api` scanner rules.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`
* Implementation impact: Surgical edits to 2 test files (`src/core/tests/test_live_provisioning.py`, `src/core/tests/test_device_provision.py`) plus dated `c2` `.copilot-tracking/` artifacts.
* Confidence: high: reproduced failure locally and verified exact regex mechanics against `PATTERNS`.

File tree:

```text
src/core/tests/
├── test_device_provision.py      (modify: assemble secret-bearing owner string at runtime)
└── test_live_provisioning.py     (modify: assemble synthetic secret constants at runtime + assert test-file source hygiene)
```

### Alternative: Single-line `+` concatenation without splitting keywords

* Approach: Keep `"HostName=zava-sim-hub.azure-devices.net;" + "DeviceId=SIM-TEST01;" + "SharedAccessKey=" + RAW_KEY_B64` without splitting `HostName`, `azure-devices.net`, or `SharedAccessKey`.
* Trade-offs: Slightly shorter tuple/expression, but vulnerable to `PATTERNS["device connection string"]` (`HostName=[^;\s]+\.azure-devices\.net;[^\n]*(?:SharedAccessKey|x509)\s*=`) whenever `HostName=...azure-devices.net;` and `SharedAccessKey=` land on the same source line.
* Evidence refs: `C3`, `C6`
* Rejection rationale: Fragile under 100-column `ruff format` because `[^\n]*` matches across `" + "` on a single line.

### Alternative: Skip `src/core/tests/` in `src/api/tests/test_iot_credential_hygiene.py`

* Approach: Add `test_live_provisioning.py` and `test_device_provision.py` to an allowlist in `test_iot_credential_hygiene.py`.
* Trade-offs: Avoids editing `src/core/tests/`, but weakens the repository-wide credential-hygiene gate (Issue #184 criterion 3) and violates explicit caller instructions.
* Evidence refs: `C3`
* Rejection rationale: Out of scope and weakens security hygiene coverage across `src/core/tests/`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: none
* Follow-up: Coordinator push of the frozen local `c2` commit on `feat/iot-185-device-provisioning` to trigger hosted `PR #1801` CI (`10/10` check verification).
* Residual uncertainty: none within repository scope; local `test_iot_credential_hygiene.py` executes the exact same `SourceScanTests` logic as hosted `src-api` CI (`C2`, `C8`).

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Split both credential marker keywords and base64 payload halves at runtime via `"".join((...))` / `+` in `test_live_provisioning.py` and `test_device_provision.py` | confirmed | evidence / caller | Preserves identical runtime strings while preventing both contiguous and `[^\n]*` single-line regex matches | `C3`, `C4`, `C5`, `C6`, `C7` | Zero production code edits; deterministic `0`-finding scan in `test_iot_credential_hygiene.py` |
| Classify `c2` validation as Focused tier (D4 / Issue #1294) and run `src/core` tests, `test_iot_credential_hygiene.py`, `ruff check`, `ruff format --check`, and `mypy` | confirmed | caller / repo instructions | Test-only change in `src/core/tests/` touches no SQL, infra, workflows, `checks/` scripts, or `web/` UI | `C8`, `C9` | Complete local verification parity with `src-core` and `src-api` unit/hygiene checks without external `rpi-checks.py` gate |
| Commit locally on `feat/iot-185-device-provisioning` with `Refs #185` and Co-authored-by trailer without pushing | confirmed | caller constraint | Leaves clean frozen HEAD for coordinator review and batch push | `C1` | No remote side effects during `c2` session |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Push frozen `c2` commit and merge `PR #1801` after `PR #1641` | Coordinator review and hosted CI re-run after push | Coordinator / repository owner | Required to turn hosted `PR #1801` `src-api` check green | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Optional CLI `--id-scheme sim-dps` ergonomics in `device_provision.py` | Unifies CLI flag over `SYN-*` and `SIM-*` | Separate follow-up issue/request after `PR #1801` lands | deferred | `Q3`; `C1` |

## Planning Readiness

* Status: Ready
* Decision state: Converged on runtime tuple-joined / concatenated fixture assembly in `src/core/tests/test_live_provisioning.py` and `src/core/tests/test_device_provision.py` plus test-source hygiene assertion under Focused validation tier.
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`
* Preconditions met: Exact failure reproduced locally; all 4 `PATTERNS` regexes traced against `ruff format` 100-char wrapping; runtime input invariance verified; `ruff` and `mypy` available locally.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                      |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                     |
| Lane evidence or inline fallback | Inline execution (`C1`-`C9`); 3-file coupled test/regex trace needed no subagent split                        |
| Research disposition             | executed                                                                                                      |
| Planning Readiness               | Ready (`C1`-`C9`)                                                                                             |
| Blockers                         | none                                                                                                          |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `Plan`                                               |

## Advisory Next Step

| Field                            | Record                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                      |
| Planning Readiness               | Ready (`C1`-`C9`)                                                                                             |
| Output mode and planning support | convergence; yes (converged surgical test-fixture remediation ready for `rpi-plan`)                           |
| Acting owner                     | confirmed automatic RPI Agent                                                                                 |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); pre-transition state write (pending) |
| Continuation result              | automatic continuation to `Plan` (`rpi-plan`)                                                                 |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/simulated-device-identity-provisioning-185-c2-research.md               |
| Notes for planning or re-entry   | Ensure split tokens avoid single-line `[^\n]*` bridging under 100-column `ruff format` and verify runtime values match `c1` byte-for-byte |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Single complete three-wave cycle saturated the bounded 2-file test-hygiene scope with deterministic local reproduction (`C2`) and full regex coverage (`C3`-`C7`).

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log (Cycle 1 Wider/Deeper/Contrarian/Synthesis/Re-entry), Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none
