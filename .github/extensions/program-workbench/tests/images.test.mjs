import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { startProgramWorkbenchServer } from "../server.mjs";

test("documentation images require a token and remain confined to docs", async () => {
  const root = await mkdtemp(join(tmpdir(), "workbench-images-"));
  let entry;
  try {
    await mkdir(join(root, "docs"));
    const svg = Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"><rect width="100" height="50"/></svg>');
    await writeFile(join(root, "docs", "diagram.svg"), svg);
    await writeFile(join(root, "outside.svg"), svg);
    await writeFile(join(root, "docs", "source.md"), "# Private source");
    await writeFile(join(root, "docs", "large.png"), Buffer.alloc(20 * 1024 * 1024 + 1));
    await symlink(root, join(root, "docs", "escape"), "junction");
    entry = await startProgramWorkbenchServer({ repositoryRoot: root });
    const media = (path, token = entry.token) => `${entry.url}media?path=${encodeURIComponent(path)}&token=${token}`;
    assert.equal((await fetch(media("docs/diagram.svg", ""))).status, 403);
    const response = await fetch(media("docs/diagram.svg"));
    assert.equal(response.status, 200);
    assert.equal(response.headers.get("content-type"), "image/svg+xml");
    assert.equal(response.headers.get("x-content-type-options"), "nosniff");
    assert.match(response.headers.get("content-security-policy"), /sandbox/);
    assert.deepEqual(Buffer.from(await response.arrayBuffer()), svg);
    for (const path of ["outside.svg", "docs/../outside.svg", "../outside.svg", "docs/source.md", "docs/large.png", "docs/escape/outside.svg"]) {
      assert.equal((await fetch(media(path))).status, 400, path);
    }
    assert.equal((await fetch(media("docs/diagram.svg"), { method: "POST" })).status, 405);
    const renderer = await fetch(`${entry.url}diagram.html`);
    assert.equal(renderer.status, 200);
    assert.match(renderer.headers.get("content-security-policy"), /sandbox allow-scripts/);
    assert.match(renderer.headers.get("content-security-policy"), /default-src 'none'/);
    assert.equal((await fetch(`${entry.url}vendor/mermaid.js`)).status, 200);
    const logo = await fetch(`${entry.url}zava-logo.png`);
    assert.equal(logo.headers.get("content-type"), "image/png");
    assert.deepEqual(Buffer.from(await logo.arrayBuffer()), await readFile(new URL("../assets/zava-logo.png", import.meta.url)));
  } finally {
    if (entry) await new Promise((resolve) => entry.server.close(resolve));
    await rm(root, { recursive: true, force: true });
  }
});
