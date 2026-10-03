import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { requestConversation, selectProductManagerAdvisor } from "../conversation.mjs";
import { startProgramWorkbenchServer } from "../server.mjs";

test("selects the stable advisor ID and excludes subagent-only profiles", () => {
  const advisor = { id: "plugin:product-manager-advisor", displayName: "Product Manager Advisor" };
  assert.equal(selectProductManagerAdvisor([{ ...advisor, userInvocable: false }, advisor]), advisor);
  assert.equal(selectProductManagerAdvisor([{ id: "unrelated" }]), undefined);
});

test("requests a detached chat with file attachment and conditional agent selection", async () => {
  for (const agents of [[], [{ id: "hve:product-manager-advisor" }]]) {
    let sent;
    const session = {
      rpc: { agent: { list: async () => ({ agents }) } },
      send: async (options) => { sent = options; return "test-message"; },
    };
    const result = await requestConversation(session, "docs/example.md");
    assert.equal(result.messageId, "test-message");
    assert.equal(result.agent, agents[0]?.id || null);
    assert.equal(sent.mode, "immediate");
    assert.match(sent.prompt, /session_kind "chat", detached true/);
    assert.match(sent.prompt, /kickoff\.attachments/);
    assert.match(sent.prompt, /navigate_to/);
    assert.match(sent.prompt, agents.length ? /exact ID/ : /Omit kickoff\.agent/);
  }
  await assert.rejects(requestConversation({
    rpc: { agent: { list: async () => { throw new Error("Discovery unavailable"); } } },
  }, "README.md"), /Discovery unavailable/);
});

test("conversation endpoint accepts protected Markdown, rejects invalid paths and surfaces errors", async () => {
  const root = await mkdtemp(join(tmpdir(), "workbench-conversation-"));
  let entry;
  try {
    await mkdir(join(root, "docs"));
    await writeFile(join(root, "README.md"), "# README");
    await writeFile(join(root, "docs", "case_study_48_original.md"), "# Protected");
    const paths = [];
    entry = await startProgramWorkbenchServer({
      repositoryRoot: root,
      requestConversation: async (path) => { paths.push(path); return { messageId: "queued", agent: null }; },
    });
    const post = (path, token = entry.token) => fetch(`${entry.url}api/start-conversation`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Canvas-Token": token },
      body: JSON.stringify({ path }),
    });
    const response = await post("docs/case_study_48_original.md");
    assert.equal(response.status, 202);
    assert.equal((await response.json()).messageId, "queued");
    assert.equal((await post("../outside.md")).status, 400);
    assert.equal((await post("README.md", "invalid")).status, 403);
    assert.deepEqual(paths, ["docs/case_study_48_original.md"]);
  } finally {
    if (entry) await new Promise((resolve) => entry.server.close(resolve));
    await rm(root, { recursive: true });
  }
});
