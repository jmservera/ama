---
title: Issue 440 bounded host validation
description: Mechanical metadata and reference checks with native discovery deferred
ms.date: 2026-10-23
---

## Result

Mechanical validation: Deferred.

Mode: validate. Intended profile: Low. Actual validator model is
runtime-resolved and unknown; no intended-profile execution claim is made.
The caller reports static Pass and behavior simulation Pass. Neither was
repeated or independently established here. This report does not grant
publication, hosted approval, cloud spending or coordinator execution authority.

Only this allocated report was deliberately written. No source, agent,
configuration or model setting was changed. Existing dirty inputs were retained.
No coordinator was selected or activated; no nested worker, GitHub operation,
Azure operation, application-model call, install, foreign process inspection,
other worktree read or foreign receipt read was performed.

## Inputs and identity

* Worktree: issue-440-stabilization.
* Branch: test/stabilization-checkpoints-440.
* HEAD: 140d8f494482c78e84d15f3d46b9223d3c487af0.
* Existing local origin/main reference:
  140d8f494482c78e84d15f3d46b9223d3c487af0.
  No fetch was requested or performed; this is not a freshness assertion.
* .github/agents/ama-backlog-delivery-coordinator.agent.md SHA256:
  f631224630d5cf9e33dd24581ed1c4248ef94680ef4122d3289f51db8957b18c.
* src/README.md SHA256:
  79785974fdcea57a934e6504305483a39f47e75c24be6a39c9435e697c13e0be.

Both supplied hashes matched on initial and final source checks. Both targets
were already modified on entry. The diff contained 98 changed agent lines and
53 added README lines, totaling 143 insertions and eight deletions.

Read both actual targets and the supplied canonical hve-builder
references/workflow-contract.md and references/stage-dispatch.md. Also read
required project context at docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md and
docs/reference/memory.md. These were bounded known-file reads, not a repository
discovery survey. Relative-link checks read only the directly linked targets.

## Check ownership and disposition

| Check | Owner | Status | Evidence |
| --- | --- | --- | --- |
| Exact requested source identities | local | Passed | Both SHA256 values matched |
| Metadata and unchanged non-tool frontmatter | local | Passed | Byte-equal to HEAD; agent keys remain name and description |
| Changed relative references and heading fragments | local | Passed | Four references resolved on corrected checker run |
| Scoped diff whitespace | local | Passed | git diff --check exited 0 without output |
| Actual native host discovery of coordinator | local | Deferred | No native agent list was obtained; see safe attempts below |
| Collection/plugin/extension distribution wiring | local | Skipped | Not applicable: existing repository-specific artifact |
| Hosted policy/publication checks | CI | Skipped | Not requested for this bounded validation; later independent gates remain |

No agent or subagent tools configuration was assessed. No non-tool
capability-bearing frontmatter was added, removed or changed. The unchanged
frontmatter contains no agents, hooks, handoffs or model declarations.
This preservation result is separate from runtime registration, which remains
unverified.

## Native discovery attempts

The authoritative fetch_copilot_cli_documentation tool was called first after
skill activation. Its README retrieval failed with ENOENT for the installed
README; its help result succeeded and documented:

```text
/agent - Browse and select agents: /agent [name]
```

CLI help was then inspected without activating a session. Exact relevant
commands and observed exits:

```bash
copilot --help
# exit 0
copilot --help | grep -A 4 -B 2 -E -- '--available-tools|--disable-builtin-mcps|--no-custom-instructions|--no-ask-user|--no-auto-update|--interactive|--config-dir|--disable.*plugin|--disable.*hook|--no.*network|--log|--banner|--silent|--stream'
# exit 0
copilot --help | grep -A 5 -B 2 -E -- '--disable|--deny-tool|--no-save|--ephemeral|--session|--plugin|--trust|--allow-all|--offline|--no-'
# exit 0
copilot --no-auto-update --available-tools --disable-builtin-mcps --no-custom-instructions --no-ask-user help /agent
# exit 1
copilot --no-auto-update help commands | grep -A 5 -B 3 -E '/agent|/exit|/env'
# pipeline exit 0
command -v bwrap
# exit 1, no output
command -v unshare
# exit 0: /usr/bin/unshare
command -v copilot
# exit 0: /home/azureuser/.nvm/versions/node/v24.21.0/bin/copilot
unshare --user --map-root-user --net --mount true
# exit 1
```

The actual help-topic attempt returned:

```text
Unknown help topic: /agent
Available topics:
  config
  commands
  limits
  environment
  logging
  monitoring
  permissions
  providers
  billing
  sandbox
```

The commands-help output confirmed the native interactive browser:

```text
/agent   Browse and select agents: /agent [name]
/env     Show loaded environment details (instructions, MCP servers, skills, agents, hooks, plugins, LSPs, extensions)
/exit    Exit the CLI; use 'print' to print the session after exiting alt screen
```

Relevant actual flag descriptions:

```text
--available-tools [<tools>...] Only these tools will be available to the model
--disable-builtin-mcps Disable all built-in MCP servers
--no-custom-instructions Disable loading of custom instructions from AGENTS.md and related files
--no-auto-update Disable downloading CLI updates automatically
--no-ask-user Disable the ask_user tool
-i, --interactive <prompt> Start interactive mode and automatically execute this prompt
```

These descriptions do not establish a read-only, no-network session-startup
boundary for plugins, custom MCPs or hooks. No configuration survey was
authorized to establish whether those startup surfaces are present. This is
uncertainty, not a finding that any such surface is configured or unsafe.
An empty model-tool allowlist is not proof that all host startup side effects
are blocked. No listing-only standalone command was established by the help
outputs. The controlled-PTY option therefore was not launched without an
independently enforced containment boundary.

The non-mutating namespace capability probe failed before launching Copilot:

