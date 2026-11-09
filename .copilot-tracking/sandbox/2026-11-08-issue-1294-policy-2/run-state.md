# Run state: issue-1294 policy behavior test, run 2 (correction C1)

* Run type: full (earlier run 1 was lead-designed, proxy, and did not grade the examples table; not eligible for reuse)
* Targets (working tree on top of HEAD 397ce435ae4dddfcf9279179656049b8b670b720, uncommitted):
  * .github/copilot-instructions.md (instructions, validation paragraph)
  * src/README.md (guide: Local RPI gate lead, Hosted CI versus local gate coverage section, direct-check list, policy examples table)
  * .github/agents/ama-backlog-delivery-coordinator.agent.md (agent, local validation tiers paragraph)
* Target profile: Medium. Canonical first model: GPT-5.6 Terra.
* Model resolution: the host task tool disallows a model override unless the request requires one, so every dispatch omits the model. The executed model is the host default and is not proven to be the Medium profile. Profile status: unresolved, proxy. Any Pass is proxy evidence only, never intended-profile.
* Fidelity: simulation (read-only literal conformance; no native execution)
* Retain sandbox: YES (owner instruction). Nothing is deleted.
* Containment: executor and grader read-only; lead persists returns; synthetic data only; no network, Azure, provider, Docker, SQL.
* Independence: fresh generic design subagent given no lead-drafted scenarios; separate fresh generic grading subagent given the examples table and the full employee-chat contract.
* Requirements:
  * R1 direct employee-chat check restates the runner contract: pinned axe digest, three ordered states, positive integer passes, PASS employee chat: marker, no skips or violations; selector named, exactly one test, zero skips.
  * R2 coverage labels accurate: Shared, Local-only, Hosted-only (only artifact upload and hosted runner, matrix, path filter are hosted-only).
  * R3 impact-based classification of workflow, gate-tool, dependency and Dockerfile edits; no categorical full or safe tier; full tier kept for security-sensitive, infrastructure, deployment, SQL, major, release, mixed, unresolved.
  * R4 the policy examples table: documentation-only, small employee chat, SQL, Bicep or security, mixed, workflow or tool.
  * R5 absent, path-filtered or skipped CI is never a pass; the full tier is never a partial or --changed receipt; no blanket --changed for small tiers.
* Pre-run workspace status: 4 modified policy files; 4 untracked C1 research, plan, details and critique files; ignored tools/__pycache__.
