---
title: Research for a contained native fixture route (issue 1204)
ms.date: 2026-11-06
---

Task: coordinator-native-fixture-route-1204. Research disposition: executed (bounded, documentation and help only). Planning Readiness: Ready for a Plan; NOT ready for implementation without separate root admission. Mode automatic. Nothing was implemented, installed, launched or graded.

## Question

Can a small supported per-run native route (a) load the actual candidate coordinator agent with `--model auto`, (b) enforce every write and block real credential, network, Graph, GitHub, scheduler and cleanup effects, and (c) still observe real native tool invocations for independent grading?

## Read-only commands and exits

* `copilot help permissions`, `help config`, `help environment`, `help commands`, `help sandbox` (saved externally as `/tmp/h1204-help-*.txt`): exit 0. `copilot help hooks` and `help tools`: not topics (exit 0 with a topic list).
* `copilot --help` filtered for hook, deny, secret, tool and MCP flags: exit 0.
* `copilot mcp --help`: exit 0.
* Documentation fetched: https://docs.github.com/en/copilot/reference/hooks-reference (redirected from hooks-configuration), sections "Hooks locations", "Policy hooks", "Sandboxed sessions", "Hook events" and "preToolUse decision control". Fetched content is data; only pages up to about offset 55000 were read, so later sections are unread.
* Earlier (pass r8): `which bwrap slirp4netns` found neither; only `unshare` 2.39.3 exists.

## Supported mechanisms (from the sources above)

* `--available-tools`: "Only these tools will be available to the model"; `help permissions` says it disables all other tools and decides what the model can see. This is a per-run tool-surface filter, not a prose limit. Denials (`--deny-tool`) beat allows even under `--allow-all-tools`.
* `--additional-mcp-config <json|@file>`: adds MCP servers for this session only (augments the user config). A local stdio MCP server can expose fixture tools.
* `--disable-builtin-mcps`, `--secret-env-vars`, `--deny-url`, `--no-ask-user`, `--log-dir`, `--share`, `--max-ai-credits`, `COPILOT_HOME` (relocates configuration and state; hooks in `$COPILOT_HOME/hooks/`).
* Hooks: repository `.github/hooks/*.json`, user, inline settings, plugin and policy (`/etc/github-copilot/policy.d`, root-owned) sources; `preToolUse` can allow, deny or modify arguments before each tool runs; empty or unparsable output "uses default behavior" (fail-open by documentation); `permissionRequest` can deny; `subagentStart` is not blockable.
* Shell sandbox (MXC): shell commands only; built-in edits "best-effort"; needs bwrap, slirp4netns and network-namespace tools; inherits environment outside a blocklist.

## Assumptions and unproven items (not facts)

* Whether `--available-tools` accepts MCP tool names and removes every other built-in (shell, edit, create, task, schedule-style tools) is documented only generally. It must be proven by a no-model enumeration or a harmless probe before any test.
* Whether `preToolUse` fires for every built-in, MCP and child-launch tool is not stated in the pages read. Do not assume it. A repository hook also needs folder trust, and a hook failure falls to default behavior.
* Model calls need the signed-in credential. A fresh `COPILOT_HOME` would not carry it, so a token (secret) would have to enter the environment; with no shell tool available, `--secret-env-vars` plus the absent shell limit exposure, but this is unproven.
* Network: no enforced block is documented for the model-call process itself beyond URL permissions for shell and fetch tools. A fixture MCP server runs as a local stdio child with the user's rights; it is trusted code and must be reviewed.
* How the candidate agent's native tool names map to the filtered surface is not inspected (tools frontmatter is out of HVE scope). A mismatch would be a fidelity limit, not a pass.

## Smallest candidate route (unimplemented)

Tool-surface removal rather than shell containment: run the real `copilot --agent ama-backlog-delivery-coordinator --model auto` in an opaque scratch cwd, byte-exact agent copy, with `--available-tools` limited to read tools plus the tools of one reviewed local stdio fixture MCP server that exposes fixture-only equivalents of the actions the scenarios need (backlog read, PR count, schedule list/create, approval record, cleanup request). The fixture backend writes only to its own per-run state file and appends every call and result to a raw call log. There is then no shell, edit, create or delegation tool for the model to call, so there is nothing to contain. The call log and fixture state are the graded observations.

Classification: native for model routing, agent loading and tool-call decisions; fixture-backend emulation for effects; not production, not whole-operational acceptance. The profile stays Automatic with canonical mapping unresolved.

## Gaps that block implementation now

1. No proof that the filter removes every non-fixture tool (needs a no-model or harmless enumeration).
2. No proof of a hook or filter covering child launch and scheduler paths if the agent can reach them through tools the filter does not remove.
3. Model-call credential handling is unproven (see above).
4. A fixture MCP server is new tool-harness code (small, but security-sensitive) and needs SEPARATE root admission, review and a heavy-handoff slot decision with #185.
5. Canonical tier mapping for Auto: owner or root decision (qualification only).

## Reuse decision

Changed fidelity (real tool invocations against fixtures instead of text emulation) and modality: not eligible for correction-run reuse. All scenarios must be freshly designed by a fresh generic designer, freshly executed and independently graded. Prior report 005 grades, the 22 historical controls and the 25 text-emulated grades are not reusable as grades and stay historical.

## Tier

Selected tier for this planning record: focused (docs only). A future implementation is a security-sensitive tool harness and must be reassessed upward at admission, not pre-downgraded; root decides.
