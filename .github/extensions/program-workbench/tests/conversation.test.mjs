import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { requestConversation, selectProductManagerAdvisor } from "../conversation.mjs";
import { startProgramWorkbenchServer } from "../server.mjs";

test("serves the exact logo bytes and external sizing rule without relaxing CSP", async () => {
  const entry = await startProgramWorkbenchServer();
  try {
    const response = await fetch(entry.url);
    assert.equal(response.status, 200);
    assert.match(response.headers.get("content-security-policy"), /(?:^|; )style-src 'self';/);
    const html = await response.text();
    assert.match(html, /href="\/styles.css"/);
    assert.match(html, /class="zava-logo"/);
    assert.doesNotMatch(html, /<style>/);
    const css = await fetch(`${entry.url}styles.css`);
    assert.equal(css.status, 200);
    assert.match(await css.text(), /\.zava-logo\s*\{[^}]*width:114px;[^}]*height:40px;[^}]*flex-shrink:0;/);
    const logo = await fetch(`${entry.url}zava-logo.png`);
    assert.equal(logo.status, 200);
    assert.equal(logo.headers.get("content-type"), "image/png");
    const expected = await readFile(new URL("../assets/zava-logo.png", import.meta.url));
    assert.deepEqual(Buffer.from(await logo.arrayBuffer()), expected);
  } finally {
    await new Promise((resolve) => entry.server.close(resolve));
  }
});

test("selects the stable advisor ID and excludes subagent-only profiles", () => {
  const advisor = { id: "plugin:product-manager-advisor", displayName: "Product Manager Advisor" };
  assert.equal(selectProductManagerAdvisor([{ ...advisor, userInvocable: false }, advisor]), advisor);
  assert.equal(selectProductManagerAdvisor([{ id: "unrelated" }]), undefined);
});

test("requests a new project conversation with file attachment and conditional agent selection", async () => {
  for (const agents of [[], [{ id: "hve:product-manager-advisor" }]]) {
    let sent;
    const session = {
      rpc: { agent: { list: async () => ({ agents }) } },
      send: async (options) => { sent = options; return "test-message"; },
    };
    const result = await requestConversation(session, "docs/example.md", { target: "new" });
    assert.equal(result.messageId, "test-message");
    assert.equal(result.agent, agents[0]?.id || null);
    assert.equal(sent.mode, "immediate");
    assert.match(sent.prompt, /session_kind "project"/);
    assert.match(sent.prompt, /detached false/);
    assert.match(sent.prompt, /kickoff\.attachments/);
    assert.match(sent.prompt, /navigate_to/);
    assert.match(sent.prompt, agents.length ? /exact ID/ : /Omit kickoff\.agent/);
  }
  await assert.rejects(requestConversation({
    rpc: { agent: { list: async () => { throw new Error("Discovery unavailable"); } } },
  }, "README.md"), /Discovery unavailable/);
});

test("current conversation sends context directly and selects advisor before sending", async () => {
  for (const agents of [[], [{ id: "hve:product-manager-advisor" }]]) {
    const calls = [];
    let sent;
    const session = {
      sessionId: "current-session",
      rpc: { agent: {
        list: async () => ({ agents }),
        select: async (request) => { calls.push(request); },
      } },
      send: async (options) => { sent = options; return "message"; },
    };
    const absolutePath = join(tmpdir(), "example.md");
    await requestConversation(session, "docs/example.md", { absolutePath });
    assert.deepEqual(sent.attachments, [{ type: "file", path: absolutePath, displayName: "docs/example.md" }]);
    assert.match(sent.prompt, /Briefly acknowledge/);
    assert.match(sent.prompt, /"current-session"/);
    assert.doesNotMatch(sent.prompt, /Use create_session/);
    assert.deepEqual(calls, agents.length ? [{ name: agents[0].id }] : []);
  }
  await assert.rejects(requestConversation({}, "README.md", { target: "invalid" }), /Unknown conversation target/);
  await assert.rejects(requestConversation({
    rpc: { agent: { list: async () => ({ agents: [] }) } },
  }, "README.md"), /context file path/);
});

test("conversation endpoint accepts protected Markdown, rejects invalid paths and surfaces errors", async () => {
  const root = await mkdtemp(join(tmpdir(), "workbench-conversation-"));
  let entry;
  try {
    await mkdir(join(root, "docs"));
    await writeFile(join(root, "README.md"), "# README");
    await writeFile(join(root, "docs", "case_study_48_original.md"), "# Protected");
    const paths = [], targets = [];
    entry = await startProgramWorkbenchServer({
      repositoryRoot: root,
      requestConversation: async (path, options) => {
        paths.push(path); targets.push(options);
        return { messageId: "queued", agent: null };
      },
    });
    const post = (path, token = entry.token, target) => fetch(`${entry.url}api/start-conversation`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Canvas-Token": token },
      body: JSON.stringify({ path, target }),
    });
    const response = await post("docs/case_study_48_original.md");
    assert.equal(response.status, 202);
    assert.equal((await response.json()).messageId, "queued");
    assert.equal((await post("../outside.md")).status, 400);
    assert.equal((await post("README.md", "invalid")).status, 403);
    assert.equal((await post("README.md", entry.token, "invalid")).status, 400);
    assert.equal((await post("README.md", entry.token, "new")).status, 202);
    assert.deepEqual(paths, ["docs/case_study_48_original.md", "README.md"]);
    assert.deepEqual(targets, [
      { target: "current", absolutePath: join(root, "docs/case_study_48_original.md") },
      { target: "new", absolutePath: join(root, "README.md") },
    ]);
  } finally {
    if (entry) await new Promise((resolve) => entry.server.close(resolve));
    await rm(root, { recursive: true });
  }
});
