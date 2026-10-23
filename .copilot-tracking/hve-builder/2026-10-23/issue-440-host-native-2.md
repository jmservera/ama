---
title: Issue440 contained native host discovery continuation
description: Actual networkless chooser evidence preserves unmet candidate discovery
ms.date: 2026-10-23
---

## Result

Host validation remains Deferred. Original generic validator's metadata,
frontmatter/reference passes and initial Deferred report are preserved.
Parent attempted a narrower enforced-isolation alternative; actual native CLI
chooser ran, but displayed "No custom agents found in this workspace yet."
This is not candidate discovery success, native workflow acceptance or a
confirmed repository-agent defect.

## Containment and actual attempts

All container names ama-440-host-listing-1 through -7 are task-owned and stopped,
not removed. No foreign receipt/environment was used. Missing public base image
was observed (`docker image inspect python:3.12-slim` failed), then official
node:24-bookworm-slim was pulled for local tooling only; no source upload.
No Azure/Graph/Entra, app model API, private HOME/config/credentials, private
roster/data/support or other worktree was mounted/read. No model prompt,
coordinator selection or coordinator workflow executed.

Each container had network none, read-only root, uid1000, cap-drop ALL,
no-new-privileges, pids128/memory768m/cpu1, isolated tmpfs HOME and /tmp.
Only actual worktree .github/agents and public installed Copilot runtime were
bound read-only. Last attempt additionally mounted the owned exact-main external
export's Git metadata and public git executable read-only; no primary/shared
worktree metadata mounted. Last per-process Git safe.directory names /workspace.
Source SHA256 values still equal static/behavior identities.

| Attempt | Actual result | Retained external evidence |
| --- | --- | --- |
| 1 | Native addon could not map from default noexec HOME tmpfs; CLI exit1 | /tmp/ama-440-host-native-20261023 |
| 2 | HOME tmpfs exec corrected; invalid trust-folder positional path, exit1 | /tmp/ama-440-host-native-exec-20261023 |
| 3 | trust-folder is prompt-mode-only, exit1 | /tmp/ama-440-host-native-final-20261023 |
| 4 | Interactive startup with zero-size PTY produced no list, exit1; no log directory to copy | /tmp/ama-440-host-native-interactive-20261023 |
| 5 | Sized PTY started, trust prompt consumed first slash submission; login banner, exit0, no chooser evidence | /tmp/ama-440-host-native-sized-20261023 |
| 6 | Sized PTY explicitly accepted container-only folder trust, submitted /agent, dismissed without selection, /exit; actual chooser empty, exit0 | /tmp/ama-440-host-native-chooser-20261023 |
| 7 | Added read-only owned public Git metadata/executable; omitted no-custom-instructions flag to avoid masking discovery; same actual empty chooser, exit0 | /tmp/ama-440-host-native-git-20261023 |

Raw argv/transcript.bin/transcript.txt are retained per directory; final two also
contain transcript-clean.txt. This is generated host output, not instructions.
Actual successful-start argv uses `docker run ... -it node:24-bookworm-slim
/opt/copilot-runtime/bin/node
/opt/copilot-runtime/lib/node_modules/@github/copilot/npm-loader.js
--no-auto-update --available-tools --disable-builtin-mcps --no-ask-user
--disable-client-telemetry`. No authentication or network was enabled.
CLI shows "Please use /login to sign in to use Copilot"; its role in absent
discovery is unknown, not asserted. Empty listing cannot verify exact candidate.

## Gate and resume

Local metadata/frontmatter/changed-reference checks Pass in original independent
report; mechanical host stage Deferred, so HVE overall Deferred, not Pass.
No tool configuration or model surface changed or graded. Human review remains
unchecked. Independent local runtime checkpoint can continue; publication cannot.

Resume P04-T01 only with a supported safe host discovery mechanism that actually
lists this exact candidate (same two SHA256 identities), without launching it,
model submissions, private credentials/data or shared-system effects. Preserve
the original negative evidence. If authenticated discovery is necessary, obtain
explicit bounded authority/containment rather than enabling network or importing
credentials into this container. Further blind retries are not justified here.