```text
unshare: write failed /proc/self/uid_map: Operation not permitted
isolation_probe_exit=1
```

There was no PTY, no coordinator selection and no model submission. Help output,
file presence, parsed metadata and the current agent inventory are not accepted
as evidence that this exact candidate is natively discoverable.

Exact rerun condition: provide an approved host whose session startup is
demonstrably constrained against source/configuration mutations, external
operations and model submissions, with this worktree and the two exact hashes
above still present. In that host, run a controlled PTY using
`copilot --available-tools --disable-builtin-mcps --no-custom-instructions --no-ask-user --no-auto-update`,
submit only `/agent`, capture the native list showing
`AMA Backlog Delivery Coordinator`, dismiss the chooser without selecting any
agent, then exit using `/exit` or EOF and record the exact argv, transcript,
exit and before/after source identities. Alternatively, use a host-documented
non-mutating agent-list-only operation if one becomes available. Do not use
`--agent`, select the coordinator, or submit a natural-language prompt.

## Mechanical command evidence

Initial read-only commands included:

```bash
git status --short
git branch --show-current
sha256sum .github/agents/ama-backlog-delivery-coordinator.agent.md src/README.md
git --no-pager diff -- .github/agents/ama-backlog-delivery-coordinator.agent.md src/README.md
git --no-pager diff --stat -- .github/agents/ama-backlog-delivery-coordinator.agent.md src/README.md
git --no-pager diff --unified=0 -- .github/agents/ama-backlog-delivery-coordinator.agent.md src/README.md | head -150
git rev-parse HEAD
git rev-parse origin/main
```

These completed successfully. Initial status showed the two modified targets
and pre-existing untracked dated tracking directories plus
.copilot-tracking/sandbox/. No contents of unrelated tracking directories were
read or changed. Tool-generated overflow from the first large combined output
was not opened; bounded commands were used instead.

Final mechanical checker command, exit 0:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, re, subprocess
expected={'.github/agents/ama-backlog-delivery-coordinator.agent.md':'f631224630d5cf9e33dd24581ed1c4248ef94680ef4122d3289f51db8957b18c','src/README.md':'79785974fdcea57a934e6504305483a39f47e75c24be6a39c9435e697c13e0be'}
root=Path.cwd()
for name,digest in expected.items():
 p=Path(name); text=p.read_text(); baseline=subprocess.check_output(['git','show',f'HEAD:{name}'],text=True)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
 front=text.split('---',2)[1]; old=baseline.split('---',2)[1]
 assert front==old
 print(f'{name}: exact expected SHA256; unchanged frontmatter')
 if name.endswith('.agent.md'):
  assert re.findall(r'^([\w.-]+):',front,re.M)==['name','description']
  assert 'name: AMA Backlog Delivery Coordinator' in front
  assert 'description: ' in front
  print('Non-tool frontmatter keys: name, description; no capability-bearing keys added, removed or altered')
 diff=subprocess.check_output(['git','diff','--unified=0','--',name],text=True)
 added='\n'.join(line[1:] for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++'))
 for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',added):
  if '://' in ref: continue
  local,_,anchor=ref.partition('#'); target=(p.parent/local).resolve() if local else p.resolve()
  assert target.is_relative_to(root) and target.exists(),ref
  if anchor:
   headings=re.findall(r'^#{1,6}\s+(.+?)\s*#*$',target.read_text(),re.M)
   anchors=[re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-') for heading in headings]
   assert anchor in anchors,ref
  print(f'Changed reference resolves: {name} -> {ref}')
check=subprocess.run(['git','diff','--check','--',*expected],capture_output=True,text=True)
print(f'git diff --check -- .github/agents/ama-backlog-delivery-coordinator.agent.md src/README.md: exit={check.returncode}; stdout={check.stdout!r}; stderr={check.stderr!r}')
assert check.returncode==0
report=Path('.copilot-tracking/hve-builder/2026-10-23/issue-440-host-1.md')
assert not report.exists(),'Allocated report already exists; do not overwrite'
print('Allocated report absent; source read-only checks complete')
PY
```

Actual final output:

```text
.github/agents/ama-backlog-delivery-coordinator.agent.md: exact expected SHA256; unchanged frontmatter
Non-tool frontmatter keys: name, description; no capability-bearing keys added, removed or altered
Changed reference resolves: .github/agents/ama-backlog-delivery-coordinator.agent.md -> ../../docs/architecture/cutover-evidence-pack.md
Changed reference resolves: .github/agents/ama-backlog-delivery-coordinator.agent.md -> ../../src/README.md#stabilization-validation-ladder
src/README.md: exact expected SHA256; unchanged frontmatter
Changed reference resolves: src/README.md -> ../docs/case_study_48_addendum.md#revised-owner-budget-decision-2026-10-22
Changed reference resolves: src/README.md -> #local-rpi-gate
git diff --check -- .github/agents/ama-backlog-delivery-coordinator.agent.md src/README.md: exit=0; stdout=''; stderr=''
Allocated report absent; source read-only checks complete
```

Preserved checker failure: the first execution of the same Python command
used `target=(p.parent/local).resolve()` without the empty-local-path branch.
It exited 1 after the first three successful references with
`IsADirectoryError: [Errno 21] Is a directory` for the current worktree's src
directory. That was a validator bug handling `#local-rpi-gate`, not a broken
source reference. Only the in-memory checker was corrected; no source was
edited. The final complete rerun above passed.

## Handoff

Metadata, unchanged frontmatter and changed-reference integrity pass locally.
Native discovery is still unmet, so the mechanical stage remains Deferred,
not Pass. Execute the exact safe rerun condition above before claiming host
validation success. Hosted checks and the final policy-publication local RPI
gate are separate later work and were not run or replaced by this report.
